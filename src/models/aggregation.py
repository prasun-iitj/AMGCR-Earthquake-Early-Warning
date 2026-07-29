"""Final prediction aggregation for the EarthESND ML + ESN ensemble.

The paper describes averaging six tree-model outputs with ``y_ESN``, but the
exact weights are not specified in the main article. This module therefore
requires an explicit weight mapping and never applies implicit equal weighting.

Trace: RE §7.2, §16; Spec R-ENS, test_aggregation_requires_weights.
"""

from __future__ import annotations

from collections.abc import Mapping

ENSEMBLE_PREDICTION_KEYS: frozenset[str] = frozenset(
    {
        "y_esn",
        "xgboost_real",
        "xgboost_augmented",
        "lightgbm_real",
        "lightgbm_augmented",
        "catboost_real",
        "catboost_augmented",
    }
)


def aggregate_predictions(
    predictions: Mapping[str, float],
    weights: Mapping[str, float] | None,
) -> float:
    """Combine component predictions using caller-declared weights.

    Args:
        predictions: Named scalar outputs, typically ``y_esn`` plus the six
            tabular-ensemble predictions from :func:`~src.models.tabular_ensemble.TabularEnsemble.predict_six`.
        weights: Non-empty mapping with exactly the same keys as ``predictions``.
            Must be supplied explicitly; equal ``1/7`` weighting is not assumed.

    Returns:
        The weighted sum ``sum_k w_k * prediction_k``.

    Raises:
        ValueError: If ``weights`` is ``None``, empty, or misaligned with
            ``predictions``.
    """
    if weights is None:
        raise ValueError(
            "aggregation weights must be declared explicitly; "
            "implicit equal-weight averaging is not permitted."
        )
    if not weights:
        raise ValueError("aggregation weights must be a non-empty mapping.")

    prediction_keys = frozenset(predictions)
    weight_keys = frozenset(weights)
    if prediction_keys != weight_keys:
        missing_weights = sorted(prediction_keys - weight_keys)
        extra_weights = sorted(weight_keys - prediction_keys)
        details: list[str] = []
        if missing_weights:
            details.append(f"missing weights for {missing_weights}")
        if extra_weights:
            details.append(f"unexpected weight keys {extra_weights}")
        raise ValueError(
            "aggregation weights must match prediction keys exactly "
            f"({'; '.join(details)})."
        )

    return float(sum(float(predictions[key]) * float(weights[key]) for key in predictions))
