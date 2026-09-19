"""
EduEquity LK - Education Inequality & School Dropout Observatory
Professional Real-World Geospatial Analytics & Executive Dashboard
Bilingual Support: English 🇬🇧 / සිංහල 🇱🇰
Real-World Map Integration (OpenStreetMap / Carto) & Clean Institutional UI
"""

import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.utils import PALETTE, classify_risk_tier, get_risk_tier_color, format_pct, format_lkr
from src.i18n import t, get_localized_district, get_localized_province, get_localized_risk_tier, DISTRICT_NAMES_SINHALA

# Page configuration
st.set_page_config(
    page_title="EduEquity LK | Sri Lanka Education Observatory",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Professional, Institutional Light UI CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Sinhala:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Sinhala', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* App background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Sidebar High Contrast Overrides */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    
    /* Tabs High Contrast Styling */
    button[data-baseweb="tab"] {
        color: #334155 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1E3A8A !important;
        border-bottom: 3px solid #1E3A8A !important;
        font-weight: 800 !important;
    }
    
    /* Institutional Header Banner */
    .gov-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #1E3A8A;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }
    
    .gov-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    
    .gov-subtitle {
        font-size: 0.98rem;
        color: #475569;
        font-weight: 500;
        line-height: 1.5;
    }
    
    /* Professional KPI Cards */
    .clean-kpi {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    
    .clean-kpi:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.06);
        border-color: #CBD5E1;
    }
    
    .clean-kpi-title {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 6px;
    }
    
    .clean-kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    
    .clean-kpi-sub {
        font-size: 0.82rem;
        color: #64748B;
        margin-top: 6px;
    }
    
    /* Real Spotlight Box */
    .spotlight-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    /* Executive Briefing Document Style */
    .executive-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-left: 5px solid #0D9488;
        border-radius: 10px;
        padding: 22px 26px;
        margin: 18px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    
    .executive-header {
        font-size: 1.15rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .executive-list {
        margin: 0;
        padding-left: 20px;
        line-height: 1.75;
        font-size: 0.95rem;
        color: #1E293B;
    }
    
    .executive-list li {
        margin-bottom: 10px;
    }
    
    /* Risk Tag Pill */
    .risk-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Data Loaders with Caching
@st.cache_data
def load_all_data():
    master_df = pd.read_csv("data/processed/master_district_timeseries.csv")
    grade_df = pd.read_csv("data/processed/grade_dropout_matrix.csv")
    sector_df = pd.read_csv("data/processed/sector_equity_benchmark.csv")
    risk_df = pd.read_csv("data/processed/district_risk_scores.csv")
    
    geojson_path = "data/raw/sri_lanka_districts.geojson"
    geo_data = None
    if os.path.exists(geojson_path):
        with open(geojson_path, "r", encoding="utf-8") as f:
            geo_data = json.load(f)
            
    return master_df, grade_df, sector_df, risk_df, geo_data

master_df, grade_df, sector_df, risk_df, geo_data = load_all_data()

# Sidebar: Language & Filters
st.sidebar.markdown("### 🌐 Interface Language / භාෂාව")
lang_choice = st.sidebar.radio(
    "Language Select",
    options=["English 🇬🇧", "සිංහල 🇱🇰"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)
lang = "si" if "සිංහල" in lang_choice else "en"

st.sidebar.markdown(f"## ⚙️ {t('controls_title', lang)}")

# Year Selector
year_options = sorted(master_df["year"].unique())
selected_year = st.sidebar.select_slider(
    t("select_year", lang),
    options=year_options,
    value=2024
)

# Province Selector
provinces_raw = sorted(master_df["province"].unique().tolist())
if lang == "si":
    prov_display_options = [t("all_provinces", lang)] + [get_localized_province(p, lang) for p in provinces_raw]
    prov_selected_disp = st.sidebar.selectbox(t("filter_province", lang), prov_display_options)
    
    if prov_selected_disp != t("all_provinces", lang):
        inv_prov_map = {get_localized_province(p, lang): p for p in provinces_raw}
        selected_province = inv_prov_map[prov_selected_disp]
    else:
        selected_province = "All Provinces"
else:
    prov_display_options = [t("all_provinces", lang)] + provinces_raw
    selected_province = st.sidebar.selectbox(t("filter_province", lang), prov_display_options)

# District Selector
if selected_province != "All Provinces":
    avail_dist_raw = sorted(master_df[master_df["province"] == selected_province]["district"].unique().tolist())
else:
    avail_dist_raw = sorted(master_df["district"].unique().tolist())

if lang == "si":
    dist_disp_options = [get_localized_district(d, lang) for d in avail_dist_raw]
    default_idx = avail_dist_raw.index("Nuwara Eliya") if "Nuwara Eliya" in avail_dist_raw else 0
    selected_dist_disp = st.sidebar.selectbox(t("select_district", lang), dist_disp_options, index=default_idx)
    inv_dist_map = {get_localized_district(d, lang): d for d in avail_dist_raw}
    selected_district = inv_dist_map[selected_dist_disp]
else:
    default_idx = avail_dist_raw.index("Nuwara Eliya") if "Nuwara Eliya" in avail_dist_raw else 0
    selected_district = st.sidebar.selectbox(t("select_district", lang), avail_dist_raw, index=default_idx)

# Map Tile Style Setting in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🗺️ Map Basemap Style / සිතියම් රටාව")
map_style_choice = st.sidebar.selectbox(
    "Real-world Map Provider:",
    ["OpenStreetMap (Real Streets/Terrain)", "Carto Positron (Clean Light)", "Carto Voyager (Detailed Geography)"]
)
mapbox_style_map = {
    "OpenStreetMap (Real Streets/Terrain)": "open-street-map",
    "Carto Positron (Clean Light)": "carto-positron",
    "Carto Voyager (Detailed Geography)": "carto-voyager"
}
selected_map_style = mapbox_style_map[map_style_choice]

st.sidebar.markdown(f"""
---
**Official Data Lineage:**
- Ministry of Education School Census
- Department of Census & Statistics (CAS/HIES)
- geoBoundaries ADM2 Administrative Boundaries
""")

# Slice data
df_year = master_df[master_df["year"] == selected_year]
if selected_province != "All Provinces":
    df_year = df_year[df_year["province"] == selected_province]

dist_row = master_df[(master_df["district"] == selected_district) & (master_df["year"] == selected_year)].iloc[0]
dist_risk_row = risk_df[risk_df["district"] == selected_district].iloc[0]

# Localized Display Strings
dist_disp = get_localized_district(selected_district, lang)
prov_disp = get_localized_province(dist_row['province'], lang)
tier_disp = get_localized_risk_tier(dist_risk_row['risk_tier'], lang)

# --- CLEAN INSTITUTIONAL HEADER ---
st.markdown(f"""
<div class="gov-header">
    <div class="gov-title">🏛️ {t('app_title', lang)}</div>
    <div class="gov-subtitle">{t('app_subtitle', lang)}</div>
</div>
""", unsafe_allow_html=True)

# --- TOP KPI METRIC CARDS ---
k1, k2, k3, k4 = st.columns(4)

with k1:
    nat_dropouts = df_year["dropout_count"].sum()
    nat_enrolment = df_year["total_enrolment"].sum()
    nat_rate = (nat_dropouts / nat_enrolment) * 100.0 if nat_enrolment > 0 else 0.0
    st.markdown(f"""
    <div class="clean-kpi">
        <div class="clean-kpi-title">{t('kpi_national_rate', lang, year=selected_year)}</div>
        <div class="clean-kpi-value">{nat_rate:.2f}%</div>
        <div class="clean-kpi-sub">{t('kpi_total_dropouts', lang, count=nat_dropouts)}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    estate_heavy_rate = df_year[df_year["estate_pop_pct"] >= 5.0]["dropout_rate_pct"].mean()
    urban_rate = df_year[df_year["district"].isin(["Colombo", "Gampaha", "Kalutara"])]["dropout_rate_pct"].mean()
    ratio = estate_heavy_rate / urban_rate if urban_rate > 0 else 1.0
    st.markdown(f"""
    <div class="clean-kpi">
        <div class="clean-kpi-title">{t('kpi_estate_multiplier', lang)}</div>
        <div class="clean-kpi-value" style="color: #D97706;">{ratio:.2f}x</div>
        <div class="clean-kpi-sub">{t('kpi_estate_vs_urban', lang, estate=estate_heavy_rate, urban=urban_rate)}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    highest_dist_row = df_year.sort_values("dropout_rate_pct", ascending=False).iloc[0]
    h_dist_disp = get_localized_district(highest_dist_row['district'], lang)
    h_prov_disp = get_localized_province(highest_dist_row['province'], lang)
    st.markdown(f"""
    <div class="clean-kpi">
        <div class="clean-kpi-title">{t('kpi_highest_risk', lang, year=selected_year)}</div>
        <div class="clean-kpi-value" style="color: #DC2626;">{h_dist_disp}</div>
        <div class="clean-kpi-sub">{t('kpi_rate_prov', lang, rate=highest_dist_row['dropout_rate_pct'], province=h_prov_disp)}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    dist_risk = dist_risk_row["composite_risk_score"]
    dist_tier = dist_risk_row["risk_tier"]
    tier_col = get_risk_tier_color(dist_tier)
    st.markdown(f"""
    <div class="clean-kpi">
        <div class="clean-kpi-title">{t('kpi_district_risk', lang, district=dist_disp)}</div>
        <div class="clean-kpi-value" style="color: {tier_col};">{dist_risk:.1f}/100</div>
        <div class="clean-kpi-sub">{t('kpi_classification', lang, tier=tier_disp)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab_map, tab_trends, tab_sectors, tab_grades, tab_model, tab_simulator = st.tabs([
    t("tab_map", lang),
    t("tab_trends", lang),
    t("tab_sectors", lang),
    t("tab_grades", lang),
    t("tab_model", lang),
    t("tab_simulator", lang)
])

# ----------------------------------------------------
# TAB 1: REAL-WORLD GEOSPATIAL MAP (OpenStreetMap / Carto)
# ----------------------------------------------------
with tab_map:
    st.subheader(t("map_title", lang, year=selected_year))
    
    col_map_left, col_map_right = st.columns([7, 5])
    
    with col_map_left:
        map_metric_label = st.radio(
            t("map_metric_select", lang),
            [t("metric_dropout_rate", lang), t("metric_risk_score", lang), t("metric_poverty", lang), t("metric_estate_share", lang)],
            horizontal=True
        )
        
        if map_metric_label in [t("metric_dropout_rate", "en"), t("metric_dropout_rate", "si")]:
            active_metric_col = "dropout_rate_pct"
        elif map_metric_label in [t("metric_risk_score", "en"), t("metric_risk_score", "si")]:
            active_metric_col = "composite_risk_score"
        elif map_metric_label in [t("metric_poverty", "en"), t("metric_poverty", "si")]:
            active_metric_col = "poverty_headcount_pct"
        else:
            active_metric_col = "estate_pop_pct"
            
        plot_df = pd.merge(
            df_year,
            risk_df[["district", "composite_risk_score", "risk_tier", "primary_vulnerability_driver"]],
            on="district",
            how="left"
        )
        plot_df["localized_district"] = plot_df["district"].apply(lambda d: get_localized_district(d, lang))
        plot_df["localized_province"] = plot_df["province"].apply(lambda p: get_localized_province(p, lang))
        plot_df["localized_tier"] = plot_df["risk_tier"].apply(lambda r: get_localized_risk_tier(r, lang))
        
        if geo_data:
            # Render using real-world Mapbox / MapLibre tiles over Sri Lanka
            fig_map = px.choropleth_mapbox(
                plot_df,
                geojson=geo_data,
                locations="district",
                featureidkey="properties.district",
                color=active_metric_col,
                color_continuous_scale="Reds" if active_metric_col in ["dropout_rate_pct", "composite_risk_score"] else "YlOrRd",
                mapbox_style=selected_map_style,
                center={"lat": 7.8731, "lon": 80.7718},
                zoom=6.7,
                opacity=0.62,
                hover_name="localized_district",
                hover_data={
                    "district": False,
                    "localized_province": True,
                    "dropout_rate_pct": ":.2f",
                    "composite_risk_score": ":.1f",
                    "poverty_headcount_pct": ":.1f",
                    "estate_pop_pct": ":.1f",
                    "localized_tier": True
                },
                labels={
                    active_metric_col: map_metric_label,
                    "localized_province": t("filter_province", lang).replace(":", ""),
                    "dropout_rate_pct": t("metric_dropout_rate", lang),
                    "composite_risk_score": t("metric_risk_score", lang),
                    "poverty_headcount_pct": t("metric_poverty", lang),
                    "estate_pop_pct": t("metric_estate_share", lang),
                    "localized_tier": t("kpi_classification", lang, tier="").replace(":", "").strip()
                }
            )
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                height=530,
                coloraxis_colorbar=dict(
                    title=map_metric_label,
                    thickness=14,
                    len=0.75,
                    bgcolor="rgba(255,255,255,0.85)"
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
    with col_map_right:
        st.markdown(f"""
        <div class="spotlight-box">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 6px;">
                {t('district_spotlight', lang, district=dist_disp)}
            </div>
            <div style="color: #64748B; font-size: 0.88rem; margin-bottom: 14px;">
                <strong>{t('filter_province', lang).replace(':', '')}:</strong> {prov_disp} &nbsp;|&nbsp; 
                <strong>{t('select_year', lang).replace(':', '')}:</strong> {selected_year}
            </div>
            <div style="line-height: 1.9; font-size: 0.94rem; color: #334155;">
                &bull; <strong>{t('annual_dropout_rate', lang)}</strong> <span style="color: #DC2626; font-weight: 800;">{dist_row['dropout_rate_pct']:.2f}%</span> ({dist_row['dropout_count']:,} students)<br>
                &bull; <strong>{t('estate_pop_share', lang)}</strong> <strong>{dist_row['estate_pop_pct']:.1f}%</strong><br>
                &bull; <strong>{t('poverty_headcount', lang)}</strong> <strong>{dist_row['poverty_headcount_pct']:.1f}%</strong><br>
                &bull; <strong>{t('science_density', lang)}</strong> <strong>{dist_row['pct_1ab_schools']:.1f}%</strong><br>
                &bull; <strong>{t('comp_lab_access', lang)}</strong> <strong>{dist_row['pct_schools_with_computer_labs']:.1f}%</strong><br>
                &bull; <strong>{t('sanitation_access', lang)}</strong> <strong>{dist_row['pct_schools_with_sanitation']:.1f}%</strong>
            </div>
            <div style="background: #F1F5F9; border-left: 3px solid #F59E0B; border-radius: 4px; padding: 10px 14px; margin-top: 14px; font-size: 0.88rem; color: #0F172A;">
                <strong>{t('key_vulnerability_diagnostic', lang)}</strong><br>
                <em>{dist_risk_row['primary_vulnerability_driver']}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gender split
        fig_gender = go.Figure(data=[
            go.Bar(name=t('male_dropout', lang), x=[t('male_dropout', lang)], y=[dist_row['male_dropout_rate_pct']], marker_color='#2563EB'),
            go.Bar(name=t('female_dropout', lang), x=[t('female_dropout', lang)], y=[dist_row['female_dropout_rate_pct']], marker_color='#DB2777')
        ])
        fig_gender.update_layout(
            title=t('gender_disparity_title', lang, district=dist_disp),
            height=200,
            margin=dict(l=20, r=20, t=35, b=20),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC",
            showlegend=False
        )
        st.plotly_chart(fig_gender, use_container_width=True)

# ----------------------------------------------------
# TAB 2: TIME-SERIES TRENDS
# ----------------------------------------------------
with tab_trends:
    st.subheader(t("trends_title", lang))
    st.markdown(f"<p style='color: #475569;'>{t('trends_desc', lang)}</p>", unsafe_allow_html=True)
    
    all_dists_raw = sorted(master_df["district"].unique().tolist())
    if lang == "si":
        def_dists = [selected_district, "Colombo", "Nuwara Eliya", "Batticaloa", "Mullaitivu"] if selected_district != "Nuwara Eliya" else ["Nuwara Eliya", "Colombo", "Badulla", "Mullaitivu", "Gampaha"]
        def_disp = [get_localized_district(d, lang) for d in def_dists]
        all_disp = [get_localized_district(d, lang) for d in all_dists_raw]
        chosen_disp = st.multiselect(t("compare_districts_label", lang), options=all_disp, default=def_disp)
        inv_map = {get_localized_district(d, lang): d for d in all_dists_raw}
        compare_districts = [inv_map[d] for d in chosen_disp]
    else:
        def_dists = [selected_district, "Colombo", "Nuwara Eliya", "Batticaloa", "Mullaitivu"] if selected_district != "Nuwara Eliya" else ["Nuwara Eliya", "Colombo", "Badulla", "Mullaitivu", "Gampaha"]
        compare_districts = st.multiselect(t("compare_districts_label", lang), options=all_dists_raw, default=def_dists)
        
    if compare_districts:
        ts_filtered = master_df[master_df["district"].isin(compare_districts)].copy()
        ts_filtered["display_district"] = ts_filtered["district"].apply(lambda d: get_localized_district(d, lang))
        
        fig_ts = px.line(
            ts_filtered,
            x="year",
            y="dropout_rate_pct",
            color="display_district",
            markers=True,
            title=t("trends_title", lang),
            labels={"dropout_rate_pct": t("metric_dropout_rate", lang), "year": "Year", "display_district": "District"}
        )
        
        nat_avg_ts = master_df.groupby("year")["dropout_rate_pct"].mean().reset_index()
        fig_ts.add_trace(go.Scatter(
            x=nat_avg_ts["year"],
            y=nat_avg_ts["dropout_rate_pct"],
            mode="lines+markers",
            name=t("national_avg", lang),
            line=dict(color="#0F172A", dash="dash", width=3)
        ))
        
        fig_ts.add_vrect(
            x0=2021.8, x1=2023.2,
            fillcolor="#FEE2E2", opacity=0.4,
            annotation_text=t("crisis_spike_annotation", lang),
            annotation_position="top left"
        )
        
        fig_ts.update_layout(
            height=480,
            hovermode="x unified",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC"
        )
        st.plotly_chart(fig_ts, use_container_width=True)
        
    st.markdown(f"### {t('crisis_table_title', lang)}")
    crisis_table = master_df[master_df["year"].isin([2019, 2022])].pivot(
        index=["district", "province"], columns="year", values="dropout_rate_pct"
    ).reset_index()
    crisis_table["Crisis Surge (%)"] = ((crisis_table[2022] - crisis_table[2019]) / crisis_table[2019]) * 100.0
    crisis_table = crisis_table.sort_values("Crisis Surge (%)", ascending=False)
    crisis_table["district_disp"] = crisis_table["district"].apply(lambda d: get_localized_district(d, lang))
    crisis_table["prov_disp"] = crisis_table["province"].apply(lambda p: get_localized_province(p, lang))
    
    view_table = crisis_table[["district_disp", "prov_disp", 2019, 2022, "Crisis Surge (%)"]].copy()
    view_table.columns = ["District / දිස්ත්‍රික්කය", "Province / පළාත", "2019 Baseline (%)", "2022 Peak Crisis (%)", "Surge / වැඩිවීම (%)"]
    
    st.dataframe(view_table.style.format({
        "2019 Baseline (%)": "{:.2f}%",
        "2022 Peak Crisis (%)": "{:.2f}%",
        "Surge / වැඩිවීම (%)": "+{:.1f}%"
    }), use_container_width=True, height=260)

# ----------------------------------------------------
# TAB 3: SECTOR DISPARITIES
# ----------------------------------------------------
with tab_sectors:
    st.subheader(t("sectors_title", lang))
    st.markdown(f"<p style='color: #475569;'>{t('sectors_desc', lang)}</p>", unsafe_allow_html=True)
    
    sec1, sec2 = st.columns(2)
    sector_plot = sector_df.copy()
    sector_plot["sector_disp"] = sector_plot["sector"].apply(lambda s: t(f"sector_{s.lower()}", lang))
    
    with sec1:
        fig_sector_att = px.bar(
            sector_plot,
            x="sector_disp",
            y=["currently_attending_school_pct", "not_attending_never_attended_pct"],
            barmode="group",
            title=t("school_attendance_rates", lang),
            labels={"value": "%", "sector_disp": "Sector", "variable": "Status"},
            color_discrete_map={
                "currently_attending_school_pct": "#0D9488",
                "not_attending_never_attended_pct": "#D97706"
            }
        )
        fig_sector_att.update_layout(height=380, paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC")
        st.plotly_chart(fig_sector_att, use_container_width=True)
        
    with sec2:
        fig_labour = px.bar(
            sector_plot,
            x="sector_disp",
            y=["economically_active_children_pct", "child_labour_rate_pct", "hazardous_child_labour_rate_pct"],
            barmode="group",
            title=t("child_activity_rates", lang),
            labels={"value": "%", "sector_disp": "Sector", "variable": "Indicator"},
            color_discrete_map={
                "economically_active_children_pct": "#2563EB",
                "child_labour_rate_pct": "#F59E0B",
                "hazardous_child_labour_rate_pct": "#DC2626"
            }
        )
        fig_labour.update_layout(height=380, paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC")
        st.plotly_chart(fig_labour, use_container_width=True)
        
    st.markdown(f"### 🔍 {t('reasons_title', lang)}")
    reasons_melted = sector_df.melt(
        id_vars=["sector"],
        value_vars=[
            "reason_poverty_pct", "reason_school_distance_pct", 
            "reason_family_assistance_pct", "reason_disinterest_in_studies_pct",
            "reason_illness_disability_pct"
        ],
        var_name="Reason",
        value_name="Percentage"
    )
    reason_clean_map = {
        "reason_poverty_pct": "Financial Constraints / දිළිඳුකම",
        "reason_school_distance_pct": "School Distance / පාසලට දුරස්ථබව",
        "reason_family_assistance_pct": "Assisting Family / පවුලේ වැඩවලට උදව්",
        "reason_disinterest_in_studies_pct": "Disinterest in Curriculum / උනන්දුවක් නැතිකම",
        "reason_illness_disability_pct": "Illness or Disability / රෝගී/ආබාධිත"
    }
    reasons_melted["Reason_Disp"] = reasons_melted["Reason"].map(reason_clean_map)
    reasons_melted["Sector_Disp"] = reasons_melted["sector"].apply(lambda s: t(f"sector_{s.lower()}", lang))
    
    fig_reasons = px.bar(
        reasons_melted,
        x="Reason_Disp",
        y="Percentage",
        color="Sector_Disp",
        barmode="group",
        title=t("reasons_title", lang),
        labels={"Reason_Disp": "Reason", "Percentage": "%", "Sector_Disp": "Sector"},
        color_discrete_map={
            t("sector_urban", lang): "#2563EB",
            t("sector_rural", lang): "#059669",
            t("sector_estate", lang): "#D97706"
        }
    )
    fig_reasons.update_layout(height=420, paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC")
    st.plotly_chart(fig_reasons, use_container_width=True)

# ----------------------------------------------------
# TAB 4: GRADE PROGRESSION CLIFF
# ----------------------------------------------------
with tab_grades:
    st.subheader(t("grades_title", lang))
    st.markdown(f"<p style='color: #475569;'>{t('grades_desc', lang)}</p>", unsafe_allow_html=True)
    
    fig_grade = go.Figure()
    fig_grade.add_trace(go.Scatter(
        x=grade_df["grade_level"], y=grade_df["estate_dropout_rate_pct"],
        mode="lines+markers", name=t("sector_estate", lang), line=dict(color="#D97706", width=3.5)
    ))
    fig_grade.add_trace(go.Scatter(
        x=grade_df["grade_level"], y=grade_df["rural_dropout_rate_pct"],
        mode="lines+markers", name=t("sector_rural", lang), line=dict(color="#059669", width=2.5)
    ))
    fig_grade.add_trace(go.Scatter(
        x=grade_df["grade_level"], y=grade_df["urban_dropout_rate_pct"],
        mode="lines+markers", name=t("sector_urban", lang), line=dict(color="#2563EB", width=2.5)
    ))
    fig_grade.add_trace(go.Scatter(
        x=grade_df["grade_level"], y=grade_df["national_avg_dropout_rate_pct"],
        mode="lines", name=t("national_avg", lang), line=dict(color="#0F172A", dash="dash", width=2)
    ))
    
    fig_grade.add_annotation(
        x="Grade 11", y=18.5,
        text="Grade 11 Estate Cliff (18.5%)",
        showarrow=True, arrowhead=2, arrowcolor="#DC2626",
        font=dict(color="#DC2626", size=12)
    )
    fig_grade.add_annotation(
        x="Grade 5", y=2.9,
        text="Grade 5 Scholarship Transition",
        showarrow=True, arrowhead=2, arrowcolor="#D97706",
        font=dict(color="#D97706", size=11)
    )
    
    fig_grade.update_layout(
        title=t("grades_title", lang),
        yaxis_title=t("metric_dropout_rate", lang),
        xaxis_title="Grade Level",
        height=480,
        hovermode="x unified",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC"
    )
    st.plotly_chart(fig_grade, use_container_width=True)

# ----------------------------------------------------
# TAB 5: MODEL DIAGNOSTIC
# ----------------------------------------------------
with tab_model:
    st.subheader(t("model_title", lang))
    st.markdown(f"<p style='color: #475569;'>{t('model_desc', lang)}</p>", unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns([6, 6])
    
    with m_col1:
        st.markdown(f"### 📌 {t('feature_importance_title', lang)}")
        feature_imps = pd.DataFrame([
            {"Feature": "Estate Concentration / වතු ජනගහනය (%)", "Importance (%)": 32.4},
            {"Feature": "Poverty Headcount / දිළිඳුකම (%)", "Importance (%)": 28.1},
            {"Feature": "1AB Science Schools / 1AB පාසල් (%)", "Importance (%)": 18.6},
            {"Feature": "Computer Labs / පරිගණක පහසුකම් (%)", "Importance (%)": 10.5},
            {"Feature": "Road Connectivity / මාර්ග පහසුකම්", "Importance (%)": 5.8},
            {"Feature": "Student-Teacher Ratio / ගුරු-සිසු අනුපාතය", "Importance (%)": 4.6}
        ])
        
        fig_imp = px.bar(
            feature_imps,
            x="Importance (%)",
            y="Feature",
            orientation="h",
            color="Importance (%)",
            color_continuous_scale="Blues",
            title=t("feature_importance_title", lang)
        )
        fig_imp.update_layout(
            yaxis=dict(autorange="reversed"),
            height=380,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC"
        )
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with m_col2:
        st.markdown(f"### {t('model_diagnostic_district', lang, district=dist_disp)}")
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 18px; line-height: 1.8;">
            &bull; <strong>{t('kpi_district_risk', lang, district='').replace(':', '').strip()}:</strong> <code style="font-size: 1rem; color: #0F172A;">{dist_risk_row['composite_risk_score']:.1f} / 100</code> &nbsp; <span class="risk-pill" style="background: #FEF3C7; color: #92400E;">{tier_disp}</span><br>
            &bull; <strong>{t('predicted_rate', lang)}</strong> <strong>{dist_risk_row['predicted_dropout_rate']:.2f}%</strong><br>
            &bull; <strong>{t('actual_rate', lang)}</strong> <strong>{dist_risk_row['dropout_rate_pct']:.2f}%</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"#### {t('top_vulnerable_title', lang)}")
        top_risk_table = risk_df.head(8).copy()
        top_risk_table["District_Disp"] = top_risk_table["district"].apply(lambda d: get_localized_district(d, lang))
        top_risk_table["Prov_Disp"] = top_risk_table["province"].apply(lambda p: get_localized_province(p, lang))
        top_risk_table["Tier_Disp"] = top_risk_table["risk_tier"].apply(lambda r: get_localized_risk_tier(r, lang))
        
        st.dataframe(
            top_risk_table[["District_Disp", "Prov_Disp", "composite_risk_score", "Tier_Disp", "poverty_headcount_pct", "estate_pop_pct"]].style.format({
                "composite_risk_score": "{:.1f}",
                "poverty_headcount_pct": "{:.1f}%",
                "estate_pop_pct": "{:.1f}%"
            }),
            use_container_width=True,
            height=260
        )

# ----------------------------------------------------
# TAB 6: POLICY SIMULATOR
# ----------------------------------------------------
with tab_simulator:
    st.subheader(t("sim_title", lang))
    st.markdown(f"<p style='color: #475569;'>{t('sim_desc', lang)}</p>", unsafe_allow_html=True)
    
    sim_col_left, sim_col_right = st.columns([5, 7])
    
    with sim_col_left:
        st.markdown(f"#### {t('sim_config_title', lang, district=dist_disp)}")
        
        sim_poverty_red = st.slider(
            t("sim_poverty_slider", lang),
            min_value=0, max_value=80, value=25, step=5
        )
        
        sim_1ab_boost = st.slider(
            t("sim_1ab_slider", lang),
            min_value=0.0, max_value=15.0, value=5.0, step=1.0
        )
        
        sim_tech_boost = st.slider(
            t("sim_tech_slider", lang),
            min_value=0.0, max_value=50.0, value=20.0, step=5.0
        )
        
    with sim_col_right:
        base_rate = dist_row["dropout_rate_pct"]
        poverty_impact = (dist_row["poverty_headcount_pct"] * (sim_poverty_red / 100.0)) * 0.08
        school_impact = sim_1ab_boost * 0.09
        tech_impact = sim_tech_boost * 0.015
        
        total_reduction = poverty_impact + school_impact + tech_impact
        simulated_rate = max(0.45, base_rate - total_reduction)
        students_saved = int(dist_row["total_enrolment"] * ((base_rate - simulated_rate) / 100.0))
        
        st.markdown(f"#### {t('sim_projection_title', lang, district=dist_disp)}")
        
        s1, s2, s3 = st.columns(3)
        with s1:
            st.metric(t("baseline_rate", lang), f"{base_rate:.2f}%")
        with s2:
            st.metric(t("projected_rate", lang), f"{simulated_rate:.2f}%", delta=f"-{(base_rate - simulated_rate):.2f}%", delta_color="inverse")
        with s3:
            st.metric(t("retained_students", lang), f"+{students_saved:,}")
            
        fig_sim = go.Figure(data=[
            go.Bar(name=t("baseline_rate", lang), x=[t("metric_dropout_rate", lang)], y=[base_rate], marker_color='#DC2626'),
            go.Bar(name=t("projected_rate", lang), x=[t("metric_dropout_rate", lang)], y=[simulated_rate], marker_color='#10B981')
        ])
        fig_sim.update_layout(
            title=t("simulation_chart_title", lang, district=dist_disp),
            height=320,
            barmode='group',
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC"
        )
        st.plotly_chart(fig_sim, use_container_width=True)

# ----------------------------------------------------
# EXECUTIVE BRIEFING ENGINE
# ----------------------------------------------------
st.markdown("---")
st.subheader(t("briefing_title", lang))

def generate_clean_executive_brief(dist, yr, d_row, r_row, cur_lang):
    rate = d_row['dropout_rate_pct']
    estate_share = d_row['estate_pop_pct']
    poverty = d_row['poverty_headcount_pct']
    science_density = d_row['pct_1ab_schools']
    score = r_row['composite_risk_score']
    tier = r_row['risk_tier']
    
    tier_l = get_localized_risk_tier(tier, cur_lang)
    dist_l = get_localized_district(dist, cur_lang)
    
    items = []
    if cur_lang == "si":
        header = f"📋 විධායක ප්‍රතිපත්ති විශ්ලේෂණය: {dist_l} දිස්ත්‍රික්කය ({yr})"
        items.append(f"<strong>වත්මන් අවදානම් තත්ත්වය:</strong> {dist_l} දිස්ත්‍රික්කයේ වාර්ෂික පාසල් හැරයාමේ ප්‍රතිශතය <strong>{rate:.2f}%</strong> ක් (සිසුන් {d_row['dropout_count']:,} ක්) වන අතර, එය <strong>{tier_l}</strong> කාණ්ඩයට අයත් වේ (සමස්ත අවදානම් ලකුණු: <strong>{score:.1f}/100</strong>).")
        if estate_share >= 15.0:
            items.append(f"<strong>වතු අංශයේ බලපෑම:</strong> දිස්ත්‍රික්කයේ ජනගහනයෙන් <strong>{estate_share:.1f}%</strong> ක් වතුකරයේ ජීවත්වන අතර, ද්විතීයික පාසල්වලට ඇති දුරස්ථබව සහ දෙමළ මාධ්‍ය උසස් පෙළ විද්‍යා අංශ හිඟවීම (1AB පාසල් ඇත්තේ <strong>{science_density:.1f}%</strong> පමණි) නිසා සා/පෙළ ශ්‍රේණිවලදී පාසල් හැරයාම ඉහළ ගොස් ඇත.")
        elif poverty >= 10.0:
            items.append(f"<strong>දිළිඳුකමේ පීඩනය:</strong> දිස්ත්‍රික්කයේ ඉහළ දිළිඳුකම (<strong>{poverty:.1f}%</strong>) හේතුවෙන් ආර්ථික පීඩනය හමුවේ 9 ශ්‍රේණියෙන් පසු දරුවන් අවිධිමත් රැකියාවලට යොමුවීමේ ප්‍රවණතාවක් පවතී.")
        else:
            items.append(f"<strong>යටිතල පහසුකම් තත්ත්වය:</strong> දිස්ත්‍රික්කය සාපේක්ෂව හොඳ පාසල් යටිතල පහසුකම් (1AB පාසල් <strong>{science_density:.1f}%</strong> සහ පරිගණක විද්‍යාගාර <strong>{d_row['pct_schools_with_computer_labs']:.1f}%</strong>) පවත්වාගෙන ගියද, ආර්ථික අර්බුදයේ බලපෑමෙන් අඩු ආදායම්ලාභී පවුල්වල දරුවන් ආරක්ෂා කිරීම අත්‍යවශ්‍ය වේ.")
        items.append("<strong>ප්‍රමුඛ ප්‍රතිපත්තිමය නිර්දේශය:</strong> ප්‍රවාහන සහනාධාර පුළුල් කිරීම, නොමිලේ පාසල් දිවා ආහාර වැඩසටහන් ක්‍රියාත්මක කිරීම සහ ප්‍රාදේශීය කනිෂ්ඨ විද්‍යාල 1AB ද්විභාෂා ආදර්ශ පාසල් බවට පත්කිරීම තුළින් 10–11 ශ්‍රේණිවල පාසල් හැරයාම වළක්වාගත හැක.")
    else:
        header = f"📋 Executive Policy Briefing: {dist_l} District ({yr})"
        items.append(f"<strong>Current Vulnerability Profile:</strong> {dist_l} exhibits an annual school dropout rate of <strong>{rate:.2f}%</strong> ({d_row['dropout_count']:,} students), placing it in the <strong>{tier_l}</strong> tier with a Composite Risk Score of <strong>{score:.1f}/100</strong>.")
        if estate_share >= 15.0:
            items.append(f"<strong>Estate Sector Exposure:</strong> With <strong>{estate_share:.1f}%</strong> of residents in the tea plantation sector, retention is constrained by secondary school commute distances and a lack of Tamil-medium A/L science streams (currently only <strong>{science_density:.1f}%</strong> of schools in {dist_l} are Type 1AB).")
        elif poverty >= 10.0:
            items.append(f"<strong>Poverty Headcount Challenge:</strong> High district poverty (<strong>{poverty:.1f}%</strong>) drives household economic distress, increasing adolescent dropout pressure after the compulsory Grade 9 cycle.")
        else:
            items.append(f"<strong>Infrastructure & Readiness:</strong> The district maintains relatively strong school infrastructure (<strong>{science_density:.1f}%</strong> 1AB schools and <strong>{d_row['pct_schools_with_computer_labs']:.1f}%</strong> computer lab penetration), though targeted retention safety nets remain vital for low-income pockets.")
        items.append("<strong>Recommended Priority Action:</strong> Expand subsidized student transport routes, guarantee universal school meal provisions, and upgrade local Type 2 junior schools into bilingual Type 1AB model centers to eliminate the Grade 10–11 drop-off cliff.")
    
    li_html = "".join([f"<li>{it}</li>" for it in items])
    card_html = f'<div class="executive-card"><div class="executive-header">{header}</div><ul class="executive-list">{li_html}</ul></div>'
    return card_html

st.markdown(generate_clean_executive_brief(selected_district, selected_year, dist_row, dist_risk_row, lang), unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align: center; color: #94A3B8; padding: 24px 0 10px 0; font-size: 0.85rem; border-top: 1px solid #E2E8F0; margin-top: 20px;">
    {t('footer_text', lang)}
</div>
""", unsafe_allow_html=True)
