import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="True Free Cash Engine", page_icon="💰", layout="wide")

st.title("💼 True Free Cash & EOY Tax Forecasting Engine")
st.write("Strip away director salaries and accurate corporate tax liabilities to see exactly what you can safely withdraw right now.")
st.write("---")

# Define the Indian Financial Year sequence (April to March)
FY_MONTHS = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# Default baseline assumptions
BASELINE_REV = 500000
BASELINE_SALARY = 100000
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

current_director_salary = st.sidebar.number_input(
    f"Director Salary for {current_month}:",
    min_value=0,
    value=BASELINE_SALARY,
    step=10000,
    help="This acts as a business deduction, directly reducing your company's taxable profit.",
    key="current_salary"
)

# --- SIDEBAR SECTION 3: FUTURE MONTHS PROJECTIONS ---
st.sidebar.write("---")
st.sidebar.subheader("🔮 Remaining Months Projections")
st.sidebar.caption("Independently adjust expected revenue, salaries, and overhead constraints:")

# ==========================================
# 3. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
final_monthly_records = []

for idx, m_name in enumerate(FY_MONTHS):
    if idx < current_month_idx:
        status = "Past (Closed)"
        revenue = past_revenues[m_name]
        salary = BASELINE_SALARY
        overhead = BASELINE_OH
    elif idx == current_month_idx:
        status = "Present (Active)"
        revenue = current_active_revenue
        salary = current_director_salary
        overhead = 0  # General operations overhead is already factored directly out of bank balance
    else:
        st.sidebar.markdown(f"**{m_name}**")
        revenue = st.sidebar.number_input(
            f"Projected Revenue ({m_name}):",
            min_value=0,
            value=int(current_active_revenue),
            step=25000,
            key=f"rev_{m_name}"
        )
        salary = st.sidebar.number_input(
            f"Projected Director Salary ({m_name}):",
            min_value=0,
            value=int(current_director_salary),
            step=10000,
            key=f"salary_{m_name}"
        )
        overhead = st.sidebar.number_input(
            f"Projected Overhead ({m_name}):",
            min_value=0,
            value=int(BASELINE_OH),
            step=5000,
            key=f"oh_{m_name}"
        )
        status = "Future (Projected)"
        
    # The crucial change: Director salary reduces net corporate profit margins
    net_profit = max(0, revenue - salary - overhead)
    calculated_tax = net_profit * 0.25
    
    final_monthly_records.append({
        "Month": m_name,
        "Status": status,
        "Revenue": revenue,
        "Director Salary": salary,
        "Projected Overhead": overhead,
        "Net Taxable Profit": net_profit,
        "Corporate Tax Liability": calculated_tax
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 4. LIQUIDITY INPUTS & WATERFALL MATH
# ==========================================
col_input1, col_input2 = st.columns(2)

with col_input1:
    bank_balance = st.number_input(
        "💵 Current Bank Balance (₹):", 
        min_value=0, 
        value=1000000, 
        step=25000
    )

with col_input2:
    st.caption("ℹ️ **Engine Rule Framework**")
    st.info(f"Your Freely Withdrawable Cash protects your liquid reserves by isolating the fresh corporate tax obligations generated after your active director salary deduction for {current_month}.")

st.write("---")

# Extract live values for current month
current_month_tax_liability = df_engine.loc[current_month_idx, "Corporate Tax Liability"]

# Pure mathematical withdrawal formula
freely_withdrawable_cash = bank_balance - current_month_tax_liability

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
    st.write(f"ℹ️ *Salary Strategy:* Deducting a salary of ₹{current_director_salary:,.2f} safely lowered your corporate tax bill for the month.")
    st.write(f"⚠️ *Minus* Live Predicted Corporate Tax Liability Generated (25% of profit): -₹{current_month_tax_liability:,.2f}")
    st.write("---")
    st.write(f"**Net Discovered Spendable Capital:** ₹{freely_withdrawable_cash:,.2f}")

st.write("---")

# ==========================================
# 6. FISCAL SUMMARY SCOREBOARD
# ==========================================
st.subheader("📊 Full-Year Fiscal Projections (EOY Estimates)")

# 1. My Actual Company Revenue = Complete 12-month total
total_12_month_actual = df_engine["Revenue"].sum()

# 2. My Projected Revenue = Remaining future months total only
only_remaining_future_revenue = df_engine[df_engine["Status"] == "Future (Projected)"]["Revenue"].sum()

# Liabilities and profit models
total_corporate_tax = df_engine["Corporate Tax Liability"].sum()
total_full_year_net_profit = df_engine["Net Taxable Profit"].sum()
profit_after_corporate_tax = max(0, total_full_year_net_profit - total_corporate_tax)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="My Actual Company Revenue", value=f"₹{total_12_month_actual:,.2f}")
with col_m2:
    st.metric(label="My Projected Revenue", value=f"₹{only_remaining_future_revenue:,.2f}")
with col_m3:
    st.metric(label="What Company Owes as Corporate Tax", value=f"₹{total_corporate_tax:,.2f}")
with col_m4:
    st.metric(label="Company Profits After Corporate Tax", value=f"₹{profit_after_corporate_tax:,.2f}")

st.write("### 📋 Underlying 12-Month Financial Spread Matrix")
st.dataframe(df_engine, use_container_width=True)
