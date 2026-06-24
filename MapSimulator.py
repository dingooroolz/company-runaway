import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Spatiotemporal Growth Simulator", page_icon="🗺️", layout="wide")

st.title("🗺️ Script 4: Interactive Geographic Growth & Multiplication Simulator")
st.write("Simulate regional expansion dynamics natively using built-in engine rendering parameters.")
st.write("---")

# ==========================================
# STATIC DATA: GEOGRAPHIC COORDINATE POOL (Northern India Hubs)
# ==========================================
# Native st.map requires columns named exactly 'latitude' and 'longitude'
GEOGRAPHIC_POOL = [
    {"Name": "Hub Base: Panchkula", "latitude": 30.6942, "longitude": 76.8606},
    {"Name": "Chandigarh Sector 15", "latitude": 30.7502, "longitude": 76.7610},
    {"Name": "Mohali Phase 3B2", "latitude": 30.7052, "longitude": 76.7236},
    {"Name": "Zirakpur Center", "latitude": 30.6425, "longitude": 76.8264},
    {"Name": "Pinjore Outreach", "latitude": 30.7954, "longitude": 76.9154},
    {"Name": "Kalka Substation", "latitude": 30.8331, "longitude": 76.9348},
    {"Name": "Ambala Cantt Hub", "latitude": 30.3440, "longitude": 76.8282},
    {"Name": "Kurukshetra Branch", "latitude": 29.9695, "longitude": 76.8783},
    {"Name": "Karnal Station", "latitude": 29.6857, "longitude": 76.9905},
    {"Name": "Panipat Outpost", "latitude": 29.3909, "longitude": 76.9635},
    {"Name": "Sonipat Fellowship", "latitude": 28.9948, "longitude": 77.0194},
    {"Name": "New Delhi North East Hub", "latitude": 28.6975, "longitude": 77.2913},
    {"Name": "New Delhi South Extension", "latitude": 28.5652, "longitude": 77.2185},
    {"Name": "Gurugram Core", "latitude": 28.4595, "longitude": 77.0266},
    {"Name": "Noida Extension Sector 62", "latitude": 28.6274, "longitude": 77.3725}
]

# ==========================================
# SIMULATION SESSION STATE CONTROLS
# ==========================================
if "sim_time_step" not in st.session_state:
    st.session_state.sim_time_step = 1

# ==========================================
# 2. INTERACTIVE PANEL (SIDEBAR)
# ==========================================
st.sidebar.header("🕹️ Simulation Engine Controls")
st.sidebar.write("Manipulate variables to observe resource-driven deployment velocities.")

# Variable 1: Funding Multiplier Strategy
funding_tier = st.sidebar.radio(
    "💰 Select Active Funding Layer Allocation:",
    options=["Seed Tier (Low)", "Sustained Tier (Medium)", "Exponential Acceleration (High)"],
    index=0
)

if funding_tier == "Seed Tier (Low)":
    growth_multiplier = 1
    tier_desc = "Standard linear propagation model."
    dot_color = "#1E88E5" # Blue
elif funding_tier == "Sustained Tier (Medium)":
    growth_multiplier = 2
    tier_desc = "Dual-track parallel multiplication enabled."
    dot_color = "#FFB300" # Orange
else:
    growth_multiplier = 4
    tier_desc = "High-velocity cluster planting strategy active."
    dot_color = "#D81B60" # Deep Pink

st.sidebar.info(f"**Throughput Efficiency:** {tier_desc}")

st.sidebar.write("---")
# Variable 2: Time Controls
st.sidebar.subheader("⏳ Time Sequence Management")
st.sidebar.write(f"Current Active Time Block: **Month {st.session_state.sim_time_step}**")

col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    if st.button("➕ Advance 1 Month", type="primary", use_container_width=True):
        st.session_state.sim_time_step += 1
        st.rerun()
with col_s2:
    if st.button("🔄 Reset Timeline", use_container_width=True):
        st.session_state.sim_time_step = 1
        st.rerun()

# ==========================================
# 3. MATHEMATICAL ALGORITHM PROJECTION ENGINE
# ==========================================
total_allowed_locations = st.session_state.sim_time_step * growth_multiplier
active_slice_count = min(total_allowed_locations, len(GEOGRAPHIC_POOL))
active_locations = GEOGRAPHIC_POOL[:active_slice_count]

df_map = pd.DataFrame(active_locations)

# ==========================================
# 4. DATA RENDERING & KPI SCOREBOARDS
# ==========================================
col_k1, col_k2, col_k3 = st.columns(3)
col_k1.metric(label="Current Simulation Phase", value=f"Month {st.session_state.sim_time_step}")
col_k2.metric(label="Simultaneous Growth Velocity", value=f"{growth_multiplier} Churches / Month")
col_k3.metric(label="Active Planted House Churches", value=f"{active_slice_count} Active Locations")

st.write("---")

# ==========================================
# 5. REAL PHYSICAL MAP DISPLAY LAYER (NATIVE)
# ==========================================
st.subheader("🗺️ Live Regional Deployment Map Coverage")

if df_map.empty:
    st.warning("Simulation parameters are at zero state. Advance time variables to populate graphical data layers.")
else:
    # Uses Streamlit's built-in map UI that requires zero dependencies
    st.map(
        df_map, 
        latitude="latitude", 
        longitude="longitude", 
        color=dot_color, 
        size=40
    )

# ==========================================
# 6. MASTER DATA VIEW LEDGER
# ==========================================
st.write("---")
st.subheader("📋 Active Location Network Blueprint Log")
if not df_map.empty:
    st.dataframe(df_map[["Name", "latitude", "longitude"]], use_container_width=True)
else:
    st.caption("No records initialized.")
