import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="True Free Cash Engine", page_icon="💰", layout="wide")

st.title("💼 True Free Cash & EOY Tax Forecasting Engine")
st.write("Strip away business overhead and accurate tax liabilities to see exactly what you can withdraw right now.")
st.write("---")

# Define the Indian Financial Year sequence (April to March)
FY_MONTHS = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# ==========================================
# 2. BASELINE DATA CONFIGURATION
# ==========================================
# Default baseline assumptions if not overridden by the user
BASELINE_REV = 500000
BASELINE_OH = 150000

baseline_data = {
    "Month": FY_MONTHS,
    "Estimated_Revenue": [BASELINE_REV] * 12,
    "Fixed_Overhead": [BASELINE_OH] * 12,
}
df_base = pd.DataFrame(baseline_data)

# ==========================================
# 3. INTERACTIVE CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.header("🛠️ Engine Controls")

# Control 1: Choose the starting configuration month
current_month = st.sidebar.selectbox(
    "Select the Current Active Month:", 
    options=FY_MONTHS, 
    index=2 # Defaults to June
)
current_month_idx = FY_MONTHS.index(current_month)

st.sidebar.write("---")
st.sidebar.subheader("📊 Current Month Tuning")

# Capture user input for the CURRENT active month
st.sidebar.markdown(f"**Current Month ({current_month})**")
current_active_revenue = st.sidebar.number_input(
    f"Revenue for {current_month}:",
    min_value=0,
    value=BASELINE_REV,
    step=25000,
    key="current_rev"
)
current_changeable_overhead = st.sidebar.number_input(
    f"Active Overhead for {current_month}:",
    min_value=0,
    value=BASELINE_OH,
    step=5000,
    key="current_oh"
)

st.sidebar.write("---")
st.sidebar.subheader("🔮 Remaining Months Projections")
st.sidebar.caption("Independently adjust expected revenue and overhead constraints for upcoming months:")

# ==========================================
# 4. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
final_monthly_records = []

# Build the dynamic 12-month fiscal spreadsheet model
for idx, row in df_base.iterrows():
    month_name = row["Month"]
    
    if idx < current_month_idx:
        # PAST MONTHS: Locked History
        status = "Past (Closed)"
        revenue = row["Estimated_Revenue"]
        overhead = row["Fixed_Overhead"]
    elif idx == current_month_idx:
        # CURRENT MONTH: Driven dynamically by our primary inputs
        status = "Present (Active)"
        revenue = current_active_revenue
        overhead = current_changeable_overhead
    else:
        # FUTURE MONTHS: Individually editable inputs in the sidebar
        st.sidebar.markdown(f"**{month_name}**")
        revenue = st.sidebar.number_input(
            f"Projected Revenue ({month_name}):",
            min_value=0,
            value=int(current_active_revenue), # Defaults to current month's active revenue input
            step=25000,
            key=f"rev_{month_name}"
        )
        overhead = st.sidebar.number_input(
            f"Projected Overhead ({month_name}):",
            min_value=0,
            value=int(current_changeable_overhead), # Defaults to current month's overhead input
            step=5000,
            key=f"oh_{month_name}"
        )
        status = "Future (Projected)"
        
    net_profit = max(0, revenue - overhead)
    # Estimated Corporate Tax (Assumed flat baseline rate of 25% on business profit margins)
    calculated_tax = net_profit * 0.25
    # Estimated TDS tracking (Assumed standard 10% source deduction on inbound gross revenue streams)
    calculated_tds = revenue * 0.10
    
    final_monthly_records.append({
        "Month": month_name,
        "Status": status,
        "Revenue": revenue,
        "Overhead": overhead,
        "Net Profit": net_profit,
        "Tax Liability": calculated_tax,
        "TDS": calculated_tds
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 5. LIQUIDITY INPUTS & WATERFALL MATH
# ==========================================
col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    bank_balance = st.number_input(
        "💵 Current Bank Balance (₹):", 
        min_value=0, 
        value=1000000, 
        step=25000
    )

with col_input2:
    tax_paid_so_far = st.number_input(
        "🏛️ Actual Tax Settled Up to Date (₹):",
        min_value=0,
        value=0,
        step=5000,
        help="Input your real-world historical settlements (Advance Tax, TDS credits used, or Q1 payouts)."
    )

with col_input3:
    st.caption("ℹ️ **Engine Rule Framework**")
    st.info(f"The engine assumes you have settled all taxes prior to **{current_month}** via the input amount. It will now isolate and reserve fresh taxes generated by **{current_month}**.")

st.write("---")

# Core Liquidity Math execution
current_month_overhead_commitment = df_engine.loc[current_month_idx, "Overhead"]
current_month_tax_liability = df_engine.loc[current_month_idx, "Tax Liability"]

# Ultimate Authorization Equation: Balance minus current commitments and dynamic month tax
freely_withdrawable_cash = bank_balance - current_month_overhead_commitment - current_month_tax_liability

# ==========================================
# 6. VISUAL METRICS DISPLAY
# ==========================================
st.subheader("🏁 Safe Withdrawal Matrix")

if freely_withdrawable_cash >= 0:
    st.success(f"### Freely
