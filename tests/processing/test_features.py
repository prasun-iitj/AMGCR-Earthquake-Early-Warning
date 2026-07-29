import pytest
from dataclasses import fields
from src.processing.features import VerticalPWaveFeatures, extract_vertical_features

def test_feature_schema():
    """
    Tests that the VerticalPWaveFeatures class has exactly seven named features.
    
    Trace: RE §4, §16
    """
    expected_features = {"tau_c", "ID2", "IV2", "PI", "RSSCV", "Tva", "CAV"}
    feature_fields = {field.name for field in fields(VerticalPWaveFeatures)}
    
    assert feature_fields == expected_features, \
        f"Expected features {expected_features}, but got {feature_fields}"

def test_feature_extraction_blocks_missing_formulae():
    """
    Tests that extract_vertical_features blocks numeric extraction.
    
    Trace: RE §4, §16
    """
    with pytest.raises(NotImplementedError) as excinfo:
        extract_vertical_features(None)
    
    assert "Numerical feature extraction is blocked" in str(excinfo.value)
    assert "approved deviation" in str(excinfo.value)