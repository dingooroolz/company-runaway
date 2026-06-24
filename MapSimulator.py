import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Spatiotemporal Growth Simulator", page_icon="🗺️", layout="wide")

st.title("🗺️ Script 4: Interactive Geographic Growth & Multiplication Simulator")
st.write("Simulate regional expansion dynamics by manipulating time phases and parallel funding multipliers.")
st.write("---")

# ==========================================
# STATIC DATA: GEOGRAPHIC COORDINATE POOL (Northern India Hubs)
# ==========================================
# A structured list of sequential coordinates to simulate outward expansion
GEOGRAPHIC_POOL = [
    {"Name": "Hub Base: Panchkula", "lat": 30.6942, "lon": 76.8606},
    {"Name": "Chandigarh Sector 15", "lat": 30.7502, "lon": 76.7610},
    {"Name": "Mohali Phase 3B2", "lat": 30.7052, "lon": 76.7236},
    {"Name": "Zirakpur Center", "lat": 30.6425, "lon": 76.8264},
    {"Name": "Pinjore Outreach", "lat": 30.7954, "lon": 76.9154},
    {"Name": "Kalka Substation", "lat": 30.8331, "lon": 76.9348},
    {"Name": "Ambala Cantt Hub", "lat": 30.3440, "lon": 76.8282},
    {"Name": "Kurukshetra Branch", "lat": 29.9695, "lon": 76.8783},
    {"Name": "Karnal Station", "lat": 29.6857, "lon": 76.9905},
    {"Name": "Panipat Outpost", "lat": 29.3909, "lon": 76.9635},
    {"Name": "Sonipat Fellowship", "lat": 28.9948, "lon": 77.0194},
    {"Name": "New Delhi North East Hub", "lat": 28.6975, "lon": 77.2913},
    {"Name": "New Delhi South Extension", "lat": 28.5652, "lon": 77.2185},
    {"Name": "Gurugram Core", "lat": 28.4595, "lon": 77.0266},
    {"Name": "Noida Extension Sector 62", "lat": 28.6274, "lon": 77.3725}
]

# ==========================================
# SIMULATION SESSION STATE CONTROLS
# ==========================================
if "sim_time_step" not in st.session_state:
    st.session_state.sim_time_step = 1

# ==========================================
# 2. INTERACTIVE INTERACTION PANEL (SIDEBAR)
# ==========================================
st.sidebar.header("🕹️ Simulation Engine Controls")
st.sidebar.write("Manipulate variables to observe resource-driven deployment velocities.")

# Variable 1: Funding Multiplier Strategy
funding_tier = st.sidebar.radio(
    "💰 Select Active Funding Layer Allocation:",
    options=["Seed Tier (Low)", "Sustained Tier (Medium)", "Exponential Acceleration (High)"],
    index=0
)

# Assign processing power multiplier depending on funding selection
if funding_tier == "Seed Tier (Low)":
    growth_multiplier = 1  # 1 time unit unlocks 1 location
    tier_desc = "Standard linear propagation model."
elif funding_tier == "Sustained Tier (Medium)":
    growth_multiplier = 2  # 1 time unit unlocks 2 locations
    tier_desc = "Dual-track parallel multiplication enabled."
else:
    growth_multiplier = 4  # 1 time unit unlocks 4 locations
    tier_desc = "High-velocity cluster planting strategy active."

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
# Calculate cumulative index allocation ceiling
total_allowed_locations = st.session_state.sim_time_step * growth_multiplier

# Cap the selection to the physical limits of our database pool coordinates
active_slice_count = min(total_allowed_locations, len(GEOGRAPHIC_POOL))
active_locations = GEOGRAPHIC_POOL[:active_slice_count]

# Convert active map state into structured analytics dataframe
df_map = pd.DataFrame(active_locations)

# ==========================================
# 4. DATA RENDERING & KPI SCOREBOARDS
# ==========================================
col_k1, col_k2, col_k3 = st.columns(3)
col_k1.metric(label="Current Simulation Phase", value=f"Month {st.session_state.sim_time_step}")
col_k2.metric(label="Simultaneous Growth Velocity", value=f"{growth_multiplier} Churches / Month")
col_k3.metric(label="Active Planted House Churches", value=f"{active_slice_count} Active Locations", 
              delta=None if st.session_state.sim_time_step == 1 else f"+{growth_multiplier} this phase")

st.write("---")

# ==========================================
# 5. REAL PHYSICAL MAP DISPLAY LAYER (PLOTLY)
# ==========================================
st.subheader("🗺️ Live Regional Deployment Map Coverage")

if df_map.empty:
    st.warning("Simulation parameters are at zero state. Advance time variables to populate graphical data layers.")
else:
    # Build complete programmatic Mapbox canvas
    fig = go.Figure()

    # Add geographical scatter pin points
    fig.add_trace(go.Scattermapbox(
        lat=df_map['lat'],
        lon=df_map['lon'],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=16,
            color='#1E88E5' if growth_multiplier == 1 else ('#FFB300' if growth_multiplier == 2 else '#D81B60'),
            opacity=0.9
        ),
        text=df_map['Name'],
        textposition="top center",
        hoverinfo='text'
    ))

    # Establish look-at camera viewpoint framing around Northern India center points
    fig.update_layout(
        mapbox=dict(
            style="open-street-map", # Clear physical street road topography layers
            center=dict(lat=29.8, lon=77.2),
            zoom=6.8
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        height=550,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 6. MASTER DATA VIEW LEDGER
# ==========================================
st.write("---")
st.subheader("📋 Active Location Network Blueprint Log")
if not df_map.empty:
    st.dataframe(df_map[["Name", "lat", "lon"]], use_container_width=True)
else:
    st.caption("No records initialized.")
