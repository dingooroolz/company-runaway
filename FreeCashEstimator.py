import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="True Free Cash Engine", page_icon="💰", layout="wide")

st.title("💼 True Free Cash & EOY Tax Forecasting Engine")
st.write("Tracks real-world baseline liquidity while running a parallel zero-tax optimization forecast for salary surplus routing.")
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

past_data = {}
for idx in range(current_month_idx):
    m_name = FY_MONTHS[idx]
    st.sidebar.markdown(f"**Past Month: {m_name}**")
    
    p_rev = st.sidebar.number_input(f"True Revenue ({m_name}):", min_value=0, value=int(BASELINE_REV), step=25000, key=f"past_rev_{m_name}")
    p_net = st.sidebar.number_input(f"True Net Salary Paid ({m_name}):", min_value=0, value=int(BASELINE_NET_SALARY), step=10000, key=f"past_net_{m_name}")
    p_oh = st.sidebar.number_input(f"True Overhead ({m_name}):", min_value=0, value=int(BASELINE_OH), step=5000, key=f"past_oh_{m_name}")
    
    past_data[m_name] = {"revenue": p_rev, "net_salary": p_net, "overhead": p_oh}

# --- SIDEBAR SECTION 2: CURRENT MONTH TUNING ---
st.sidebar.write("---")
st.sidebar.subheader("📊 Current Month Tuning")
st.sidebar.markdown(f"**Active Month Context: {current_month}**")

current_active_revenue = st.sidebar.number_input(f"Revenue for {current_month}:", min_value=0, value=int(BASELINE_REV), step=25000, key="main_current_rev")
current_net_target = st.sidebar.number_input(f"Target NET Take-Home Salary ({current_month}):", min_value=0, value=int(BASELINE_NET_SALARY), step=10000, key="main_current_net_salary")
current_active_overhead = st.sidebar.number_input(f"Overhead Expenses for {current_month}:", min_value=0, value=int(BASELINE_OH), step=5000, key="main_current_overhead")

current_gross_salary, current_monthly_tds = calculate_gross_salary_and_tds(current_net_target)

# --- SIDEBAR SECTION 3: FUTURE MONTHS PROJECTIONS ---
st.sidebar.write("---")
st.sidebar.subheader("🔮 Remaining Months Projections")

use_global_override = st.sidebar.toggle("🔗 Enable Global Run Rate", value=True)

if use_global_override:
    st.sidebar.markdown("⚡ *Global Baseline Drivers*")
    global_revenue = st.sidebar.number_input("Global Projected Revenue:", min_value=0, value=int(current_active_revenue), step=25000, key="global_rev")
    global_net_sal = st.sidebar.number_input("Global Projected Net Take-Home:", min_value=0, value=int(current_net_target), step=10000, key="global_net_sal")
    global_overhead = st.sidebar.number_input("Global Projected Overhead:", min_value=0, value=int(current_active_overhead), step=5000, key="global_oh")

# ==========================================
# 4. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
final_monthly_records = []

for idx, m_name in enumerate(FY_MONTHS):
    if idx < current_month_idx:
        status = "Past (Closed)"
        revenue = past_data[m_name]["revenue"]
        net_sal = past_data[m_name]["net_salary"]
        gross_sal, tds_val = calculate_gross_salary_and_tds(net_sal)
        overhead = past_data[m_name]["overhead"]
    elif idx == current_month_idx:
        status = "Present (Active)"
        revenue = float(current_active_revenue)
        gross_sal = float(current_gross_salary)
        tds_val = float(current_monthly_tds)
        overhead = float(current_active_overhead)
    else:
        status = "Future (Projected)"
        if use_global_override:
            revenue = float(global_revenue)
            net_sal = float(global_net_sal)
            gross_sal, tds_val = calculate_gross_salary_and_tds(net_sal)
            overhead = float(global_overhead)
        else:
            st.sidebar.markdown(f"**{m_name}**")
            revenue = st.sidebar.number_input(f"Projected Revenue ({m_name}):", min_value=0, value=int(current_active_revenue), step=25000, key=f"loop_rev_{m_name}")
            fut_net = st.sidebar.number_input(f"Projected Net Take-Home ({m_name}):", min_value=0, value=int(current_net_target), step=10000, key=f"loop_net_sal_{m_name}")
            gross_sal, tds_val = calculate_gross_salary_and_tds(fut_net)
            overhead = st.sidebar.number_input(f"Projected Overhead ({m_name}):", min_value=0, value=int(current_active_overhead), step=5000, key=f"loop_oh_{m_name}")
        
    # --- Standard Track Calculations ---
    standard_net_profit = max(0.0, float(revenue - gross_sal - overhead))
    standard_corp_tax = float(standard_net_profit * 0.25)
    
    # --- PARALLEL OVERHEAD SURPLUS SIMULATION MATH ---
    sim_available_surplus = standard_net_profit 
    sim_total_gross_salary = gross_sal + sim_available_surplus
    
    sim_net_annual_est = max(0.0, (sim_total_gross_salary * 12.0) * 0.70)
    _, sim_combined_monthly_tds = calculate_gross_salary_and_tds(sim_net_annual_est / 12.0)
    
    sim_corp_tax = 0.0
    
    final_monthly_records.append({
        "Month": m_name,
        "Status": status,
        "Gross Revenue": float(revenue),
        "Company Salary Expense (Gross)": float(gross_sal),
        "Salary TDS (To Remit)": float(tds_val),
        "Projected Overhead": float(overhead),
        "Net Corporate Profit": float(standard_net_profit),
        "Corporate Tax Liability": float(standard_corp_tax),
        "Simulated Total Gross Salary": float(sim_total_gross_salary),
        "Simulated Extra Salary TDS": float(sim_combined_monthly_tds - tds_val if sim_combined_monthly_tds > tds_val else 0.0),
        "Simulated Corporate Tax": float(sim_corp_tax)
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 5. AUTOMATED LIQUIDITY & WATERFALL MATH
# ==========================================
calculated_bank_balance = float(current_active_revenue - current_gross_salary - current_active_overhead)
current_month_tax_liability = float(df_engine.loc[current_month_idx, "Corporate Tax Liability"])
freely_withdrawable_cash = float(calculated_bank_balance - current_month_tax_liability)

# ==========================================
# 6. VISUAL METRICS DISPLAY
# ==========================================
st.subheader("🏁 Safe Withdrawal Matrix")

if freely_withdrawable_cash >= 0:
    st.success(f"### Freely Withdrawable Cash: **₹{freely_withdrawable_cash:,.2f}**")
else:
    st.error(f"### Shortfall Warning! Negative Liquidity Balance: **₹{freely_withdrawable_cash:,.2f}**")

# RESTORED: Detailed breakdown analysis component
with st.expander("🔍 Operational Breakdown"):
    st.write(f"**Step 1. Starting Gross Revenue ({current_month}):** ₹{current_active_revenue:,.2f}")
    st.write(f"💼 *Step 2. Deduct Salary Gross-Up Info:* Target payout of ₹{current_net_target:,.2f} + Company TDS reservation of ₹{current_monthly_tds:,.2f} = Total Gross Expense of **-₹{current_gross_salary:,.2f}**")
    st.write(f"🛠️ *Step 3. Deduct Overhead Expenses:* -₹{current_active_overhead:,.2f}")
    st.write(f"➡️ **Calculated Bank Balance (Liquid Leftover):** **₹{calculated_bank_balance:,.2f}**")
    st.write(f"⚠️ *Step 4. Isolate Corporate Tax Liability (25% of ₹{df_engine.loc[current_month_idx, 'Net Corporate Profit']:,.2f} profit):* -₹{current_month_tax_liability:,.2f}")
    st.write("---")
    st.write(f"🏁 **Net Discovered Spendable Capital (Freely Withdrawable Cash):** **₹{freely_withdrawable_cash:,.2f}**")

st.write("---")

# ==========================================
# 7. FISCAL SUMMARY SCOREBOARDS (COMPARATIVE LAYOUT)
# ==========================================
st.subheader("📊 Full-Year Fiscal Projections (EOY Estimates)")

total_12_month_actual = float(df_engine["Gross Revenue"].sum())
only_remaining_future_revenue = float(df_engine[df_engine["Status"] == "Future (Projected)"]["Gross Revenue"].sum())
total_corporate_tax = float(df_engine["Corporate Tax Liability"].sum())
total_full_year_net_profit = float(df_engine["Net Corporate Profit"].sum())
profit_after_corporate_tax = max(0.0, float(total_full_year_net_profit - total_corporate_tax))

st.markdown("#### Baseline Strategy (Current Input Configuration)")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric(label="Total Annual Revenue", value=f"₹{total_12_month_actual:,.2f}")
col_m2.metric(label="Projected Remaining Inflows", value=f"₹{only_remaining_future_revenue:,.2f}")
col_m3.metric(label="What Company Owes as Corporate Tax", value=f"₹{total_corporate_tax:,.2f}")
col_m4.metric(label="Company Profits After Corporate Tax", value=f"₹{profit_after_corporate_tax:,.2f}")

total_sim_extra_tds = float(df_engine["Simulated Extra Salary TDS"].sum())
total_base_tds = float(df_engine["Salary TDS (To Remit)"].sum())
grand_total_personal_tds_remittance = total_base_tds + total_sim_extra_tds

st.write("---")
st.markdown("#### ⚡ Parallel Scenario Strategy: *Zero-Tax Salary Surplus Optimization*")
st.caption("This model simulates sweeping 100% of residual company cash out as a director salary bonus across all months to force company taxable income down to zero.")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
col_s1.metric(label="Simulated Corporate Tax Due", value="₹0.00", delta="-100% Tax Drop", delta_color="inverse")
col_s2.metric(label="Additional Personal TDS Triggered", value=f"₹{total_sim_extra_tds:,.2f}", delta="Outflow Increase", delta_color="off")
col_s3.metric(label="Grand Total Personal TDS To Remit", value=f"₹{grand_total_personal_tds_remittance:,.2f}")
col_s4.metric(label="Remaining Left Inside Company", value="₹0.00", delta="Fully Extracted", delta_color="normal")

st.write("---")
st.write("### 📋 Comparative 12-Month Financial Spread Matrix")

preview_df = df_engine[[
    "Month", "Status", "Gross Revenue", "Company Salary Expense (Gross)", "Projected Overhead",
    "Corporate Tax Liability", "Simulated Total Gross Salary", "Simulated Extra Salary TDS", "Simulated Corporate Tax"
]]
st.dataframe(preview_df, use_container_width=True)
