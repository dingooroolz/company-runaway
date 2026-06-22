import streamlit as st
import time

# Core state initialization
if 'net_worth' not in st.session_state:
    st.session_state.net_worth = 1000
if 'income_per_second' not in st.session_state:
    st.session_state.income_per_second = 0

# The Layout
st.title("💼 EMPIRE: The Ultimate Wealth Fantasy")
st.metric(label="Your Net Worth", value=f"₹{st.session_state.net_worth:,}")
st.caption(f"Passive Cash Flow: +₹{st.session_state.income_per_second}/sec")

# Action Options
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Execute High-Value Trade (+₹500)"):
        st.session_state.net_worth += 500
        st.rerun()

with col2:
    if st.button("🏢 Buy Commercial Real Estate (Cost: ₹5,000)"):
        if st.session_state.net_worth >= 5000:
            st.session_state.net_worth -= 5000
            st.session_state.income_per_second += 50
            st.success("Asset Acquired! Your passive income increased.")
            st.rerun()
        else:
            st.error("Insufficient liquid capital!")