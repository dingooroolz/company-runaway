import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Tri-State Growth Simulator", page_icon="🗺️", layout="wide")

st.title("🗺️ Script 4: Tri-State House Church Multiplication Simulator")
st.write("Projecting 5-Year (60 Month) exponential expansion across Punjab, Haryana, and Himachal Pradesh.")
st.write("---")

# ==========================================
# SIMULATION SESSION STATE CONTROLS
# ==========================================
if "sim_month" not in st.session_state:
    st.session_state.sim_month = 1

# ==========================================
# 2. INTERACTIVE CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.header("🕹️ Simulation Parameters")

# Variable 1: Funding Controls the Compounding Interest Rate
funding_tier = st.sidebar.radio(
    "💰 Funding Allocation Layer:",
    options=["Seed Tier (Low Growth - 3%)", "Sustained Tier (Med Growth - 7%)", "Exponential Acceleration (High Growth - 13.51%)"],
    index=2  # Default to High to let them see the 2,000 target immediately
)

if "Low" in funding_tier:
    monthly_growth_rate = 0.03
    dot_color = "#1E88E5" # Blue
    desc = "Linear local planting."
elif "Med" in funding_tier:
    monthly_growth_rate = 0.07
    dot_color = "#FFB300" # Orange
    desc = "Active regional multiplication."
else:
    monthly_growth_rate = 0.1351  # Calibrated mathematically to hit exactly ~2,000 at month 60
    dot_color = "#D81B60" # Deep Pink
    desc = "High-velocity saturation strategy."

st.sidebar.info(f"**Strategy Matrix:** {desc}")
st.sidebar.write("---")

# Variable 2: Timeline Navigation
st.sidebar.subheader("⏳ 5-Year Timeline (Months 1 - 60)")
st.sidebar.write(f"Current Phase: **Month {st.session_state.sim_month}** ({round(st.session_state.sim_month/12, 1)} Years)")

# Slider for quick scrubbing on mobile phones
st.session_state.sim_month = st.sidebar.slider("Scrub Through Time:", min_value=1, max_value=60, value=st.session_state.sim_month)

col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    if st.button("➕ Advance 1 Month", type="primary", use_container_width=True):
        if st.session_state.sim_month < 60:
            st.session_state.sim_month += 1
            st.rerun()
with col_s2:
    if st.button("🔄 Reset to Month 1", use_container_width=True):
        st.session_state.sim_month = 1
        st.rerun()

# ==========================================
# 3. SPATIOTEMPORAL PROPAGATION ALGORITHM
# ==========================================
# Compounding curve logic: Target Count = Baseline * (1 + r)^t
calculated_churches = int(1 * ((1 + monthly_growth_rate) ** st.session_state.sim_month))

# Cap at the 5-year vision target ceiling
display_count = min(calculated_churches, 2000)

# Tri-State Regional Anchor Lat/Lons
REGIONAL_HUBS = [
    {"name": "Punjab Central (Ludhiana/Jalandhar)", "lat": 31.1471, "lon": 75.3412},
    {"name": "Haryana Hub (Panchkula/Ambala)", "lat": 30.3752, "lon": 76.7790},
    {"name": "Himachal Base (Shimla/Kangra)", "lat": 31.7087, "lon": 76.9320}
]

# Programmatic coordinate vector generator using a seeded random state 
# This ensures that when moving time forward/backward, points spawn in the exact same positions
rng = np.random.RandomState(42)

generated_latitudes = []
generated_longitudes = []
generated_names = []

for i in range(display_count):
    if i == 0:
        # Church #1 always starts at your base headquarters
        lat, lon = 30.6942, 76.8606  # Panchkula Core
        name = "Base Hub: Panchkula"
    else:
        # Systematically distribute upcoming plants across Punjab, Haryana, and HP
        hub = REGIONAL_HUBS[i % len(REGIONAL_HUBS)]
        
        # Outward spread variance increases slightly over time to simulate rural movement
        spread_factor = 0.15 + (st.session_state.sim_month * 0.005)
        
        # Calculate random vectors around regional anchors
        lat = hub["lat"] + rng.normal(0, spread_factor)
        lon = hub["lon"] + rng.normal(0, spread_factor)
        name = f"House Church #{i+1}"
        
    generated_latitudes.append(lat)
    generated_longitudes.append(lon)
    generated_names.append(name)

df_tri_state = pd.DataFrame({
    "Name": generated_names,
    "latitude": generated_latitudes,
    "longitude": generated_longitudes
})

# ==========================================
# 4. KPI SCOREBOARDS
# ==========================================
col_k1, col_k2, col_k3 = st.columns(3)
col_k1.metric(label="Current Timeline Phase", value=f"Month {st.session_state.sim_month} / 60", delta=f"Year {round(st.session_state.sim_month/12, 1)}")
col_k2.metric(label="Compound Monthly Growth (r)", value=f"{monthly_growth_rate*100:.2f}%")
col_k3.metric(label="Total Projected Plants", value=f"{display_count:,} House Churches")

st.write("---")

# ==========================================
# 5. REAL PHYSICAL MAP LAYER (NATIVE)
# ==========================================
st.subheader("🗺️ Tri-State Multiplication Density Map Coverage")
st.caption("Visualizing geographical clusters interacting across Punjab, Haryana, and Himachal Pradesh.")

if df_tri_state.empty:
    st.warning("Simulation parameters at zero state.")
else:
    # Native map viewport sizing
    st.map(
        df_tri_state,
        latitude="latitude",
        longitude="longitude",
        color=dot_color,
        size=30
    )

# ==========================================
# 6. REGIONAL SUMMARY STATS
# ==========================================
st.write("---")
st.subheader("📊 Dynamic Run-Rate Projections")

# Quick bounding box math to categorize clusters roughly into states for reporting
punjab_counts = sum(1 for lat, lon in zip(generated_latitudes, generated_longitudes) if lon < 75.8)
hp_counts = sum(1 for lat, lon in zip(generated_latitudes, generated_longitudes) if lat > 31.2 and lon > 76.5)
haryana_counts = display_count - punjab_counts - hp_counts

col_p1, col_p2, col_p3 = st.columns(3)
col_p1.info(f"🌾 **Punjab Clusters:** {punjab_counts} locations")
col_p2.info(f"🚜 **Haryana Clusters:** {haryana_counts} locations")
col_p3.info(f"🏔️ **Himachal Clusters:** {hp_counts} locations")
