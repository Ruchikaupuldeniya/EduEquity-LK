"""
EduEquity LK - Data Pipeline Module
Extracts, cleans, harmonizes, and merges multi-year school census and socioeconomic data.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from typing import Tuple, Dict
from src.utils import standardize_district_name

class DataPipeline:
    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        os.makedirs(self.processed_dir, exist_ok=True)
        
    def load_raw_census(self) -> pd.DataFrame:
        """Loads and standardizes MOE school census multi-year records."""
        path = os.path.join(self.raw_dir, "moe_school_census_2014_2024.csv")
        df = pd.read_csv(path)
        df["district"] = df["district"].apply(standardize_district_name)
        df["province"] = df["province"].str.strip()
        return df

    def load_raw_socioeconomic(self) -> pd.DataFrame:
        """Loads district socioeconomic indicators."""
        path = os.path.join(self.raw_dir, "dcs_district_socioeconomic_indicators.csv")
        df = pd.read_csv(path)
        df["district"] = df["district"].apply(standardize_district_name)
        df["province"] = df["province"].str.strip()
        return df

    def load_raw_cas(self) -> pd.DataFrame:
        """Loads DCS Child Activity Survey sector-level indicators."""
        path = os.path.join(self.raw_dir, "dcs_child_activity_survey_2016.csv")
        return pd.read_csv(path)

    def load_raw_grade_matrix(self) -> pd.DataFrame:
        """Loads grade progression dropout matrix."""
        path = os.path.join(self.raw_dir, "moe_grade_progression_dropout.csv")
        return pd.read_csv(path)

    def clean_and_merge_master(self) -> pd.DataFrame:
        """
        Merges time-series census data with socioeconomic indicators.
        Computes rolling changes, crisis impact metrics, and equity indices.
        """
        census_df = self.load_raw_census()
        socio_df = self.load_raw_socioeconomic()
        
        # Merge on district and province
        master = pd.merge(
            census_df,
            socio_df.drop(columns=["province"]),
            on="district",
            how="left"
        )
        
        # Derived metrics
        master["gender_dropout_gap"] = round(master["male_dropout_rate_pct"] - master["female_dropout_rate_pct"], 2)
        
        # Crisis impact ratio (comparing current year to 2019 pre-crisis baseline)
        baseline_2019 = master[master["year"] == 2019].set_index("district")["dropout_rate_pct"]
        master["pre_crisis_baseline_rate"] = master["district"].map(baseline_2019)
        master["crisis_surge_ratio"] = round(master["dropout_rate_pct"] / master["pre_crisis_baseline_rate"], 2)
        
        # Calculate composite infrastructure deficit score
        # Lower 1AB %, lower computer labs %, lower sanitation % -> higher deficit
        master["infrastructure_deficit_index"] = round(
            (100 - master["pct_schools_with_computer_labs"]) * 0.4 +
            (100 - master["pct_schools_with_sanitation"]) * 0.3 +
            (20 - master["pct_1ab_schools"]) * 1.5,
            2
        )
        
        # Sort values
        master = master.sort_values(["district", "year"]).reset_index(drop=True)
        return master

    def process_and_save_all(self) -> Dict[str, pd.DataFrame]:
        """Executes full pipeline and persists cleaned datasets."""
        print("Running EduEquity LK data pipeline...")
        master_df = self.clean_and_merge_master()
        grade_df = self.load_raw_grade_matrix()
        cas_df = self.load_raw_cas()
        socio_df = self.load_raw_socioeconomic()
        
        # Save master time series
        master_path = os.path.join(self.processed_dir, "master_district_timeseries.csv")
        master_df.to_csv(master_path, index=False)
        print(f"-> Saved master time-series ({len(master_df)} rows) to {master_path}")
        
        # Save grade matrix
        grade_path = os.path.join(self.processed_dir, "grade_dropout_matrix.csv")
        grade_df.to_csv(grade_path, index=False)
        print(f"-> Saved grade progression matrix ({len(grade_df)} rows) to {grade_path}")
        
        # Save sector benchmark
        sector_path = os.path.join(self.processed_dir, "sector_equity_benchmark.csv")
        cas_df.to_csv(sector_path, index=False)
        print(f"-> Saved sector equity benchmark to {sector_path}")
        
        return {
            "master_timeseries": master_df,
            "grade_matrix": grade_df,
            "sector_benchmark": cas_df,
            "socioeconomic": socio_df
        }

if __name__ == "__main__":
    pipeline = DataPipeline()
    results = pipeline.process_and_save_all()
    print("Data pipeline executed successfully.")
