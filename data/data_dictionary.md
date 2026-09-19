# Data Dictionary: EduEquity LK

This document defines the schema, data sources, calculation methodologies, and descriptions for all raw and processed datasets used in the **EduEquity LK** data science project.

---

## 1. Raw Datasets (`data/raw/`)

### 1.1 `moe_school_census_2014_2024.csv`
* **Source:** Ministry of Education Sri Lanka (MOE) Statistics Branch, Annual School Census Reports (2014–2024) & Parliamentary Education Submissions (2024).
* **Granularity:** District-year level across 25 administrative districts over 11 years (2014–2024; $N = 275$).

| Column Name | Data Type | Range / Format | Description |
| :--- | :--- | :--- | :--- |
| `year` | Integer | 2014 – 2024 | Academic census enumeration year. |
| `province` | String | 9 provinces | Administrative province (Western, Central, Southern, Northern, Eastern, North Western, North Central, Uva, Sabaragamuwa). |
| `district` | String | 25 districts | Administrative district name. |
| `total_enrolment` | Integer | 25,000 – 400,000 | Total student enrolment across government and aided schools in the district. |
| `dropout_rate_pct` | Float | 0.0% – 10.0% | Percentage of enrolled students who discontinue education within the academic year. |
| `dropout_count` | Integer | 200 – 15,000 | Estimated count of dropouts ($\text{total\_enrolment} \times \frac{\text{dropout\_rate\_pct}}{100}$). |
| `male_dropout_rate_pct` | Float | 0.0% – 12.0% | Estimated male student dropout rate (reflects historical gender disparity in secondary grades). |
| `female_dropout_rate_pct` | Float | 0.0% – 10.0% | Estimated female student dropout rate. |
| `repetition_rate_pct` | Float | 0.0% – 5.0% | Percentage of students repeating the same grade level. |
| `retention_rate_g1_g9_pct` | Float | 50.0% – 100.0% | Cohort survival/retention rate from Grade 1 through Grade 9 (compulsory basic cycle). |
| `retention_rate_g1_g11_pct`| Float | 40.0% – 100.0% | Cohort survival/retention rate from Grade 1 through G.C.E. Ordinary Level (Grade 11). |

---

### 1.2 `moe_grade_progression_dropout.csv`
* **Source:** Ministry of Education Annual School Census tables & DCS School Progression Studies.
* **Granularity:** Grade-level (Grades 1 to 11) disaggregated by Urban, Rural, Estate, and National sectors.

| Column Name | Data Type | Range / Format | Description |
| :--- | :--- | :--- | :--- |
| `grade_level` | String | Grade 1 – Grade 11 | School curriculum grade level. |
| `grade_number` | Integer | 1 – 11 | Numerical grade indicator. |
| `stage` | String | Primary / Junior / Senior | Education stage category (Primary: 1–5, Junior Secondary: 6–9, Senior Secondary: 10–11). |
| `urban_dropout_rate_pct` | Float | 0.0% – 10.0% | Annual dropout rate for urban schools. |
| `rural_dropout_rate_pct` | Float | 0.0% – 12.0% | Annual dropout rate for rural schools. |
| `estate_dropout_rate_pct` | Float | 0.0% – 25.0% | Annual dropout rate for plantation/estate sector schools. |
| `national_avg_dropout_rate_pct` | Float | 0.0% – 15.0% | Island-wide weighted average dropout rate. |
| `estate_to_urban_disparity_ratio` | Float | $\ge 1.0$ | Ratio of Estate sector dropout rate to Urban sector dropout rate ($\frac{\text{Estate}}{\text{Urban}}$). |
| `estate_to_rural_disparity_ratio` | Float | $\ge 1.0$ | Ratio of Estate sector dropout rate to Rural sector dropout rate ($\frac{\text{Estate}}{\text{Rural}}$). |

---

### 1.3 `dcs_child_activity_survey_2016.csv`
* **Source:** Department of Census and Statistics Sri Lanka (DCS), *Child Activity Survey (CAS) Report 2016*.
* **Granularity:** Sector level (Urban, Rural, Estate) for children aged 5–17 years.

| Column Name | Data Type | Range / Format | Description |
| :--- | :--- | :--- | :--- |
| `sector` | String | Urban, Rural, Estate | Residential sector classification. |
| `child_population_5_17` | Integer | $\ge 100,000$ | Total estimated child population in the age group 5–17 years. |
| `currently_attending_school_pct` | Float | 0.0% – 100.0% | Percentage of children aged 5–17 currently attending regular school. |
| `not_attending_never_attended_pct` | Float | 0.0% – 100.0% | Out-of-school rate for children aged 5–17 years. |
| `economically_active_children_pct` | Float | 0.0% – 100.0% | Percentage of children engaged in economic activity. |
| `child_labour_rate_pct` | Float | 0.0% – 100.0% | Percentage of children engaged in child labour (below legal working age or hazardous hours). |
| `hazardous_child_labour_rate_pct` | Float | 0.0% – 100.0% | Percentage of children in hazardous employment conditions. |
| `reason_poverty_pct` | Float | 0.0% – 100.0% | Share of out-of-school children citing financial/economic constraints as primary reason. |
| `reason_school_distance_pct` | Float | 0.0% – 100.0% | Share citing transport/distance barriers to secondary schools. |
| `reason_family_assistance_pct` | Float | 0.0% – 100.0% | Share citing need to assist family business, agriculture, or caregiving. |
| `reason_disinterest_in_studies_pct` | Float | 0.0% – 100.0% | Share citing lack of interest or curriculum mismatch. |
| `reason_illness_disability_pct` | Float | 0.0% – 100.0% | Share citing chronic illness or physical/learning disabilities. |
| `avg_monthly_hh_income_lkr` | Float | Currency (LKR) | Mean monthly household income in 2016 Sri Lankan Rupees. |

---

### 1.4 `dcs_district_socioeconomic_indicators.csv`
* **Source:** DCS Household Income and Expenditure Survey (HIES 2016/2019/2022-23), Census of Population & Housing, and MOE School Infrastructure Database.
* **Granularity:** District level ($N = 25$).

| Column Name | Data Type | Range / Format | Description |
| :--- | :--- | :--- | :--- |
| `district` | String | 25 districts | Administrative district. |
| `province` | String | 9 provinces | Administrative province. |
| `poverty_headcount_pct` | Float | 1.0% – 25.0% | Official poverty headcount index (% population below national poverty line). |
| `estate_pop_pct` | Float | 0.0% – 60.0% | Percentage of district population residing within the plantation estate sector. |
| `median_hh_income_lkr` | Float | Currency (LKR) | Median monthly household income. |
| `pct_1ab_schools` | Float | 0.0% – 25.0% | Percentage of schools in the district offering Advanced Level (G.C.E. A/L) Science streams (Type 1AB). |
| `student_teacher_ratio` | Float | 10.0 – 30.0 | Ratio of enrolled students to active school teachers. |
| `pct_schools_with_computer_labs` | Float | 0.0% – 100.0% | Percentage of schools equipped with functional computer/digital labs. |
| `pct_schools_with_sanitation` | Float | 0.0% – 100.0% | Percentage of schools with adequate drinking water and sanitation facilities. |
| `pct_tamil_medium_schools` | Float | 0.0% – 100.0% | Percentage of schools instructing in Tamil medium (key equity metric for estate & northern/eastern zones). |
| `roads_access_index` | Float | 0 – 100 | Composite index of road connectivity and transport availability. |

---

### 1.5 `sri_lanka_districts.geojson`
* **Source:** geoBoundaries (geoBoundaries-LKA-ADM2) / UN OCHA Humanitarian Data Exchange (HDX).
* **Format:** GeoJSON FeatureCollection with 25 polygon/multipolygon geometries corresponding to Sri Lanka's administrative districts.

---

## 2. Processed Master Datasets (`data/processed/`)

### 2.1 `master_district_timeseries.csv`
Merged, cleaned multi-year panel dataset combining historical census dropout rates with district socioeconomic indicators, lagged crisis indicators, and vulnerability metrics.

### 2.2 `district_risk_scores.csv`
Machine-learning derived risk assessment table containing:
* `composite_risk_score`: Calibrated 0–100 risk score based on multi-factor regression and ensemble feature weighting.
* `risk_tier`: Categorical risk classification (*Low*, *Moderate*, *Elevated*, *Critical*).
* `primary_vulnerability_driver`: Dominant feature contributing to elevated dropout risk for each district.
* `shap_poverty_contrib`, `shap_estate_contrib`, `shap_school_density_contrib`: Explainability SHAP/feature contribution values.

### 2.3 `sector_equity_benchmark.csv`
Cleaned comparative benchmark dataset contrasting Urban, Rural, and Estate indicators across access, infrastructure, dropout, and household economics.
