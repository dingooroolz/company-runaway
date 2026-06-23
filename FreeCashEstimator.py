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

# Default baseline assumptions
BASELINE_REV = 500000
BASELINE_OH = 150000

# ==========================================
# 2. INTERACTIVE CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.header("🛠️ Engine Controls")

current_month = st.sidebar.selectbox(
    "Select the Current Active Month:", 
    options=FY_MONTHS, 
    index=2 # Defaults to June
)
current_month_idx = FY_MONTHS.index(current_month)

# --- SIDEBAR SECTION 1: PAST MONTHS ACTUALS ---
st.sidebar.write("---")
st.sidebar.subheader("📜 Past Months (Historical Actuals)")
st.sidebar.caption("Input your true actual revenues for already closed months:")

past_revenues = {}
for idx in range(current_month_idx):
    m_name = FY_MONTHS[idx]
    past_revenues[m_name] = st.sidebar.number_input(
        f"Actual Revenue for {m_name}:",
        min_value=0,
        value=BASELINE_REV,
        step=25000,
        key=f"past_rev_{m_name}"
    )

# --- SIDEBAR SECTION 2: CURRENT MONTH TUNING ---
st.sidebar.write("---")
st.sidebar.subheader("📊 Current Month Tuning")
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

# --- SIDEBAR SECTION 3: FUTURE MONTHS PROJECTIONS ---
st.sidebar.write("---")
st.sidebar.subheader("🔮 Remaining Months Projections")
st.sidebar.caption("Independently adjust expected revenue and overhead constraints:")

# ==========================================
# 3. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
final_monthly_records = []

for idx, m_name in enumerate(FY_MONTHS):
    if idx < current_month_idx:
        status = "Past (Closed)"
        revenue = past_revenues[m_name]
        overhead = BASELINE_OH
    elif idx == current_month_idx:
        status = "Present (Active)"
        revenue = current_active_revenue
        overhead = current_changeable_overhead
    else:
        st.sidebar.markdown(f"**{m_name}**")
        revenue = st.sidebar.number_input(
            f"Projected Revenue ({m_name}):",
            min_value=0,
            value=int(current_active_revenue),
            step=25000,
            key=f"rev_{m_name}"
        )
        overhead = st.sidebar.number_input(
            f"Projected Overhead ({m_name}):",
            min_value=0,
            value=int(current_changeable_overhead),
            step=5000,
            key=f"oh_{m_name}"
        )
        status = "Future (Projected)"
        
    net_profit = max(0, revenue - overhead)
    calculated_tax = net_profit * 0.25
    calculated_tds = revenue * 0.10
    
    final_monthly_records.append({
        "Month": m_name,
        "Status": status,
        "Revenue": revenue,
        "Overhead": overhead,
        "Net Profit": net_profit,
        "Tax Liability": calculated_tax,
        "TDS": calculated_tds
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 4. LIQUIDITY INPUTS & WATERFALL MATH
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
    st.info(f"Past month manual revenue changes will affect EOY totals. Your Freely Withdrawable Cash is strictly calculated based on the current active month ({current_month}) constraints.")

st.write("---")

current_month_overhead_commitment = df_engine.loc[current_month_idx, "Overhead"]
current_month_tax_liability = df_engine.loc[current_month_idx, "Tax Liability"]

freely_withdrawable_cash = bank_balance - current_month_overhead_commitment - current_month_tax_liability

# ==========================================
# 5. VISUAL METRICS DISPLAY
# ==========================================
st.subheader("🏁 Safe Withdrawal Matrix")

if freely_withdrawable_cash >= 0:
    st.success(f"### Freely Withdrawable Cash: **₹{freely_withdrawable_cash:,.2f}**")
else:
    st.error(f"### Shortfall Warning! Negative Liquidity Balance: **₹{freely_withdrawable_cash:,.2f}**")

with st.expander("🔍 Operational Breakdown"):
    st.write(f"**Starting Bank Balance Raw Liquidity:** ₹{bank_balance:,.2f}")
    st.write(f"⚠️ *Minus* Active Monthly Overhead Budget Allocation ({current_month}): -₹{current_month_overhead_commitment:,.2f}")
    st.write(f"⚠️ *Minus* Live Predicted Tax Liability Generated for Current Month Revenue: -₹{current_month_tax_liability:,.2f}")
    st.write("---")
    st.write(f"**Net Discovered Spendable Capital:** ₹{freely_withdrawable_cash:,.2f}")

st.write("---")

# ==========================================
# 6. END OF YEAR FORECASTING BLOCKS
# ==========================================
st.subheader("📊 Full-Year Fiscal Projections (EOY Estimates)")

# Calculate isolated historical total actual revenue
total_actual_revenue_to_date = df_engine[df_engine["Status"] == "Past (Closed)"]["Revenue"].sum()

eoy_revenue = df_engine["Revenue"].sum()
eoy_calculated_tax = df_engine["Tax Liability"].sum()
eoy_tds = df_engine["TDS"].sum()
net_final_tax_payout_due = max(0, eoy_calculated_tax - tax_paid_so_far)

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.metric(label="Total Actual Revenue (To Date)", value=f"₹{total_actual_revenue_to_date:,.2f}")
with col_m2:
    st.metric(label="Total Projected Revenue (Full Yr)", value=f"₹{eoy_revenue:,.2f}")
with col_m3:
    st.metric(label="Est. Corporate Tax (Total Yr)", value=f"₹{eoy_calculated_tax:,.2f}")
with col_m4:
    st.metric(label="Estimated TDS Accrued", value=f"₹{eoy_tds:,.2f}")
with col_m5:
    st.metric(label="Net EOY Balance Due to Gov", value=f"₹{net_final_tax_payout_due:,.2f}", delta=f"-₹{tax_paid_so_far} Paid", delta_color="inverse")

st.write("### 📋 Underlying 12-Month Financial Spread Matrix")
st.dataframe(df_engine, use_container_width=True)
