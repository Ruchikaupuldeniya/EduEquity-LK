
"""
EduEquity LK - Utility functions, constants, and helper routines.
"""

import json
import os
from typing import Dict, Any, Optional

# Harmonious, modern color palette
PALETTE = {
    "primary": "#1E3A8A",       # Deep Sapphire
    "secondary": "#0D9488",     # Teal Emerald
    "accent": "#F59E0B",        # Amber Gold
    "danger": "#EF4444",        # Crimson Red
    "warning": "#F97316",       # Sunset Orange
    "success": "#10B981",       # Emerald Green
    "dark": "#0F172A",          # Slate Dark
    "light": "#F8FAFC",         # Cool Light Slate
    "card_bg": "#1E293B",       # Card Surface
    "estate": "#D97706",        # Rich Ochre (Estate Sector)
    "rural": "#059669",         # Forest Green (Rural Sector)
    "urban": "#2563EB",         # Royal Blue (Urban Sector)
    "national": "#64748B"       # Slate Neutral
}

# Standardized district name mapping
DISTRICT_SYNONYMS = {
    "nuwaraeliya": "Nuwara Eliya",
    "nuwara eliya": "Nuwara Eliya",
    "nuwara-eliya": "Nuwara Eliya",
    "moneragala": "Monaragala",
    "monaragala": "Monaragala",
    "kegalla": "Kegalle",
    "kegalle": "Kegalle",
    "mullaitivu": "Mullaitivu",
    "mullativu": "Mullaitivu",
    "kilinochchi": "Kilinochchi",
    "batticaloa": "Batticaloa"
}

def standardize_district_name(name: str) -> str:
    """Normalizes district name strings to official DCS standard."""
    if not isinstance(name, str):
        return ""
    clean = name.strip()
    clean_lower = clean.lower()
    return DISTRICT_SYNONYMS.get(clean_lower, clean.title())

def load_district_geojson(filepath: str = "data/raw/sri_lanka_districts.geojson") -> Optional[Dict[str, Any]]:
    """Loads GeoJSON dictionary from raw storage."""
    if not os.path.exists(filepath):
        print(f"Warning: GeoJSON not found at {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def format_pct(value: float, decimals: int = 1) -> str:
    """Formats numeric float as percentage string."""
    if value is None or (isinstance(value, float) and value != value):
        return "N/A"
    return f"{value:.{decimals}f}%"

def format_lkr(value: float) -> str:
    """Formats currency in Sri Lankan Rupees."""
    if value is None or (isinstance(value, float) and value != value):
        return "N/A"
    return f"LKR {value:,.0f}"

def classify_risk_tier(score: float) -> str:
    """Classifies risk score (0-100) into risk tier category."""
    if score >= 70.0:
        return "Critical Risk"
    elif score >= 50.0:
        return "Elevated Risk"
    elif score >= 30.0:
        return "Moderate Risk"
    else:
        return "Low Risk"

def get_risk_tier_color(tier: str) -> str:
    """Returns matching hex color for risk tier."""
    mapping = {
        "Critical Risk": "#DC2626", # Deep Red
        "Elevated Risk": "#EA580C", # Dark Orange
        "Moderate Risk": "#D97706", # Amber
        "Low Risk": "#16A34A"       # Green
    }
    return mapping.get(tier, "#64748B")
