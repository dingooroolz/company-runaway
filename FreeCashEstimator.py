import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="True Free Cash Engine", page_icon="💰", layout="wide")

st.title("💼 True Free Cash & EOY Tax Forecasting Engine")
st.write("Automatically grosses up your net director salary to track real-world business deductions and optimize corporate tax reservations.")
st.write("---")

# Define the Indian Financial Year sequence (April to March)
FY_MONTHS = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# Default baseline assumptions
BASELINE_REV = 500000
BASELINE_NET_SALARY = 300000
BASELINE_OH = 150000

# ==========================================
# 2. AUTOMATED SALARY GROSS-UP FUNCTION
# ==========================================
def calculate_gross_salary_and_tds(target_net_monthly):
    """
    Safely back-calculates required Gross Monthly Salary and Monthly TDS.
    """
    try:
        target_net_monthly = float(target_net_monthly)
        if target_net_monthly <= 0:
            return 0.0, 0.0
            
        target_net_annual = target_net_monthly * 12.0
        
        low_gross = target_net_annual
        high_gross = target_net_annual * 3.0
        exact_gross_annual = target_net_annual
        
        # Safe bounded loop
        for _ in range(40):
            mid_gross = (low_gross + high_gross) / 2.0
            taxable_salary = max(0.0, mid_gross - 75000.0)
            
            tax = 0.0
            if taxable_salary > 2400000:
                tax += (taxable_salary - 2400000) * 0.30 + 300000
            elif taxable_salary > 2000000:
                tax += (taxable_salary - 2000000) * 0.25 + 200000
            elif taxable_salary > 1600000:
                tax += (taxable_salary - 1600000) * 0.20 + 120000
            elif taxable_salary > 1200000:
                tax += (taxable_salary - 1200000) * 0.15 + 60000
            elif taxable_salary > 800000:
                tax += (taxable_salary - 800000) * 0.10 + 20000
            elif taxable_salary > 400000:
                tax += (taxable_salary - 400000) * 0.05
                
            total_personal_tax = tax * 1.04
            
            if taxable_salary <= 1200000:
                total_personal_tax = 0.0
                
            calculated_net = mid_gross - total_personal_tax
            
            if abs(calculated_net - target_net_annual) < 10.0:
                exact_gross_annual = mid_gross
                break
            elif calculated_net < target_net_annual:
                low_gross = mid_gross
            else:
                high_gross = mid_gross

        gross_monthly = exact_gross_annual / 12.0
        tds_monthly = (exact_gross_annual - target_net_annual) / 12.0
        return float(gross_monthly), float(tds_monthly)
    except Exception:
        return float(target_net_monthly), 0.0

# ==========================================
# 3. INTERACTIVE CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.header("🛠️ Engine Controls")

current_month = st.sidebar.selectbox(
    "Select the Current Active Month:", 
    options=FY_MONTHS, 
    index=2
)
current_month_idx = FY_MONTHS.index(current_month)

# --- SIDEBAR SECTION 1: PAST MONTHS ACTUALS ---
st.sidebar.write("---")
st.sidebar.subheader("📜 Past Months (Historical Actuals)")

past_revenues = {}
for idx in range(current_month_idx):
    m_name = FY_MONTHS[idx]
    past_revenues[m_name] = st.sidebar.number_input(
        f"Actual Revenue for {m_name}:",
        min_value=0,
        value=int(BASELINE_REV),
        step=25000,
        key=f"past_rev_{m_name}"
    )

# --- SIDEBAR SECTION 2: CURRENT MONTH TUNING ---
st.sidebar.write("---")
st.sidebar.subheader("📊 Current Month Tuning")
st.sidebar.markdown(f"**Active Month Context: {current_month}**")

current_active_revenue = st.sidebar.number_input(
    f"Revenue for {current_month}:",
    min_value=0,
    value=int(BASELINE_REV),
    step=25000,
    key="main_current_rev"
)

current_net_target = st.sidebar.number_input(
    f"Target NET Take-Home Salary ({current_month}):",
    min_value=0,
    value=int(BASELINE_NET_SALARY),
    step=10000,
    key="main_current_net_salary"
)

# Run conversion safely away from layout commands
current_gross_salary, current_monthly_tds = calculate_gross_salary_and_tds(current_net_target)

# --- SIDEBAR SECTION 3: FUTURE MONTHS PROJECTIONS ---
st.sidebar.write("---")
st.sidebar.subheader("🔮 Remaining Months Projections")

# ==========================================
# 4. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
final_monthly_records = []

for idx, m_name in enumerate(FY_MONTHS):
    if idx < current_month_idx:
        status = "Past (Closed)"
        revenue = past_revenues[m_name]
        net_sal = float(current_net_target) if current_net_target > 0 else float(BASELINE_NET_SALARY)
        gross_sal, tds_val = calculate_gross_salary_and_tds(net_sal)
        overhead = float(BASELINE_OH)
    elif idx == current_month_idx:
        status = "Present (Active)"
        revenue = float(current_active_revenue)
        gross_sal = float(current_gross_salary)
        tds_val = float(current_monthly_tds)
        overhead = 0.0
    else:
        st.sidebar.markdown(f"**{m_name}**")
        revenue = st.sidebar.number_input(
            f"Projected Revenue ({m_name}):",
            min_value=0,
            value=int(current_active_revenue),
            step=25000,
            key=f"loop_rev_{m_name}"
        )
        fut_net = st.sidebar.number_input(
            f"Projected Net Take-Home ({m_name}):",
            min_value=0,
            value=int(current_net_target),
            step=10000,
            key=f"loop_net_sal_{m_name}"
        )
        overhead = st.sidebar.number_input(
            f"Projected Overhead ({m_name}):",
            min_value=0,
            value=int(BASELINE_OH),
            step=5000,
            key=f"loop_oh_{m_name}"
        )
        status = "Future (Projected)"
        
    net_profit = max(0.0, float(revenue - gross_sal - overhead))
    calculated_tax = float(net_profit * 0.25)
    
    final_monthly_records.append({
        "Month": m_name,
        "Status": status,
        "Gross Revenue": float(revenue),
        "Company Salary Expense (Gross)": float(gross_sal),
        "Salary TDS (To Remit)": float(tds_val),
        "Projected Overhead": float(overhead),
        "Net Corporate Profit": float(net_profit),
        "Corporate Tax Liability": float(calculated_tax)
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 5. LIQUIDITY INPUTS & WATERFALL MATH
# ==========================================
col_input1, col_input2 = st.columns(2)

with col_input1:
    bank_balance = st.number_input(
        "💵 Current Bank Balance (₹):", 
        min_value=0, 
        value=1000000, 
        step=25000,
        key="main_bank_balance"
    )

with col_input2:
    st.caption("ℹ️ **Engine Rule Framework**")
    st.info(f"Your Freely Withdrawable Cash protects your liquid reserves by isolating the fresh corporate tax obligations generated after factoring in your grossed-up director salary for {current_month}.")

st.write("---")

current_month_tax_liability = float(df_engine.loc[current_month_idx, "Corporate Tax Liability"])
freely_withdrawable_cash = float(bank_balance - current_month_tax_liability)

# ==========================================
# 6. VISUAL METRICS DISPLAY
# ==========================================
st.subheader("🏁 Safe Withdrawal Matrix")

if freely_withdrawable_cash >= 0:
    st.success(f"### Freely Withdrawable Cash: **₹{freely_withdrawable_cash:,.2f}**")
else:
    st.error(f"### Shortfall Warning! Negative Liquidity Balance: **₹{freely_withdrawable_cash:,.2f}**")

with st.expander("🔍 Operational Breakdown"):
    st.write(f"**Starting Bank Balance Raw Liquidity:** ₹{bank_balance:,.2f}")
    st.write(f"💼 *Salary Gross-Up Info:* To receive ₹{current_net_target:,.2f} net, the company accounts for a gross salary expense of **₹{current_gross_salary:,.2f}** (includes **₹{current_monthly_tds:,.2f}** personal TDS to remit).")
    st.write(f"⚠️ *Minus* Live Predicted Corporate Tax Liability Generated (25% of net profit): -₹{current_month_tax_liability:,.2f}")
    st.write("---")
    st.write(f"**Net Discovered Spendable Capital:** ₹{freely_withdrawable_cash:,.2f}")

st.write("---")

# ==========================================
# 7. FISCAL SUMMARY SCOREBOARD
# ==========================================
st.subheader("📊 Full-Year Fiscal Projections (EOY Estimates)")

total_12_month_actual = float(df_engine["Gross Revenue"].sum())
only_remaining_future_revenue = float(df_engine[df_engine["Status"] == "Future (Projected)"]["Gross Revenue"].sum())
total_corporate_tax = float(df_engine["Corporate Tax Liability"].sum())
total_full_year_net_profit = float(df_engine["Net Corporate Profit"].sum())
profit_after_corporate_tax = max(0.0, float(total_full_year_net_profit - total_corporate_tax))

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric(label="My Actual Company Revenue", value=f"₹{total_12_month_actual:,.2f}")
col_m2.metric(label="My Projected Revenue", value=f"₹{only_remaining_future_revenue:,.2f}")
col_m3.metric(label="What Company Owes as Corporate Tax", value=f"₹{total_corporate_tax:,.2f}")
col_m4.metric(label="Company Profits After Corporate Tax", value=f"₹{profit_after_corporate_tax:,.2f}")

st.write("---")
st.write("### 📋 Underlying 12-Month Financial Spread Matrix")
preview_df = df_engine[["Month", "Status", "Gross Revenue", "Company Salary Expense (Gross)", "Salary TDS (To Remit)", "Projected Overhead", "Net Corporate Profit", "Corporate Tax Liability"]]
st.dataframe(preview_df, use_container_width=True)
