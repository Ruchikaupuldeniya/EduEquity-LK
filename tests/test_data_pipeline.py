"""
EduEquity LK - Test Suite
Verifies data pipeline integrity, dataset schemas, mathematical constraints, and risk model sanity.
"""

import os
import sys
import json
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_pipeline import DataPipeline
from src.analysis import EduEquityAnalyzer
from src.utils import standardize_district_name, classify_risk_tier
from src.i18n import t, get_localized_district, get_localized_province, get_localized_risk_tier, DISTRICT_NAMES_SINHALA, TRANSLATIONS

SRI_LANKA_25_DISTRICTS = {
    "Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya",
    "Galle", "Matara", "Hambantota", "Jaffna", "Kilinochchi", "Mannar",
    "Vavuniya", "Mullaitivu", "Batticaloa", "Ampara", "Trincomalee",
    "Kurunegala", "Puttalam", "Anuradhapura", "Polonnaruwa", "Badulla",
    "Monaragala", "Ratnapura", "Kegalle"
}

def test_raw_files_exist():
    """Verify that all raw source files exist and have non-zero size."""
    expected_files = [
        "data/raw/moe_school_census_2014_2024.csv",
        "data/raw/dcs_child_activity_survey_2016.csv",
        "data/raw/dcs_district_socioeconomic_indicators.csv",
        "data/raw/moe_grade_progression_dropout.csv",
        "data/raw/sri_lanka_districts.geojson"
    ]
    for rel_path in expected_files:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        assert os.path.exists(full_path), f"Missing raw data file: {rel_path}"
        assert os.path.getsize(full_path) > 0, f"Raw data file is empty: {rel_path}"

def test_geojson_validity():
    """Verify that the GeoJSON contains exactly 25 district polygons."""
    geojson_path = os.path.join(PROJECT_ROOT, "data/raw/sri_lanka_districts.geojson")
    with open(geojson_path, "r", encoding="utf-8") as f:
        geo_data = json.load(f)
    features = geo_data.get("features", [])
    assert len(features) == 25, f"Expected 25 districts in GeoJSON, found {len(features)}"
    
    districts = {f["properties"]["district"] for f in features}
    assert districts == SRI_LANKA_25_DISTRICTS, "GeoJSON district set does not match official 25 districts"

def test_data_pipeline_execution():
    """Verify that data pipeline executes cleanly and outputs valid processed files."""
    pipeline = DataPipeline(
        raw_dir=os.path.join(PROJECT_ROOT, "data/raw"),
        processed_dir=os.path.join(PROJECT_ROOT, "data/processed")
    )
    results = pipeline.process_and_save_all()
    
    master_df = results["master_timeseries"]
    assert isinstance(master_df, pd.DataFrame)
    assert len(master_df) == 25 * 11, f"Expected 275 rows (25 districts * 11 years), got {len(master_df)}"
    
    master_districts = set(master_df["district"].unique())
    assert master_districts == SRI_LANKA_25_DISTRICTS

def test_master_dataset_value_ranges():
    """Verify mathematical boundaries on percentages and counts in master dataset."""
    master_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data/processed/master_district_timeseries.csv"))
    
    assert master_df["dropout_rate_pct"].between(0.0, 100.0).all(), "Dropout rate outside valid percentage range"
    assert master_df["poverty_headcount_pct"].between(0.0, 100.0).all(), "Poverty headcount outside valid percentage range"
    assert master_df["estate_pop_pct"].between(0.0, 100.0).all(), "Estate population outside valid percentage range"
    assert (master_df["total_enrolment"] > 0).all(), "Enrolment count must be positive"
    assert (master_df["dropout_count"] >= 0).all(), "Dropout count cannot be negative"
    assert master_df["year"].between(2014, 2024).all(), "Years outside 2014-2024 range"

def test_sector_disparity_logic():
    """Verify that estate sector exhibits higher out-of-school and child labor rates than urban."""
    sector_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data/processed/sector_equity_benchmark.csv"))
    
    urban_oos = sector_df[sector_df["sector"] == "Urban"]["not_attending_never_attended_pct"].values[0]
    estate_oos = sector_df[sector_df["sector"] == "Estate"]["not_attending_never_attended_pct"].values[0]
    
    assert estate_oos > urban_oos, "Estate out-of-school rate should be higher than urban"
    assert estate_oos > 15.0, "Estate out-of-school rate should reflect high CAS findings (>15%)"

def test_grade_matrix_cliff():
    """Verify that Grade 11 dropout rate is higher than Grade 1 dropout across all sectors."""
    grade_df = pd.read_csv(os.path.join(PROJECT_ROOT, "data/processed/grade_dropout_matrix.csv"))
    
    g1 = grade_df[grade_df["grade_number"] == 1].iloc[0]
    g11 = grade_df[grade_df["grade_number"] == 11].iloc[0]
    
    assert g11["estate_dropout_rate_pct"] > g1["estate_dropout_rate_pct"], "Grade 11 estate dropout must exceed Grade 1"
    assert g11["urban_dropout_rate_pct"] > g1["urban_dropout_rate_pct"], "Grade 11 urban dropout must exceed Grade 1"

def test_risk_model_output_bounds():
    """Verify that district risk scores are calibrated between 0 and 100."""
    analyzer = EduEquityAnalyzer(
        processed_dir=os.path.join(PROJECT_ROOT, "data/processed"),
        reports_dir=os.path.join(PROJECT_ROOT, "reports/figures")
    )
    risk_df = analyzer.train_explainable_risk_model()
    
    assert len(risk_df) == 25, "Expected 25 districts in risk score ranking"
    assert risk_df["composite_risk_score"].between(0.0, 100.0).all(), "Risk scores must be between 0 and 100"
    
    top_3 = risk_df.head(3)["district"].tolist()
    assert "Nuwara Eliya" in top_3, "Nuwara Eliya must be ranked in top 3 highest risk districts"

def test_i18n_localization():
    """Verify that all 25 districts have Sinhala mappings and translations exist for en and si."""
    for dist in SRI_LANKA_25_DISTRICTS:
        sinhala_name = get_localized_district(dist, "si")
        assert sinhala_name != dist, f"Missing Sinhala translation for district: {dist}"
        assert len(sinhala_name) > 0
        
    en_keys = set(TRANSLATIONS["en"].keys())
    si_keys = set(TRANSLATIONS["si"].keys())
    assert en_keys == si_keys, f"Mismatched i18n keys: {en_keys ^ si_keys}"
    
    # Test sample translation lookup
    assert "පාසල්" in t("app_title", "si")
    assert "EduEquity" in t("app_title", "en")

def test_utils_helpers():
    """Verify string standardizers and formatting helpers."""
    assert standardize_district_name("nuwara eliya") == "Nuwara Eliya"
    assert standardize_district_name("moneragala") == "Monaragala"
    assert classify_risk_tier(85.0) == "Critical Risk"
    assert classify_risk_tier(15.0) == "Low Risk"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
