"""Phase 6 evaluation, timing, and reproducibility tests.

Trace: test_metric_equations_and_scale_guard, test_exact_run_blocks_unresolved_fields;
RE §9–§16.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pytest

from src.data.manifest import ManifestRecord
from src.evaluation.benchmarks import (
    INDIA_CROSS_REGION_MAGNITUDE_SCALE,
    JAPAN_TEST_MAGNITUDE_SCALE,
    NOTO_HOLDOUT_MAGNITUDE_SCALE,
    evaluate_india_cross_region,
    evaluate_japan_test,
    evaluate_noto_holdout,
)
from src.evaluation.metrics import (
    MagnitudeScaleMismatchError,
    mean_absolute_error,
    percent_mae_improvement,
    require_matching_magnitude_scales,
    root_mean_squared_error,
)
from src.evaluation.timing import measure_training_seconds_per_epoch
from src.experiments.run_metadata import (
    ExactReproductionBlockedError,
    assert_no_unresolved_settings,
    build_experiment_metadata,
    collect_unresolved_config_paths,
    load_earthesnd_config_bundle,
    write_deviation_log,
)


def _make_record(**overrides: object) -> ManifestRecord:
    values: dict[str, object] = {
        "event_id": "event-001",
        "station_id": "station-001",
        "component_paths": {"NS": "ns.mseed", "EW": "ew.mseed", "UD": "ud.mseed"},
        "p_pick": "2024-01-01T00:00:00Z",
        "sampling_rate_hz": 100.0,
        "station_scaling_provenance": "unresolved-project-assumption",
        "magnitude": 4.2,
        "magnitude_scale": "M_JMA",
        "epicentral_distance_km": 10.0,
        "focal_depth_km": 5.0,
        "hypocentral_distance_km": 11.0,
        "split": "test",
        "is_noto_holdout": False,
        "source_region": "japan",
    }
    values.update(overrides)
    return ManifestRecord(**values)  # type: ignore[arg-type]


class TestMetricEquations:
    def test_mean_absolute_error_equation(self) -> None:
        y_true = np.array([3.0, 5.0, 7.0])
        y_pred = np.array([2.0, 6.0, 6.0])
        assert mean_absolute_error(y_true, y_pred, magnitude_scale="M_JMA") == pytest.approx(1.0)

    def test_root_mean_squared_error_equation(self) -> None:
        y_true = np.array([1.0, 3.0])
        y_pred = np.array([1.0, 5.0])
        assert root_mean_squared_error(y_true, y_pred, magnitude_scale="M_JMA") == pytest.approx(
            np.sqrt(2.0)
        )

    def test_percent_mae_improvement_equation(self) -> None:
        # RE §9: ((MAE_other - MAE_ours) / MAE_other) * 100%
        result = percent_mae_improvement(0.80, 0.72, magnitude_scale="M_JMA")
        assert result == pytest.approx(10.0)

    def test_percent_mae_improvement_rejects_zero_baseline(self) -> None:
        with pytest.raises(ValueError, match="non-zero"):
            percent_mae_improvement(0.0, 0.1, magnitude_scale="M_JMA")

    def test_metrics_reject_mismatched_lengths(self) -> None:
        with pytest.raises(ValueError, match="same length"):
            mean_absolute_error(np.array([1.0]), np.array([1.0, 2.0]), magnitude_scale="M_JMA")


class TestMagnitudeScaleGuard:
    def test_require_matching_magnitude_scales_accepts_same_scale(self) -> None:
        require_matching_magnitude_scales("M_JMA", "M_JMA")

    def test_require_matching_magnitude_scales_rejects_cross_scale(self) -> None:
        with pytest.raises(MagnitudeScaleMismatchError, match="M_JMA"):
            require_matching_magnitude_scales("M_JMA", "M_w")

    def test_mean_absolute_error_rejects_cross_scale_target_label(self) -> None:
        y = np.array([4.0, 5.0])
        with pytest.raises(MagnitudeScaleMismatchError):
            mean_absolute_error(
                y,
                y,
                magnitude_scale="M_JMA",
                target_magnitude_scale="M_w",
            )

    def test_percent_improvement_rejects_cross_scale_mae_labels(self) -> None:
        with pytest.raises(MagnitudeScaleMismatchError):
            percent_mae_improvement(
                1.0,
                0.9,
                magnitude_scale="M_JMA",
                other_magnitude_scale="M_w",
            )


class TestBenchmarkScopes:
    def test_evaluate_japan_test_success(self) -> None:
        records = (_make_record(), _make_record(station_id="station-002"))
        y_true = np.array([4.0, 5.0])
        y_pred = np.array([4.1, 4.8])
        result = evaluate_japan_test(
            y_true,
            y_pred,
            magnitude_scale=JAPAN_TEST_MAGNITUDE_SCALE,
            records=records,
        )
        assert result.scope == "japan_test"
        assert result.magnitude_scale == "M_JMA"
        assert result.record_count == 2
        assert result.mae == pytest.approx(mean_absolute_error(y_true, y_pred, magnitude_scale="M_JMA"))

    def test_evaluate_japan_test_rejects_wrong_scale(self) -> None:
        with pytest.raises(ValueError, match="M_JMA"):
            evaluate_japan_test(
                np.array([4.0]),
                np.array([4.1]),
                magnitude_scale="M_w",
            )

    def test_evaluate_japan_test_rejects_out_of_scope_record(self) -> None:
        record = _make_record(split="train")
        with pytest.raises(ValueError, match="japan_test"):
            evaluate_japan_test(
                np.array([4.0]),
                np.array([4.1]),
                magnitude_scale=JAPAN_TEST_MAGNITUDE_SCALE,
                records=(record,),
            )

    def test_evaluate_noto_holdout_success(self) -> None:
        record = _make_record(is_noto_holdout=True, split="test")
        y_true = np.array([7.6])
        y_pred = np.array([7.4])
        result = evaluate_noto_holdout(
            y_true,
            y_pred,
            magnitude_scale=NOTO_HOLDOUT_MAGNITUDE_SCALE,
            records=(record,),
        )
        assert result.scope == "noto_holdout"
        assert result.magnitude_scale == "M_JMA"

    def test_evaluate_india_cross_region_success(self) -> None:
        record = _make_record(source_region="india", magnitude_scale="M_w", split="test")
        y_true = np.array([5.1, 5.3])
        y_pred = np.array([5.0, 5.5])
        result = evaluate_india_cross_region(
            y_true,
            y_pred,
            magnitude_scale=INDIA_CROSS_REGION_MAGNITUDE_SCALE,
            records=(record, record),
        )
        assert result.scope == "india_cross_region"
        assert result.magnitude_scale == "M_w"

    def test_evaluate_india_rejects_m_jma_on_records(self) -> None:
        record = _make_record(source_region="india", magnitude_scale="M_JMA")
        with pytest.raises(ValueError, match="M_w"):
            evaluate_india_cross_region(
                np.array([5.0]),
                np.array([5.1]),
                magnitude_scale=INDIA_CROSS_REGION_MAGNITUDE_SCALE,
                records=(record,),
            )


class TestTrainingTiming:
    def test_measure_training_seconds_per_epoch_records_elapsed_time(self) -> None:
        calls = {"count": 0}

        def one_epoch() -> None:
            calls["count"] += 1

        result = measure_training_seconds_per_epoch(
            one_epoch,
            timing_environment={"device": "test-cpu", "framework": "pytest"},
        )
        assert calls["count"] == 1
        assert result.seconds_per_epoch >= 0.0
        assert result.timing_environment == (("device", "test-cpu"), ("framework", "pytest"))

    def test_measure_training_seconds_per_epoch_requires_environment(self) -> None:
        with pytest.raises(ValueError, match="timing_environment"):
            measure_training_seconds_per_epoch(lambda: None, timing_environment=None)
        with pytest.raises(ValueError, match="timing_environment"):
            measure_training_seconds_per_epoch(lambda: None, timing_environment={})


class TestRunMetadata:
    CONFIG_DIR = Path("configs/earthesnd")

    def test_collect_unresolved_config_paths_finds_nested_nulls(self) -> None:
        sample = {"a": {"b": None}, "c": 1}
        paths = collect_unresolved_config_paths(sample)
        assert paths == ["a.b"]

    def test_assert_no_unresolved_settings_allows_non_exact_runs(self) -> None:
        assert_no_unresolved_settings(
            {"data.yaml": {"split": {"random_seed": None}}},
            exact_reproduction_claim=False,
        )

    def test_exact_run_blocks_unresolved_fields(self) -> None:
        configs = load_earthesnd_config_bundle(self.CONFIG_DIR)
        with pytest.raises(ExactReproductionBlockedError, match="null"):
            assert_no_unresolved_settings(configs, exact_reproduction_claim=True)

    def test_build_experiment_metadata_persists_unresolved_list(self) -> None:
        configs = load_earthesnd_config_bundle(self.CONFIG_DIR)
        metadata = build_experiment_metadata(
            run_id="phase6-test",
            configs=configs,
            target_scales_used=("M_JMA", "M_w"),
            exact_reproduction_claim=False,
            created_at_utc="2026-01-01T00:00:00+00:00",
        )
        assert metadata.run_id == "phase6-test"
        assert "data.yaml:split.random_seed" in metadata.unresolved_config_fields
        assert metadata.feature_count_conflict_note
        assert metadata.target_scales_used == ("M_JMA", "M_w")

    def test_write_deviation_log_round_trip(self, tmp_path: Path) -> None:
        configs = {"evaluation.yaml": {"timing_environment": None}}
        metadata = build_experiment_metadata(
            run_id="log-test",
            configs=configs,
            deviations=("Used record-level MAE aggregation",),
            project_assumptions=("JSON deviation log format",),
            target_scales_used=("M_JMA",),
            exact_reproduction_claim=False,
            created_at_utc="2026-01-01T00:00:00+00:00",
        )
        output = tmp_path / "deviation_log.json"
        write_deviation_log(metadata, output)
        loaded = json.loads(output.read_text(encoding="utf-8"))
        assert loaded["run_id"] == "log-test"
        assert loaded["deviations"] == ["Used record-level MAE aggregation"]
        assert loaded == metadata.to_dict()

    def test_write_deviation_log_blocks_exact_claim_with_nulls(self, tmp_path: Path) -> None:
        metadata = build_experiment_metadata(
            run_id="blocked",
            configs={"model.yaml": {"esn": {"layer_count": None}}},
            target_scales_used=("M_JMA",),
            exact_reproduction_claim=False,
            created_at_utc="2026-01-01T00:00:00+00:00",
        )
        exact_metadata = metadata.__class__(**{**asdict(metadata), "exact_reproduction_claim": True})
        with pytest.raises(ExactReproductionBlockedError):
            write_deviation_log(exact_metadata, tmp_path / "blocked.json")
