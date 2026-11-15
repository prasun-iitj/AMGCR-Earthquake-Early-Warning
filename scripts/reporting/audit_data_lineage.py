"""Read-only data lineage audit.

Counts events / records / stations / files from existing manifests, feature
matrices, schemas, saved models and (if present) the local raw-data folders,
and writes reports/data_lineage/data_lineage_summary.json.

It does not read waveform samples, retrain, re-extract or modify any input.
The JSON is committed so that the website and reviewers can see the verified
numbers even when raw data (git-ignored) is absent.

Usage (repo root):  python scripts/reporting/audit_data_lineage.py
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/data_lineage"
OUT.mkdir(parents=True, exist_ok=True)


def count_files(rel: str, suffix: str) -> int | None:
    p = ROOT / rel
    if not p.exists():
        return None
    return sum(1 for f in p.rglob("*") if f.is_file() and f.suffix.lower() == suffix)


def rng(s: pd.Series) -> list[float]:
    return [round(float(s.min()), 3), round(float(s.max()), 3)]


def vc(s: pd.Series) -> dict[str, int]:
    return {str(k): int(v) for k, v in s.value_counts().items()}


def main() -> None:
    m = ROOT / "data/manifests"
    ca = pd.read_csv(m / "iris_california_pilot_events.csv")
    a_man = pd.read_csv(m / "sed_switzerland_pilot_events.csv")
    a_pk = pd.read_csv(m / "sed_switzerland_set_a_picks.csv")
    c_man = pd.read_csv(m / "sed_switzerland_validation_waveforms.csv")
    c_pk = pd.read_csv(m / "sed_switzerland_validation_picks.csv")
    cand = pd.read_csv(m / "sed_switzerland_validation_candidates.csv")
    fa = pd.read_csv(ROOT / "reports/features/swiss_set_a_feature_matrix.csv")
    fc = pd.read_csv(ROOT / "reports/features/swiss_set_c_feature_matrix.csv")
    schema = json.load(open(ROOT / "reports/ml/vertical_feature_schema.json"))["features"]

    # California -------------------------------------------------------
    ca_files = [f for s in ca.waveform_files for f in str(s).split(";")]
    ca_sta = sorted({Path(f).name.split(".")[1] for f in ca_files})
    ca_ch = sorted({".".join(Path(f).name.split(".")[:4]) for f in ca_files})
    iris_dir = ROOT / "data/raw/iris"
    local_iris = sorted(p.name for p in iris_dir.rglob("*.mseed")) if iris_dir.exists() else []
    manifest_names = {Path(f).name for f in ca_files}
    california = {
        "events": int(ca.event_id.nunique()),
        "waveform_files_in_manifest": len(ca_files),
        "stations_in_manifest": ca_sta,
        "channels_in_manifest": ca_ch,
        "magnitude_range": rng(ca.magnitude),
        "origin_time_range": [ca.origin_time_utc.min(), ca.origin_time_utc.max()],
        "providers": {"events": sorted(ca.fdsn_event_provider.unique()), "waveforms": sorted(ca.fdsn_waveform_provider.unique())},
        "local_raw_mseed_files": len(local_iris) if iris_dir.exists() else None,
        "local_raw_files_not_in_manifest": sorted(set(local_iris) - manifest_names) if iris_dir.exists() else None,
        "stationxml_saved": False,
        "p_pick_method": "automatic STA/LTA (0.5 s / 10 s, threshold 2.5); no analyst picks",
    }

    # Set A ------------------------------------------------------------
    a_events = a_man.event_id.nunique()
    set_a = {
        "events": int(a_events),
        "records": int(len(a_man)),
        "stations": int(a_man.station.nunique()),
        "channels": sorted(a_man.channels.unique()),
        "sampling_rates_hz": vc(a_man.sampling_rate_hz),
        "magnitude_range": rng(a_man.magnitude),
        "magnitude_types": vc(a_man.magnitude_type),
        "download_status": vc(a_man.download_status),
        "validation_status": vc(a_man.validation_status),
        "stationxml_available": vc(a_man.stationxml_available),
        "pre_event_seconds_min": float(a_man.pre_event_seconds.min()),
        "post_event_seconds_min": float(a_man.post_event_seconds.min()),
        "picks": {"n": int(len(a_pk)), "phases": vc(a_pk.pick_phase), "evaluation_mode": vc(a_pk.pick_evaluation_mode), "source": sorted(a_pk.pick_source.unique())},
        "windows": {"total": int(len(fa)), "positive": int((fa.is_earthquake == 1).sum()), "negative": int((fa.is_earthquake == 0).sum())},
        "p_latency_s_range": rng(fa.p_latency_s),
        "epicentral_distance_km_range": rng(fa.epicentral_distance_km),
        "local_raw_mseed_files": count_files("data/raw/switzerland", ".mseed"),
        "local_stationxml_files": count_files("data/metadata/switzerland", ".xml"),
        "events_table": [
            {"short_id": str(k).split("/")[-1], "region": g.region.iloc[0], "magnitude": round(float(g.magnitude.iloc[0]), 2), "records": int(len(g)), "stations": int(g.station.nunique())}
            for k, g in a_man.groupby("event_id", sort=False)
        ],
    }

    # Set C ------------------------------------------------------------
    set_c = {
        "events": int(c_man.short_id.nunique()),
        "records": int(len(c_man)),
        "stations": int(c_man.station.nunique()),
        "channels": sorted(c_man.channel.unique()),
        "sampling_rates_hz": vc(c_man.sampling_rate),
        "magnitude_range": rng(c_man.magnitude),
        "location_class_records": vc(c_man.location_class),
        "download_status": vc(c_man.download_status),
        "verification_status": vc(c_man.verification_status),
        "coverage_status": vc(c_man.coverage_status),
        "stationxml_status": vc(c_man.StationXML_status),
        "gaps_total": int(c_man.gaps.sum()),
        "overlaps_total": int(c_man.overlaps.sum()),
        "picks": {"n": int(len(c_pk)), "phases": vc(c_pk.pick_phase), "evaluation_mode": vc(c_pk.pick_evaluation_mode), "source": sorted(c_pk.pick_source.unique())},
        "candidate_pool": {"rows": int(len(cand)), "pool_role": vc(cand.pool_role), "in_development_set": vc(cand.in_development_set)},
        "windows": {"total": int(len(fc)), "positive": int((fc.is_earthquake == 1).sum()), "negative": int((fc.is_earthquake == 0).sum())},
        "feature_matrix_sampling_rates_hz": vc(fc.sampling_rate_hz),
        "local_raw_mseed_files": count_files("data/raw/switzerland_validation", ".mseed"),
        "local_stationxml_files": count_files("data/metadata/switzerland_validation", ".xml"),
        "events_table": [
            {"short_id": k, "region": g.region.iloc[0], "location_class": g.location_class.iloc[0], "magnitude": round(float(g.magnitude.iloc[0]), 2), "records": int(len(g)), "stations": int(g.station.nunique())}
            for k, g in c_man.groupby("short_id", sort=False)
        ],
    }

    # Overlap ----------------------------------------------------------
    sa, sc = set(fa.station), set(fc.station)
    overlap = {
        "event_overlap": len(set(fa.short_id) & set(fc.short_id)),
        "stations_set_a": len(sa), "stations_set_c": len(sc),
        "stations_shared": len(sa & sc), "stations_set_c_only": len(sc - sa), "stations_set_a_only": len(sa - sc),
        "set_c_records_at_shared_stations": int(c_man.station.isin(sa).sum()),
    }

    # Schemas ----------------------------------------------------------
    meta_a = ["event_id", "short_id", "station", "channel_group", "sampling_rate_hz", "magnitude", "magnitude_type", "region", "epicentral_distance_km", "hypocentral_distance_km", "origin_time_utc", "p_pick_time_utc", "p_latency_s", "p_phase", "p_evaluation_mode", "sample_id", "window_type", "is_earthquake", "window_start_utc", "window_end_utc", "window_duration_s"]
    feat24 = [c for c in fa.columns if c not in meta_a]
    models = {}
    for name in ["swiss_rf_model", "swiss_xgb_model", "vertical_rf_model_set_a", "vertical_xgb_model_set_a"]:
        p = joblib.load(ROOT / f"reports/ml/{name}.joblib")
        models[name] = list(p["feature_columns"])
    schemas = {
        "set_a_matrix_columns": list(fa.columns), "set_c_matrix_columns": list(fc.columns),
        "feature_columns_24_in_set_a_matrix_order": feat24,
        "vertical_schema_json": schema,
        "saved_model_feature_columns": models,
        "vertical_schema_matches_vertical_models": all(models[k] == schema for k in ["vertical_rf_model_set_a", "vertical_xgb_model_set_a"]),
        "vertical_schema_is_subset_of_set_a_matrix": all(c in fa.columns for c in schema),
        "vertical_schema_is_subset_of_set_c_matrix": all(c in fc.columns for c in schema),
        "24_feature_models_match_each_other": models["swiss_rf_model"] == models["swiss_xgb_model"],
        "24_feature_model_order_equals_set_a_matrix_order": models["swiss_rf_model"] == feat24,
        "n_24": len(models["swiss_rf_model"]), "n_18": len(schema),
        "nan_counts": {"set_a_features": int(fa[feat24].isna().sum().sum()), "set_c_features": int(fc[schema].isna().sum().sum())},
    }

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Counts derived from manifests, feature matrices, schemas, saved models and local folders. No waveform samples were read.",
        "california": california, "set_a": set_a, "set_c": set_c, "overlap": overlap, "schemas": schemas,
    }
    out = OUT / "data_lineage_summary.json"
    out.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
