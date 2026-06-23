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
        net_sal = float(current_net_target)
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
            net_sal = st.sidebar.number_input(f"Projected Net Take-Home ({m_name}):", min_value=0, value=int(current_net_target), step=10000, key=f"loop_net_sal_{m_name}")
            gross_sal, tds_val = calculate_gross_salary_and_tds(net_sal)
            overhead = st.sidebar.number_input(f"Projected Overhead ({m_name}):", min_value=0, value=int(current_active_overhead), step=5000, key=f"loop_oh_{m_name}")
        
    # --- Standard Track Calculations ---
    standard_net_profit = max(0.0, float(revenue - gross_sal - overhead))
    standard_corp_tax = float(standard_net_profit * 0.25)
    
    # --- PARALLEL OVERHEAD SURPLUS SIMULATION MATH ---
    gross_surplus = standard_net_profit 
    surplus_tds = float(gross_surplus * 0.312) if gross_surplus > 0 else 0.0
    net_surplus_payout = max(0.0, gross_surplus - surplus_tds)
    total_net_personal_takehome = float(net_sal + net_surplus_payout)
    
    final_monthly_records.append({
        "Month": m_name,
        "Status": status,
        "Gross Revenue": float(revenue),
        "Company Salary Expense (Gross)": float(gross_sal),
        "Salary TDS (To Remit)": float(tds_val),
        "Net Take-Home Salary": float(net_sal),
        "Projected Overhead": float(overhead),
        "Net Corporate Profit": float(standard_net_profit),
        "Corporate Tax Liability": float(standard_corp_tax),
        # Personal Ledger Allocations
        "Gross Surplus": float(gross_surplus),
        "Surplus TDS": float(surplus_tds),
        "Net Surplus (After Tax)": float(net_surplus_payout),
        "Total Tax-Free Personal Cash Flow": float(total_net_personal_takehome)
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 5. AUTOMATED LIQUIDITY & WATERFALL MATH
# ==========================================
calculated_bank_balance = float(current_active_revenue - current_gross_salary - current_active_overhead)
current_month_tax_liability = float(df_engine.loc[current_month_idx, "Corporate Tax Liability"])
freely_withdrawable_cash = float(calculated_bank_balance - current_month_tax_liability)
current_month_personal_cash = float(df_engine.loc[current_month_idx, "Total Tax-Free Personal Cash Flow"])

# ==========================================
# 6. VISUAL METRICS DISPLAY
# ==========================================
col_w1, col_w2 = st.columns(2)

with col_w1:
    st.subheader("🏁 Safe Withdrawal Matrix")
    if freely_withdrawable_cash >= 0:
        st.success(f"### Freely Withdrawable Cash: **₹{freely_withdrawable_cash:,.2f}**")
    else:
        st.error(f"### Shortfall Warning! Negative Liquidity: **₹{freely_withdrawable_cash:,.2f}**")

with col_w2:
    st.subheader("👤 Live Personal Wallet Sync")
    st.info(f"### Current Month Tax-Free Cash: **₹{current_month_personal_cash:,.2f}**")

with st.expander("🔍 Operational Breakdown"):
    st.write(f"**Step 1. Starting Gross Revenue ({current_month}):** ₹{current_active_revenue:,.2f}")
    st.write(f"💼 *Step 2. Deduct Salary Gross-Up Info:* Target payout of ₹{current_net_target:,.2f} + Company TDS reservation of ₹{current_monthly_tds:,.2f} = Total Gross Expense of **-₹{current_gross_salary:,.2f}**")
    st.write(f"🛠️ *Step 3. Deduct Overhead Expenses:* -₹{current_active_overhead:,.2f}")
    st.write(f"➡️ **Calculated Bank Balance (Liquid Leftover):** **₹{calculated_bank_balance:,.2f}**")
    st.write(f"⚠️ *Step 4. Isolate Corporate Tax Liability (25% of profit):* -₹{current_month_tax_liability:,.2f}")
    st.write("---")
    st.write(f"🏁 **Net Discovered Spendable Capital (Freely Withdrawable Cash):** **₹{freely_withdrawable_cash:,.2f}**")

st.write("---")

# ==========================================
# 7. FISCAL SUMMARY SCOREBOARDS
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

grand_annual_tax_free_personal_cash = float(df_engine["Total Tax-Free Personal Cash Flow"].sum())
total_base_tds = float(df_engine["Salary TDS (To Remit)"].sum())
total_surplus_tds = float(df_engine["Surplus TDS"].sum())
grand_total_personal_tds_remittance = total_base_tds + total_surplus_tds

st.write("---")
st.markdown("#### ⚡ Parallel Scenario Strategy: *Zero-Tax Salary Surplus Optimization*")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
col_s1.metric(label="Simulated Corporate Tax Due", value="₹0.00", delta="-100% Tax Drop", delta_color="inverse")
col_s2.metric(label="Grand Total Personal TDS To Remit", value=f"₹{grand_total_personal_tds_remittance:,.2f}")
col_s3.metric(label="Total Annual Tax-Free Payout", value=f"₹{grand_annual_tax_free_personal_cash:,.2f}")
col_s4.metric(label="Remaining Left Inside Company", value="₹0.00", delta="Fully Extracted", delta_color="normal")

st.write("---")

# ==========================================
# 8. SPREADSHEET MATRIX VIEW TABS WITH SUMMATION
# ==========================================
st.write("### 📋 12-Month Financial Spread Matrix Split-Ledgers")

tab_corp, tab_personal = st.tabs(["🏢 Company Perspective View", "👤 Personal Director Account View"])

with tab_corp:
    st.markdown("##### Corporate Inflows, Deductions, and Tax Liability Allocations")
    preview_df = df_engine[[
        "Month", "Status", "Gross Revenue", "Company Salary Expense (Gross)", "Salary TDS (To Remit)", "Projected Overhead",
        "Net Corporate Profit", "Corporate Tax Liability"
    ]]
    st.dataframe(preview_df, use_container_width=True)

with tab_personal:
    st.markdown("##### 100% Tax-Free Cash-Flow Inflow Ledger hitting your Personal Account")
    
    # Isolate base columns
    personal_df = df_engine[[
        "Month", "Status", "Company Salary Expense (Gross)", "Salary TDS (To Remit)", 
        "Net Take-Home Salary", "Gross Surplus", "Surplus TDS", "Net Surplus (After Tax)", 
        "Total Tax-Free Personal Cash Flow"
    ]].copy()
    
    # Rename matching specs
    personal_df = personal_df.rename(columns={
        "Company Salary Expense (Gross)": "Gross Salary",
        "Salary TDS (To Remit)": "TDS on Gross Salary",
        "Net Take-Home Salary": "Base Salary (After TDS)",
        "Net Surplus (After Tax)": "Surplus (After TDS)",
        "Total Tax-Free Personal Cash Flow": "Net Take-Home (Salary + Surplus)"
    })
    
    # Safe isolation list of columns to total up
    target_cols = ["Gross Salary", "TDS on Gross Salary", "Base Salary (After TDS)", "Gross Surplus", "Surplus TDS", "Surplus (After TDS)", "Net Take-Home (Salary + Surplus)"]
    
    # Explicitly compile sums as floats to prevent concatenation object alignment issues
    totals_row = {col: float(personal_df[col].sum()) for col in target_cols}
    totals_row["Month"] = "📈 TOTALS"
    totals_row["Status"] = "Full Financial Year Summary"
    
    # Bind cleanly inside a dummy frame and append
    df_summary_row = pd.DataFrame([totals_row])
    personal_df_with_total = pd.concat([personal_df, df_summary_row], ignore_index=True)
    
    st.dataframe(personal_df_with_total, use_container_width=True)
