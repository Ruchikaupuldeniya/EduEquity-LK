"""
EduEquity LK - Bilingual Localization (i18n) Engine
Supports seamless switching between English and Sinhala (සිංහල).
"""

from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "app_title": "EduEquity LK: School Dropout & Inequality Observatory",
        "app_subtitle": "Empirical analysis of school dropouts and regional disparities in Sri Lanka (2014–2024) with focus on the Estate (Tea Plantation) Sector vs. Urban & Rural Baselines.",
        "language_select": "Language / භාෂාව:",
        "controls_title": "Analysis Controls",
        "select_year": "Select Census Year:",
        "filter_province": "Filter by Province:",
        "all_provinces": "All Provinces",
        "select_district": "Select Target District for Deep Dive:",
        "kpi_national_rate": "National Dropout Rate ({year})",
        "kpi_total_dropouts": "Total Dropouts: {count:,} students",
        "kpi_estate_multiplier": "Estate Disparity Multiplier",
        "kpi_estate_vs_urban": "Estate: {estate:.2f}% vs Urban: {urban:.2f}%",
        "kpi_highest_risk": "Highest Risk District ({year})",
        "kpi_rate_prov": "Dropout Rate: {rate:.2f}% ({province})",
        "kpi_district_risk": "{district} Risk Score",
        "kpi_classification": "Classification: {tier}",
        
        # Tabs
        "tab_map": "🗺️ Geospatial Risk Map",
        "tab_trends": "📈 Time-Series Trends (2014–2024)",
        "tab_sectors": "☕ Estate vs. Urban/Rural Disparities",
        "tab_grades": "🧗 Grade Drop-Off Cliff",
        "tab_model": "🧠 Explainable Risk Diagnostic",
        "tab_simulator": "🎯 Policy Intervention Simulator",
        
        # Map tab
        "map_title": "Sri Lanka District Dropout Risk Map ({year})",
        "map_metric_select": "Select Map Display Metric:",
        "metric_dropout_rate": "Dropout Rate (%)",
        "metric_risk_score": "Composite Risk Score (0-100)",
        "metric_poverty": "Poverty Headcount (%)",
        "metric_estate_share": "Estate Pop Share (%)",
        "district_spotlight": "📍 District Spotlight: {district}",
        "annual_dropout_rate": "Annual Dropout Rate:",
        "estate_pop_share": "Estate Population Share:",
        "poverty_headcount": "Poverty Headcount Index:",
        "science_density": "1AB Science School Density:",
        "comp_lab_access": "Computer Lab Access:",
        "sanitation_access": "Adequate Sanitation:",
        "key_vulnerability_diagnostic": "Key Vulnerability Diagnostic:",
        "gender_disparity_title": "Gender Disparity in {district} (%)",
        "male_dropout": "Male",
        "female_dropout": "Female",
        
        # Trends Tab
        "trends_title": "Longitudinal Dropout Trends (2014–2024)",
        "trends_desc": "Explore annual dropout rates over the past decade. The 2022 economic crisis produced a sharp spike in student dropouts due to transport inflation and resource shortages.",
        "compare_districts_label": "Select Districts to Compare:",
        "national_avg": "National Average",
        "crisis_spike_annotation": "2022 Economic Crisis",
        "crisis_table_title": "💥 Economic Crisis Surge Analysis (2019 Pre-Crisis vs. 2022 Peak)",
        
        # Sectors Tab
        "sectors_title": "☕ The Estate Sector Divide: Estate vs. Urban vs. Rural",
        "sectors_desc": "Data from the DCS Child Activity Survey (CAS) reveals persistent structural gaps between plantation communities and urban/rural centers.",
        "school_attendance_rates": "School Attendance & Out-of-School Rates (%)",
        "attending_school": "Attending School",
        "out_of_school": "Out of School",
        "child_activity_rates": "Child Economic Activity & Labour Rates (%)",
        "economically_active": "Economically Active",
        "child_labour": "Child Labour",
        "hazardous_labour": "Hazardous Labour",
        "reasons_title": "Primary Reported Barriers to School Attendance (CAS)",
        
        # Grades Tab
        "grades_title": "🧗 The Grade-by-Grade Drop-Off Cliff",
        "grades_desc": "Dropout rates diverge sharply at Grade 5 (Scholarship Exam) and peak at Grade 10–11 (G.C.E. O/L). In the estate sector, 18.5% of Grade 11 students drop out annually.",
        
        # Model Tab
        "model_title": "🧠 Explainable Risk Scoring & Feature Drivers",
        "model_desc": "Using an explainable Random Forest & Ridge regression ensemble (R² = 0.987) to identify the root causes of district vulnerability.",
        "feature_importance_title": "Feature Importance Breakdown (% Variance Explained)",
        "model_diagnostic_district": "🎯 Model Diagnostic for {district}",
        "predicted_rate": "Predicted Annual Dropout Rate:",
        "actual_rate": "Actual Historical Mean Rate:",
        "top_vulnerable_title": "🏆 Top Most Vulnerable Districts in Sri Lanka:",
        
        # Simulator Tab
        "sim_title": "🎯 Interactive Policy Intervention Simulator (What-If Analysis)",
        "sim_desc": "Simulate student retention improvements by testing targeted investments in poverty alleviation, 1AB schools, and digital labs.",
        "sim_config_title": "🛠️ Configure Interventions for {district}",
        "sim_poverty_slider": "Poverty Reduction Safety Net (% reduction):",
        "sim_1ab_slider": "Additional 1AB Secondary Schools (% boost):",
        "sim_tech_slider": "Computer Lab & Digital Access (% boost):",
        "sim_projection_title": "📊 Simulated Impact Projection for {district}",
        "baseline_rate": "Baseline Rate",
        "projected_rate": "Projected Rate",
        "retained_students": "Retained Students / Year",
        "simulation_chart_title": "Dropout Rate Reduction Simulation ({district})",
        
        # Executive Briefing
        "briefing_title": "📝 Automated Policy Briefing (Executive Insight Generator)",
        "footer_text": "EduEquity LK Project • Built with Python, Streamlit, and Plotly • Open Data for Educational Justice in Sri Lanka",
        
        # Risk tiers
        "tier_critical": "Critical Risk",
        "tier_elevated": "Elevated Risk",
        "tier_moderate": "Moderate Risk",
        "tier_low": "Low Risk",
        
        # Sectors
        "sector_estate": "Estate Sector",
        "sector_rural": "Rural Sector",
        "sector_urban": "Urban Sector",
        "sector_national": "National Average"
    },
    
    "si": {
        "app_title": "EduEquity LK: පාසල් හැරයාම සහ අධ්‍යාපන විෂමතා නිරීක්ෂණාගාරය",
        "app_subtitle": "ශ්‍රී ලංකාවේ දිස්ත්‍රික්ක 25 හි පාසල් හැරයාමේ ප්‍රවණතා සහ කලාපීය විෂමතා පිළිබඳ දත්ත විශ්ලේෂණය (2014–2024) — වතු (තේ වගා) අංශය සහ නාගරික/ග්‍රාමීය අංශ සංසන්දනය.",
        "language_select": "Language / භාෂාව තෝරන්න:",
        "controls_title": "විශ්ලේෂණ පාලක",
        "select_year": "සංගණන වර්ෂය තෝරන්න:",
        "filter_province": "පළාත අනුව පෙරන්න:",
        "all_provinces": "සියලුම පළාත්",
        "select_district": "විශ්ලේෂණය සඳහා දිස්ත්‍රික්කය තෝරන්න:",
        "kpi_national_rate": "ජාතික පාසල් හැරයාමේ ප්‍රතිශතය ({year})",
        "kpi_total_dropouts": "මුළු පාසල් හැරගිය සිසුන්: {count:,}",
        "kpi_estate_multiplier": "වතු අංශයේ විෂමතා ගුණකය",
        "kpi_estate_vs_urban": "වතු: {estate:.2f}% සහ නාගරික: {urban:.2f}%",
        "kpi_highest_risk": "වැඩිම අවදානමක් ඇති දිස්ත්‍රික්කය ({year})",
        "kpi_rate_prov": "හැරයාමේ අනුපාතය: {rate:.2f}% ({province})",
        "kpi_district_risk": "{district} අවදානම් දර්ශකය",
        "kpi_classification": "වර්ගීකරණය: {tier}",
        
        # Tabs
        "tab_map": "🗺️ භූගෝලීය අවදානම් සිතියම",
        "tab_trends": "📈 කාල-ශ්‍රේණි ප්‍රවණතා (2014–2024)",
        "tab_sectors": "☕ වතු සහ නාගරික/ග්‍රාමීය විෂමතා",
        "tab_grades": "🧗 ශ්‍රේණි අනුව පාසල් හැරයාමේ ප්‍රපාතය",
        "tab_model": "🧠 පුරෝකථන අවදානම් විශ්ලේෂණය",
        "tab_simulator": "🎯 ප්‍රතිපත්තිමය මැදිහත්වීම් අනුකරණය (Simulator)",
        
        # Map tab
        "map_title": "ශ්‍රී ලංකා දිස්ත්‍රික් පාසල් හැරයාමේ අවදානම් සිතියම ({year})",
        "map_metric_select": "සිතියමේ පෙන්විය යුතු දර්ශකය තෝරන්න:",
        "metric_dropout_rate": "පාසල් හැරයාමේ ප්‍රතිශතය (%)",
        "metric_risk_score": "සමස්ත අවදානම් ලකුණු (0-100)",
        "metric_poverty": "දිළිඳුකමේ දර්ශකය (%)",
        "metric_estate_share": "වතු ජනගහන ප්‍රතිශතය (%)",
        "district_spotlight": "📍 දිස්ත්‍රික් දළ විශ්ලේෂණය: {district}",
        "annual_dropout_rate": "වාර්ෂික පාසල් හැරයාමේ අනුපාතය:",
        "estate_pop_share": "වතු ජනගහන ප්‍රතිශතය:",
        "poverty_headcount": "දිළිඳුකමේ ප්‍රතිශතය:",
        "science_density": "1AB විද්‍යා පාසල් ඝනත්වය:",
        "comp_lab_access": "පරිගණක විද්‍යාගාර පහසුකම්:",
        "sanitation_access": "ප්‍රමාණවත් සනීපාරක්ෂක පහසුකම්:",
        "key_vulnerability_diagnostic": "ප්‍රධාන අවදානම් සාධකය:",
        "gender_disparity_title": "{district} දිස්ත්‍රික්කයේ ස්ත්‍රී/පුරුෂ විෂමතාව (%)",
        "male_dropout": "පිරිමි",
        "female_dropout": "ගැහැණු",
        
        # Trends Tab
        "trends_title": "දිගුකාලීන පාසල් හැරයාමේ ප්‍රවණතා (2014–2024)",
        "trends_desc": "පසුගිය දශකය තුළ වාර්ෂික පාසල් හැරයාමේ වෙනස්වීම් පරීක්ෂා කරන්න. 2022 ආර්ථික අර්බුදයත් සමඟ ප්‍රවාහන ගාස්තු ඉහළ යාම සහ පාසල් උපකරණ හිඟවීම හේතුවෙන් පාසල් හැරයාමේ කැපී පෙනෙන වර්ධනයක් සිදුවිය.",
        "compare_districts_label": "සංසන්දනය සඳහා දිස්ත්‍රික්ක තෝරන්න:",
        "national_avg": "ජාතික සාමාන්‍යය",
        "crisis_spike_annotation": "2022 ආර්ථික අර්බුදය",
        "crisis_table_title": "💥 ආර්ථික අර්බුදයේ බලපෑම (2019 සාමාන්‍යය vs 2022 අර්බුද උච්චතම අවස්ථාව)",
        
        # Sectors Tab
        "sectors_title": "☕ වතු අංශයේ අධ්‍යාපනික පරතරය: වතු vs නාගරික vs ග්‍රාමීය",
        "sectors_desc": "ජනලේඛන හා සංඛ්‍යාලේඛන දෙපාර්තමේන්තුවේ ළමා ක්‍රියාකාරකම් සමීක්ෂණ (CAS) දත්ත මගින් වතුකරයේ දරුවන් මුහුණ දෙන ගැටලු පැහැදිලි කරයි.",
        "school_attendance_rates": "පාසල් පැමිණීමේ සහ පාසල් නොයන දරුවන්ගේ ප්‍රතිශත (%)",
        "attending_school": "පාසල් යන දරුවන්",
        "out_of_school": "පාසල් නොයන දරුවන්",
        "child_activity_rates": "ළමා ශ්‍රම සහ ආර්ථික ක්‍රියාකාරකම් අනුපාත (%)",
        "economically_active": "ආර්ථිකව සක්‍රීය දරුවන්",
        "child_labour": "ළමා ශ්‍රමිකයින්",
        "hazardous_labour": "අන්තරායකර ශ්‍රමය",
        "reasons_title": "පාසල් නොයෑමට ප්‍රධාන හේතු (CAS සමීක්ෂණය)",
        
        # Grades Tab
        "grades_title": "🧗 ශ්‍රේණි අනුව පාසල් හැරයාමේ ප්‍රපාතය",
        "grades_desc": "ප්‍රාථමික අංශයේ පාසල් පැමිණීම ඉහළ වුවද, 5 වසර ශිෂ්‍යත්වයෙන් පසු සහ 10–11 ශ්‍රේණි (අ.පො.ස සා/පෙළ) දී පාසල් හැරයාම ශීඝ්‍රයෙන් ඉහළ යයි. වතු අංශයේ 11 ශ්‍රේණියේදී 18.5% ක වාර්ෂික හැරයාමක් වාර්තා වේ.",
        
        # Model Tab
        "model_title": "🧠 පැහැදිලි කළ හැකි අවදානම් පුරෝකථන ආකෘතිය",
        "model_desc": "Random Forest සහ Ridge Regression ආකෘති (R² = 0.987) භාවිතයෙන් දිස්ත්‍රික්කවල පාසල් හැරයාමට බලපාන මූලික සමාජ-ආර්ථික සාධක හඳුනාගැනීම.",
        "feature_importance_title": "ප්‍රධාන බලපෑම්කාරී සාධකවල වැදගත්කම (%)",
        "model_diagnostic_district": "🎯 {district} දිස්ත්‍රික්කය පිළිබඳ ආදර්ශ විශ්ලේෂණය",
        "predicted_rate": "පුරෝකථනය කළ හැරයාමේ අනුපාතය:",
        "actual_rate": "සත්‍ය ඓතිහාසික සාමාන්‍ය අනුපාතය:",
        "top_vulnerable_title": "🏆 ශ්‍රී ලංකාවේ වැඩිම අධ්‍යාපනික අවදානමක් ඇති දිස්ත්‍රික්ක:",
        
        # Simulator Tab
        "sim_title": "🎯 ප්‍රතිපත්තිමය මැදිහත්වීම් අනුකරණය (What-If Analysis)",
        "sim_desc": "දිළිඳුකම අවම කිරීම, 1AB පාසල් ඉදිකිරීම සහ ඩිජිටල් පහසුකම් ලබාදීම මගින් පාසල් හැරයාම අඩුකරගත හැකි ආකාරය ගණනය කරන්න.",
        "sim_config_title": "🛠️ {district} සඳහා ප්‍රතිපත්ති සැකසුම්",
        "sim_poverty_slider": "දිළිඳුකම අවම කිරීමේ වැඩසටහන් (% අඩු කිරීම):",
        "sim_1ab_slider": "අතිරේක 1AB උසස් පෙළ විද්‍යා පාසල් ප්‍රතිශතය (%):",
        "sim_tech_slider": "පරිගණක විද්‍යාගාර සහ ඩිජිටල් පහසුකම් (% වැඩිවීම):",
        "sim_projection_title": "📊 {district} සඳහා අපේක්ෂිත ප්‍රතිඵල",
        "baseline_rate": "වත්මන් අනුපාතය",
        "projected_rate": "අපේක්ෂිත අනුපාතය",
        "retained_students": "වසරකට රඳවාගත හැකි සිසුන් සංඛ්‍යාව",
        "simulation_chart_title": "පාසල් හැරයාම අවම කිරීමේ ප්‍රතිඵල සංසන්දනය ({district})",
        
        # Executive Briefing
        "briefing_title": "📝 ස්වයංක්‍රීය විධායක ප්‍රතිපත්ති වාර්තාව (Executive Briefing)",
        "footer_text": "EduEquity LK ව්‍යාපෘතිය • Python, Streamlit, සහ Plotly භාවිතයෙන් නිර්මාණය කරන ලදී • ශ්‍රී ලංකාවේ අධ්‍යාපනික සමානාත්මතාවය සඳහා විවෘත දත්ත",
        
        # Risk tiers
        "tier_critical": "අධි අවදානම්",
        "tier_elevated": "ඉහළ අවදානම්",
        "tier_moderate": "මධ්‍යම අවදානම්",
        "tier_low": "අඩු අවදානම්",
        
        # Sectors
        "sector_estate": "වතු අංශය",
        "sector_rural": "ග්‍රාමීය අංශය",
        "sector_urban": "නාගරික අංශය",
        "sector_national": "ජාතික සාමාන්‍යය"
    }
}

DISTRICT_NAMES_SINHALA = {
    "Colombo": "කොළඹ",
    "Gampaha": "ගම්පහ",
    "Kalutara": "කළුතර",
    "Kandy": "මහනුවර",
    "Matale": "මාතලේ",
    "Nuwara Eliya": "නුවරඑළිය",
    "Galle": "ගාල්ල",
    "Matara": "මාතර",
    "Hambantota": "හම්බන්තොට",
    "Jaffna": "යාපනය",
    "Kilinochchi": "කිලිනොච්චිය",
    "Mannar": "මන්නාරම",
    "Vavuniya": "වවුනියාව",
    "Mullaitivu": "මුලතිව්",
    "Batticaloa": "මඩකලපුව",
    "Ampara": "අම්පාර",
    "Trincomalee": "ත්‍රිකුණාමලය",
    "Kurunegala": "කුරුණෑගල",
    "Puttalam": "පුත්තලම",
    "Anuradhapura": "අනුරාධපුරය",
    "Polonnaruwa": "පොළොන්නරුව",
    "Badulla": "බදුල්ල",
    "Monaragala": "මොණරාගල",
    "Ratnapura": "රත්නපුරය",
    "Kegalle": "කෑගල්ල"
}

PROVINCE_NAMES_SINHALA = {
    "Western": "බස්නාහිර",
    "Central": "මධ්‍යම",
    "Southern": "දකුණ",
    "Northern": "උතුර",
    "Eastern": "නැගෙනහිර",
    "North Western": "වයඹ",
    "North Central": "උතුරු මැද",
    "Uva": "ඌව",
    "Sabaragamuwa": "සබරගමුව"
}

def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translates a localized string key and interpolates format variables."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    template = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template

def get_localized_district(name: str, lang: str = "en") -> str:
    """Returns the localized district name."""
    if lang == "si":
        return DISTRICT_NAMES_SINHALA.get(name, name)
    return name

def get_localized_province(name: str, lang: str = "en") -> str:
    """Returns the localized province name."""
    if lang == "si":
        return PROVINCE_NAMES_SINHALA.get(name, name)
    return name

def get_localized_risk_tier(tier: str, lang: str = "en") -> str:
    """Translates risk tier classifications."""
    if lang == "si":
        mapping = {
            "Critical Risk": "අධි අවදානම්",
            "Elevated Risk": "ඉහළ අවදානම්",
            "Moderate Risk": "මධ්‍යම අවදානම්",
            "Low Risk": "අඩු අවදානම්"
        }
        return mapping.get(tier, tier)
    return tier
