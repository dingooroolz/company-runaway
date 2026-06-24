import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Advance Tax Engine (Script 2)", page_icon="📈", layout="wide")

st.title("💼 Script 2: True Free Cash & Dynamic Quarterly Advance Tax Engine")
st.write("Calculates real-world baseline liquidity while running progressive quarterly advance tax installment schedules.")
st.write("---")

# Define the Indian Financial Year sequence (April to March)
FY_MONTHS = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# Map months to their respective financial quarters
MONTH_TO_QUARTER_MAP = {
    "April": "Q1", "May": "Q1", "June": "Q1",
    "July": "Q2", "August": "Q2", "September": "Q2",
    "October": "Q3", "November": "Q3", "December": "Q3",
    "January": "Q4", "February": "Q4", "March": "Q4"
}

# Default baseline assumptions
BASELINE_REV = 500000
BASELINE_NET_SALARY = 300000
BASELINE_OH = 150000

# ==========================================
# INDIAN NUMBER FORMATTING FUNCTION
# ==========================================
def format_indian_currency(val):
    """
    Formats a numeric value into the Indian comma system (e.g., 12,34,567.89)
    """
    try:
        val = float(val)
        is_negative = val < 0
        val = abs(val)
        
        s = f"{val:.2f}"
        parts = s.split(".")
        int_part = parts[0]
        dec_part = parts[1]
        
        if len(int_part) <= 3:
            result = int_part
        else:
            last_three = int_part[-3:]
            remaining = int_part[:-3]
            remaining_with_commas = re.sub(r'(.)(?=(..)+$)', r'\1,', remaining)
            result = f"{remaining_with_commas},{last_three}"
            
        return f"-₹{result}.{dec_part}" if is_negative else f"₹{result}.{dec_part}"
    except Exception:
        return f"₹{val}"

# ==========================================
# 2. AUTOMATED SALARY GROSS-UP FUNCTION
# ==========================================
def calculate_gross_salary_and_tds(target_net_monthly):
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
current_quarter = MONTH_TO_QUARTER_MAP[current_month]

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
st.sidebar.markdown(f"**Active Month Context: {current_month} ({current_quarter})**")

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
    m_quarter = MONTH_TO_QUARTER_MAP[m_name]
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
        
    standard_net_profit = max(0.0, float(revenue - gross_sal - overhead))
    standard_corp_tax = float(standard_net_profit * 0.25)
    
    # Parallel Overhead Surplus Simulation Math
    gross_surplus = standard_net_profit 
    surplus_tds = float(gross_surplus * 0.312) if gross_surplus > 0 else 0.0
    net_surplus_payout = max(0.0, gross_surplus - surplus_tds)
    total_net_personal_takehome = float(net_sal + net_surplus_payout)
    
    final_monthly_records.append({
        "Month": m_name,
        "Quarter": m_quarter,
        "Status": status,
        "Gross Revenue": float(revenue),
        "Company Salary Expense (Gross)": float(gross_sal),
        "Salary TDS (To Remit)": float(tds_val),
        "Net Take-Home Salary": float(net_sal),
        "Projected Overhead": float(overhead),
        "Net Corporate Profit": float(standard_net_profit),
        "Corporate Tax Liability": float(standard_corp_tax),
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
        st.success(f"### Freely Withdrawable Cash: **{format_indian_currency(freely_withdrawable_cash)}**")
    else:
        st.error(f"### Shortfall Warning! Negative Liquidity: **{format_indian_currency(freely_withdrawable_cash)}**")

with col_w2:
    st.subheader("👤 Live Personal Wallet Sync")
    st.info(f"### Current Month Tax-Free Cash: **{format_indian_currency(current_month_personal_cash)}**")

with st.expander("🔍 Operational Breakdown"):
    st.write(f"**Step 1. Starting Gross Revenue ({current_month}):** {format_indian_currency(current_active_revenue)}")
    st.write(f"💼 *Step 2. Deduct Salary Gross-Up Info:* Target payout of {format_indian_currency(current_net_target)} + Company TDS reservation of {format_indian_currency(current_monthly_tds)} = Total Gross Expense of **-{format_indian_currency(current_gross_salary)}**")
    st.write(f"🛠️ *Step 3. Deduct Overhead Expenses:* -{format_indian_currency(current_active_overhead)}")
    st.write(f"➡️ **Calculated Bank Balance (Liquid Leftover):** **{format_indian_currency(calculated_bank_balance)}**")
    st.write(f"⚠️ *Step 4. Isolate Corporate Tax Liability (25% of profit):* -{format_indian_currency(current_month_tax_liability)}")
    st.write("---")
    st.write(f"🏁 **Net Discovered Spendable Capital (Freely Withdrawable Cash):** **{format_indian_currency(freely_withdrawable_cash)}**")

st.write("---")

# ==========================================
# 7. QUARTERLY ADVANCE TAX RESERVE TABLE
# ==========================================
st.subheader("📆 Corporate Quarterly Advance Tax Estimation Schedule")
st.write("Tracks your cumulative tax legal requirements dynamically based on your current selection phase.")

q_order = ["Q1", "Q2", "Q3", "Q4"]
curr_q_idx = q_order.index(current_quarter)

total_predicted_annual_tax = float(df_engine["Corporate Tax Liability"].sum())

quarterly_schedule_data = []
cumulative_paid_tracker = 0.0

advance_tax_rules = {
    "Q1": {"target_pct": 15, "deadline": "June 15"},
    "Q2": {"target_pct": 45, "deadline": "September 15"},
    "Q3": {"target_pct": 75, "deadline": "December 15"},
    "Q4": {"target_pct": 100, "deadline": "March 15"}
}

for q_idx, q_name in enumerate(q_order):
    q_rev = float(df_engine[df_engine["Quarter"] == q_name]["Gross Revenue"].sum())
    q_profit = float(df_engine[df_engine["Quarter"] == q_name]["Net Corporate Profit"].sum())
    q_tax_generated = float(df_engine[df_engine["Quarter"] == q_name]["Corporate Tax Liability"].sum())
    
    if q_idx < curr_q_idx:
        q_status = "🔒 Locked (Historical Actuals)"
    elif q_idx == curr_q_idx:
        q_status = "⚡ Active (Current Phase)"
    else:
        q_status = "🔮 Projected Phase"
        
    target_percentage = advance_tax_rules[q_name]["target_pct"]
    deadline_date = advance_tax_rules[q_name]["deadline"]
    
    cumulative_required_reserve = total_predicted_annual_tax * (target_percentage / 100.0)
    net_installment_due_this_quarter = max(0.0, cumulative_required_reserve - cumulative_paid_tracker)
    cumulative_paid_tracker = cumulative_required_reserve
    
    quarterly_schedule_data.append({
        "Quarter": q_name,
        "Phase Status": q_status,
        "Quarterly Revenue": q_rev,
        "Quarterly Net Profit": q_profit,
        "Tax Liability Added": q_tax_generated,
        "Legal Mandate (%)": f"{target_percentage}%",
        "Cumulative Reserve Needed": cumulative_required_reserve,
        "Net Installment Outflow Due": net_installment_due_this_quarter,
        "Compliance Deadline": deadline_date
    })

df_quarterly = pd.DataFrame(quarterly_schedule_data)

df_quarterly_render = df_quarterly.copy()
currency_cols = ["Quarterly Revenue", "Quarterly Net Profit", "Tax Liability Added", "Cumulative Reserve Needed", "Net Installment Outflow Due"]
for col in currency_cols:
    df_quarterly_render[col] = df_quarterly_render[col].apply(format_indian_currency)

st.dataframe(df_quarterly_render, use_container_width=True)
st.write("---")

# ==========================================
# 8. FISCAL SUMMARY SCOREBOARDS & PERCENTAGES
# ==========================================
st.subheader("📊 Full-Year Fiscal Projections (EOY Estimates)")

# FIXED: Safely calculating all summary values from the loaded dataframe
total_12_month_actual = float(df_engine["Gross Revenue"].sum()) if df_engine["Gross Revenue"].sum() > 0 else 1.0
total_corporate_tax = float(df_engine["Corporate Tax Liability"].sum())
total_full_year_net_profit = float(df_engine["Net Corporate Profit"].sum())
profit_after_corporate_tax = max(0.0, float(total_full_year_net_profit - total_corporate_tax))
total_annual_overhead = float(df_engine["Projected Overhead"].sum())
total_annual_gross_salary = float(df_engine["Company Salary Expense (Gross)"].sum())
total_baseline_salary_tds = float(df_engine["Salary TDS (To Remit)"].sum())

pct_expenses = ((total_annual_overhead + total_annual_gross_salary) / total_12_month_actual) * 100
pct_tax = (total_corporate_tax / total_12_month_actual) * 100
pct_retained = (profit_after_corporate_tax / total_12_month_actual) * 100
pct_baseline_tds = (total_baseline_salary_tds / total_12_month_actual) * 100

st.markdown("#### Baseline Strategy (Current Input Configuration)")
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric(label="Total Annual Revenue", value=format_indian_currency(total_12_month_actual))
col_m2.metric(label="Total Annual Company Expenses", value=format_indian_currency(total_annual_overhead + total_annual_gross_salary), delta=f"{pct_expenses:.1f}% of Rev", delta_color="inverse")
col_m3.metric(label="What Company Owes as Corporate Tax", value=format_indian_currency(total_corporate_tax), delta=f"{pct_tax:.1f}% of Rev", delta_color="inverse")
col_m4.metric(label="Company Profits After Corporate Tax", value=format_indian_currency(profit_after_corporate_tax), delta=f"{pct_retained:.1f}% of Rev", delta_color="normal")
col_m5.metric(label="Baseline Salary TDS Remitted", value=format_indian_currency(total_baseline_salary_tds), delta=f"{pct_baseline_tds:.1f}% of Rev", delta_color="inverse")

st.write("---")

# ==========================================
# 9. SPREADSHEET MATRIX VIEW TABS WITH SUMMATION
# ==========================================
st.write("### 📋 12-Month Financial Spread Matrix Split-Ledgers")

tab_corp, tab_personal = st.tabs(["🏢 Company Perspective View", "👤 Personal Director Account View"])

with tab_corp:
    st.markdown("##### Corporate Inflows, Deductions, and Tax Liability Allocations")
    preview_df = df_engine[[
        "Month", "Status", "Gross Revenue", "Company Salary Expense (Gross)", "Salary TDS (To Remit)", "Projected Overhead",
        "Net Corporate Profit", "Corporate Tax Liability"
    ]].copy()
    
    corp_cols = ["Gross Revenue", "Company Salary Expense (Gross)", "Salary TDS (To Remit)", "Projected Overhead", "Net Corporate Profit", "Corporate Tax Liability"]
    corp_totals = {col: float(preview_df[col].sum()) for col in corp_cols}
    corp_totals["Month"] = "📈 TOTALS"
    corp_totals["Status"] = "Full Financial Year Summary"
    
    preview_df_with_total = pd.concat([preview_df, pd.DataFrame([corp_totals])], ignore_index=True)
    for col in corp_cols:
        preview_df_with_total[col] = preview_df_with_total[col].apply(format_indian_currency)
    st.dataframe(preview_df_with_total, use_container_width=True)

with tab_personal:
    st.markdown("##### 100% Tax-Free Cash-Flow Inflow Ledger hitting your Personal Account")
    
    personal_df = df_engine[[
        "Month", "Status", "Company Salary Expense (Gross)", "Salary TDS (To Remit)", 
        "Net Take-Home Salary", "Gross Surplus", "Surplus TDS", "Net Surplus (After Tax)", 
        "Total Tax-Free Personal Cash Flow"
    ]].copy()
    
    personal_df = personal_df.rename(columns={
        "Company Salary Expense (Gross)": "Gross Salary",
        "Salary TDS (To Remit)": "TDS on Gross Salary",
        "Net Take-Home Salary": "Base Salary (After TDS)",
        "Net Surplus (After Tax)": "Surplus (After TDS)",
        "Total Tax-Free Personal Cash Flow": "Net Take-Home (Salary + Surplus)"
    })
    
    target_cols = ["Gross Salary", "TDS on Gross Salary", "Base Salary (After TDS)", "Gross Surplus", "Surplus TDS", "Surplus (After TDS)", "Net Take-Home (Salary + Surplus)"]
    totals_row = {col: float(personal_df[col].sum()) for col in target_cols}
    totals_row["Month"] = "📈 TOTALS"
    totals_row["Status"] = "Full Financial Year Summary"
    
    personal_df_with_total = pd.concat([personal_df, pd.DataFrame([totals_row])], ignore_index=True)
    for col in target_cols:
        personal_df_with_total[col] = personal_df_with_total[col].apply(format_indian_currency)
    st.dataframe(personal_df_with_total, use_container_width=True)
