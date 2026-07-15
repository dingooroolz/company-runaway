import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Corporate & Personal Wealth Engine", page_icon="💰", layout="wide")

st.title("💰 Script 5: Corporate Drain & Absolute Income Matrix Engine")
st.write("Drains corporate funds while mapping exact, itemized YTD income channels to precise personal tax regime slabs.")
st.write("---")

# ==========================================
# INDIAN NUMBER FORMATTING FUNCTION
# ==========================================
def format_indian_currency(val):
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
            
        return f"-₹{result}" if is_negative else f"₹{result}"
    except Exception:
        return f"₹{val}"

# ==========================================
# PROGRESSIVE SLAB CALCULATION ENGINE (NEW REGIME)
# ==========================================
def calculate_personal_tax(income):
    if income <= 400000:
        return 0.0
    
    tax = 0.0
    slabs = [
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, float('inf'), 0.30)
    ]
    
    for start, end, rate in slabs:
        if income > start:
            taxable_in_slab = min(income, end) - start
            tax += taxable_in_slab * rate
            
    if income <= 1200000:
        return 0.0
        
    return tax * 1.04

# ==========================================
# 2. INPUT CONSOLE (SIDEBAR CONTROLS)
# ==========================================
st.sidebar.header("📥 Financial Ledger Inputs")

st.sidebar.subheader("💵 Monthly Corporate Inflow & Overhead")
rev_received = st.sidebar.number_input("Revenue Already Received (This Month):", min_value=0.0, value=500000.0, step=50000.0)
rev_expected = st.sidebar.number_input("Additional Expected Revenue:", min_value=0.0, value=250000.0, step=50000.0)
overhead_incurred = st.sidebar.number_input("Expenses Already Billed / Paid:", min_value=0.0, value=250000.0, step=10000.0)
overhead_projected = st.sidebar.number_input("Expected Remaining Overhead:", min_value=0.0, value=124000.0, step=10000.0)

# --- NEW ABSOLUTE ITEMIZATION INPUT FIELDS ---
st.sidebar.write("---")
st.sidebar.subheader("👤 Historical YTD Absolute Income Matrix")
st.sidebar.info("Input the exact net amounts received in your personal account since April 1st:")

ytd_remuneration_net = st.sidebar.number_input("1. Director Remuneration (Net):", min_value=0.0, value=500000.0, step=50000.0)
ytd_bonus_net = st.sidebar.number_input("2. Salary Bonuses (Net):", min_value=0.0, value=100000.0, step=10000.0)
ytd_dividends_net = st.sidebar.number_input("3. Retained Earnings / Dividends (Net):", min_value=0.0, value=100000.0, step=10000.0)
ytd_rent_gross = st.sidebar.number_input("4. House Rent Received (Gross):", min_value=0.0, value=0.0, step=10000.0,
                                        help="Gross rent received. The app automatically slices off a 30% statutory deduction for upkeep before taxing it.")
ytd_other_income = st.sidebar.number_input("5. Income from Other Sources:", min_value=0.0, value=0.0, step=5000.0)

rem_future = st.sidebar.number_input("Projected Future Remuneration (Rest of Year Gross):", min_value=0.0, value=500000.0, step=50000.0)
total_months_to_amortize = st.sidebar.slider("Total Months to Spread Tax Across (Including Current):", min_value=1, max_value=12, value=9)

st.sidebar.write("---")
st.sidebar.subheader("🏦 Personal Savings Vault Inputs")
savings_initial = st.sidebar.number_input("Current Savings Balance (Baseline):", min_value=0.0, value=500000.0, step=50000.0)
advance_tax_paid = st.sidebar.number_input("Personal Advance Taxes Paid So Far (YTD):", min_value=0.0, value=0.0, step=10000.0)
personal_tax_arrears = st.sidebar.number_input("Personal Tax Arrears from Previous Years:", min_value=0.0, value=0.0, step=5000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏛️ Corporate Compliance & Credit Adjustments")
corp_advance_tax = st.sidebar.number_input("Company Advance Taxes Paid So Far (YTD):", min_value=0.0, value=0.0, step=10000.0)
corp_tax_arrears = st.sidebar.number_input("Company Tax Arrears from Previous Years:", min_value=0.0, value=0.0, step=5000.0)
base_tds_rate = st.sidebar.slider("Standard Transactional TDS Rate (%)", min_value=0.0, max_value=30.0, value=10.0, step=1.0) / 100.0

# ==========================================
# 3. MATHEMATICAL COMPUTATION MATRICES
# ==========================================
# 1. Gross Up Calculations Based on Exact Inputs
# Remuneration and Bonuses share the standard corporate base TDS filter
assumed_ytd_rem_gross = ytd_remuneration_net / (1.0 - base_tds_rate) if base_tds_rate < 1.0 else ytd_remuneration_net
assumed_ytd_rem_tds = assumed_ytd_rem_gross - ytd_remuneration_net

assumed_ytd_bonus_gross = ytd_bonus_net / (1.0 - base_tds_rate) if base_tds_rate < 1.0 else ytd_bonus_net
assumed_ytd_bonus_tds = assumed_ytd_bonus_gross - ytd_bonus_net

# Dividends hit standard 10% withholding under Section 194
assumed_ytd_div_gross = ytd_dividends_net / 0.90
assumed_ytd_div_tds = assumed_ytd_div_gross - ytd_dividends_net

# Rental Income drops 30% automatically for statutory standard deduction
taxable_rent_income = ytd_rent_gross * 0.70

# Summing total YTD Net Cash for ledger references
rem_ytd = ytd_remuneration_net + ytd_bonus_net + ytd_dividends_net + ytd_rent_gross + ytd_other_income

# 2. Corporate Account Optimization Logic
total_monthly_revenue = rev_received + rev_expected
total_month_overhead = overhead_incurred + overhead_projected
free_floating_operating_cash = total_monthly_revenue - total_month_overhead

net_corporate_arrears_burden = max(0.0, corp_tax_arrears - corp_advance_tax)
cash_available_for_remuneration_pool = max(0.0, free_floating_operating_cash - net_corporate_arrears_burden)

if cash_available_for_remuneration_pool <= 0:
    max_safe_gross_remuneration = 0.0
    max_safe_net_takehome = 0.0
    calculated_immediate_tds = 0.0
    annual_tax_liability = 0.0
    total_projected_annual_gross = 0.0
else:
    max_safe_gross_remuneration = cash_available_for_remuneration_pool
    base_net_takehome = max_safe_gross_remuneration * (1.0 - base_tds_rate)
    calculated_immediate_tds = max_safe_gross_remuneration - base_net_takehome
    max_safe_net_takehome = base_net_takehome

    # Full Annual Personal Income Model using explicitly itemized gross pools
    total_projected_annual_gross = (
        assumed_ytd_rem_gross + 
        assumed_ytd_bonus_gross + 
        max_safe_gross_remuneration + 
        rem_future + 
        assumed_ytd_div_gross + 
        taxable_rent_income + 
        ytd_other_income
    )
    annual_tax_liability = calculate_personal_tax(total_projected_annual_gross)

# 3. Personal Savings & Dynamic Tax Amortization
combined_total_savings = savings_initial + max_safe_net_takehome
total_gross_personal_liabilities = annual_tax_liability + personal_tax_arrears

# Dynamic total tax credit pooling across all discrete tracks
net_withheld_credits = (
    advance_tax_paid + 
    assumed_ytd_rem_tds + 
    assumed_ytd_bonus_tds + 
    assumed_ytd_div_tds + 
    calculated_immediate_tds
)
outstanding_total_tax_shortfall = max(0.0, total_gross_personal_liabilities - net_withheld_credits)

# Amortize tax target over custom month ceiling (including current month)
amortized_monthly_tax_runway_target = outstanding_total_tax_shortfall / total_months_to_amortize if total_months_to_amortize > 0 else outstanding_total_tax_shortfall
current_immediate_tax_reserve = personal_tax_arrears + amortized_monthly_tax_runway_target
safely_disposable_income = combined_total_savings - current_immediate_tax_reserve

# ==========================================
# 4. SIDE-BY-SIDE LEDGER DISPLAY RENDER
# ==========================================
col_corp, col_pers = st.columns(2)

with col_corp:
    st.subheader("🏢 Corporate Optimization Ledger")
    st.write("Draining corporate liquid funds safely:")
    
    st.metric(label="🚀 Monthly Max Net Take-Home Payout", value=format_indian_currency(max_safe_net_takehome))
    st.metric(label="🔒 Mandatory TDS Leave-Behind", value=format_indian_currency(calculated_immediate_tds))
    
    corp_ledger = [
        {"Matrix Item": "Gross Inflow Focus", "Value": format_indian_currency(total_monthly_revenue)},
        {"Matrix Item": "Deduct: Monthly Overheads", "Value": f"- {format_indian_currency(total_month_overhead)}"},
        {"Matrix Item": "Available Cash Allocation", "Value": format_indian_currency(free_floating_operating_cash)},
        {"Matrix Item": "Deduct: Corporate Arrears (Net)", "Value": f"- {format_indian_currency(net_corporate_arrears_burden)}"},
        {"Matrix Item": "Assigned Gross Remuneration", "Value": format_indian_currency(max_safe_gross_remuneration)}
    ]
    st.table(pd.DataFrame(corp_ledger))

with col_pers:
    st.subheader("🏦 Personal Savings & Amortized Tax Ledger")
    st.write("Sequential tracking with itemized asset entries:")
    
    st.metric(label="💎 Safely Disposable Income (Current Month)", value=format_indian_currency(safely_disposable_income))
    st.metric(label="📉 Monthly Tax Savings Target", value=format_indian_currency(amortized_monthly_tax_runway_target), delta="Target Budget Allocation Per Month", delta_color="inverse")
    
    pers_ledger = [
        {"Sequence Steps": "1. Current Personal Savings Balance", "Value": format_indian_currency(savings_initial), "Context Description": "Core starting savings account balance baseline."},
        {"Sequence Steps": "2. New Monthly Fund Influx", "Value": format_indian_currency(max_safe_net_takehome), "Context Description": "Fresh net extraction from corporate clearing engine."},
        {"Sequence Steps": "3. Total Summation Balance", "Value": format_indian_currency(combined_total_savings), "Context Description": "Aggregated cash pool inside your account right now."},
        {"Sequence Steps": "4. Deduct: Total Current Month Reserves", "Value": f"- {format_indian_currency(current_immediate_tax_reserve)}", "Context Description": f"Includes past arrears ({format_indian_currency(personal_tax_arrears)}) + this month's tax share ({format_indian_currency(amortized_monthly_tax_runway_target)})."}
    ]
    st.table(pd.DataFrame(pers_ledger))

st.write("---")
st.subheader("🛡️ Itemized Income Profile Audit Summary")
st.markdown(f"Your absolute tracked annual gross income projection has reached **{format_indian_currency(total_projected_annual_gross)}**, driven by your custom itemized YTD entries and current monthly clearing models. Your true full-year pending tax shortfall is **{format_indian_currency(outstanding_total_tax_shortfall)}**.") 
st.info(f"💡 **The Capital Multiplier Strategy:** The engine has safely isolated this month's target runway share of **{format_indian_currency(amortized_monthly_tax_runway_target)}** to protect your year-end compliance while keeping **{format_indian_currency(safely_disposable_income)}** fully liquid for your use today.")
