import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Strategic Growth Simulator", page_icon="🗺️", layout="wide")

st.title("🗺️ Script 4: Targeted Regional Multiplication Simulator")
st.write("Simulating organic, outward expansion from key missional launch points across Punjab and Haryana.")
st.write("---")

# ==========================================
# SIMULATION SESSION STATE CONTROLS
# ==========================================
if "sim_month" not in st.session_state:
    st.session_state.sim_month = 1

# ==========================================
# 2. STRATEGIC TARGET ANCHORS (Your Specified Cities)
# ==========================================
PUNJAB_ANCHORS = [
    {"name": "Amritsar Hub", "lat": 31.6340, "lon": 74.8723},
    {"name": "Rajpura Hub", "lat": 30.4836, "lon": 76.5942},
    {"name": "Patiala Hub", "lat": 30.3398, "lon": 76.3869}
]

HARYANA_ANCHORS = [
    {"name": "Samalkha Hub", "lat": 29.2374, "lon": 77.0094},
    {"name": "Panipat Hub", "lat": 29.3909, "lon": 76.9635},
    {"name": "Ahmedpur Hub", "lat": 29.8377, "lon": 76.1751} # Mapped to regional coordinate sector
]

HIMACHAL_ANCHORS = [
    {"name": "Himachal West (Kangra)", "lat": 32.1001, "lon": 76.2691},
    {"name": "Himachal Central (Mandi)", "lat": 31.5892, "lon": 76.9182},
    {"name": "Himachal South (Shimla)", "lat": 31.1048, "lon": 77.1734}
]

# Combine all targeted launch points into a single master blueprint list
TARGETED_LAUNCH_POINTS = PUNJAB_ANCHORS + HARYANA_ANCHORS + HIMACHAL_ANCHORS

# ==========================================
# 3. INTERACTIVE CONTROLS (TOP CONSOLE CONFIGURATION)
# ==========================================
col_ctrl1, col_ctrl2 = st.columns([1, 3])

with col_ctrl1:
    funding_tier = st.radio(
        "💰 Funding Multiplier Allocation:",
        options=["Seed Tier (3%)", "Sustained Tier (7%)", "Exponential Acceleration (13.51%)"],
        index=2
    )

# Establish active compounding coefficients
if "Seed" in funding_tier:
    monthly_growth_rate = 0.03
    dot_color = "#00E5FF" # Electric Cyan
elif "Sustained" in funding_tier:
    monthly_growth_rate = 0.07
    dot_color = "#FF9100" # Neon Orange
else:
    monthly_growth_rate = 0.1351  # Reaches 2,000 at month 60
    dot_color = "#FF007F" # High-Vibrancy Neon Pink

# --- EMBEDDED MAP SLIDER INTERACTION BAR ---
st.write("### ⏳ Timeline Control Console")
st.session_state.sim_month = st.slider(
    "Slide to advance timeline phase and view outward cluster expansion:",
    min_value=1, max_value=60, value=st.session_state.sim_month, label_visibility="collapsed"
)

# ==========================================
# 4. ORGANIC SPATIAL SPREAD PROPAGATION MATH
# ==========================================
calculated_churches = int(1 * ((1 + monthly_growth_rate) ** st.session_state.sim_month))
display_count = min(calculated_churches, 2000)

# Build a deterministic pseudorandom loop anchored to your specific cities
rng = np.random.RandomState(42)

generated_latitudes = []
generated_longitudes = []
generated_names = []

for i in range(display_count):
    # The initial plants start directly inside your core target cities
    if i < len(TARGETED_LAUNCH_POINTS):
        base_city = TARGETED_LAUNCH_POINTS[i]
        lat = base_city["lat"]
        lon = base_city["lon"]
        name = f"Core Launch Point: {base_city['name']}"
    else:
        # Subsequent generations spawn organically around the target hubs
        # As time steps progress, the spread distance expands slightly to model country movement
        base_city = TARGETED_LAUNCH_POINTS[i % len(TARGETED_LAUNCH_POINTS)]
        
        # Organic spread range parameter calculation
        spread_range = 0.08 + (st.session_state.sim_month * 0.003)
        
        lat = base_city["lat"] + rng.normal(0, spread_range)
        lon = base_city["lon"] + rng.normal(0, spread_range)
        name = f"House Church Network Point #{i+1}"
        
    generated_latitudes.append(lat)
    generated_longitudes.append(lon)
    generated_names.append(name)

df_organic = pd.DataFrame({
    "Name": generated_names,
    "latitude": generated_latitudes,
    "longitude": generated_longitudes
})

# ==========================================
# 5. DYNAMIC MAP RENDER LAYER (ST.MAP NATIVE)
# ==========================================
# Passing the map a highly colorful, high-contrast dark style
st.map(
    df_organic,
    latitude="latitude",
    longitude="longitude",
    color=dot_color,
    size=35
)

# ==========================================
# 6. READOUT METRICS PANEL (FOOTER)
# ==========================================
st.write("---")
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric(label="Simulation Phase", value=f"Month {st.session_state.sim_month} (Year {round(st.session_state.sim_month/12, 1)})")
col_m2.metric(label="Planted Network Density", value=f"{display_count:,} Active Locations")
col_m3.metric(label="Target Vectors Engaged", value=f"{len(TARGETED_LAUNCH_POINTS)} Core Hubs")
