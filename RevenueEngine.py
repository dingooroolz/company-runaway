import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Corporate & Personal Wealth Engine", page_icon="💰", layout="wide")

st.title("💰 Script 5: Corporate Drain & Amortized Tax Runway Engine")
st.write("Drains corporate funds efficiently while accurately limiting your maximum personal payout to the company's actual liquid cash.")
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

st.sidebar.write("---")
st.sidebar.subheader("👤 Historical YTD Inflows & Bifurcation")
rem_ytd = st.sidebar.number_input("Total Historic Cash Inflows Received YTD Net:", min_value=0.0, value=700000.0, step=50000.0)
rem_split_pct = st.sidebar.slider("What % of this YTD historic cash was Director Remuneration?", min_value=0.0, max_value=100.0, value=100.0, step=5.0)
rem_future = st.sidebar.number_input("Projected Future Remuneration (Rest of Year Gross):", min_value=0.0, value=500000.0, step=50000.0)
months_remaining = st.sidebar.slider("Months Remaining in FY (To Amortize Tax Across):", min_value=1, max_value=12, value=8)

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
# 1. Process YTD Split Details
ytd_remuneration_net = rem_ytd * (rem_split_pct / 100.0)
ytd_dividends_net = rem_ytd * (1.0 - (rem_split_pct / 100.0))

assumed_ytd_rem_gross = ytd_remuneration_net / (1.0 - base_tds_rate) if base_tds_rate < 1.0 else ytd_remuneration_net
assumed_ytd_rem_tds = assumed_ytd_rem_gross - ytd_remuneration_net

assumed_ytd_div_gross = ytd_dividends_net / 0.90
assumed_ytd_div_tds = assumed_ytd_div_gross - ytd_dividends_net

# 2. Corporate Account Optimization Logic (Factoring Liquid Bounds)
total_monthly_revenue = rev_received + rev_expected
total_month_overhead = overhead_incurred + overhead_projected
free_floating_operating_cash = total_monthly_revenue - total_month_overhead

# Net corporate liabilities to clear this month (Arrears offset by corporate advance taxes paid)
net_corporate_arrears_burden = max(0.0, corp_tax_arrears - corp_advance_tax)

# --- FIX LOGIC: Advance tax credits cannot exceed your available monthly liquid cash pool ---
cash_available_for_remuneration_pool = free_floating_operating_cash - net_corporate_arrears_burden
cash_available_for_remuneration_pool = max(0.0, cash_available_for_remuneration_pool)

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

    # Full Annual Personal Income Model
    total_projected_annual_gross = (assumed_ytd_rem_gross + max_safe_gross_remuneration + rem_future) + assumed_ytd_div_gross
    annual_tax_liability = calculate_personal_tax(total_projected_annual_gross)

# 3. Personal Savings Equations 
combined_total_savings = savings_initial + max_safe_net_takehome
total_gross_personal_liabilities = annual_tax_liability + personal_tax_arrears
net_withheld_credits = advance_tax_paid + assumed_ytd_rem_tds + assumed_ytd_div_tds + calculated_immediate_tds
outstanding_total_tax_shortfall = max(0.0, total_gross_personal_liabilities - net_withheld_credits)

amortized_monthly_tax_runway_target = outstanding_total_tax_shortfall / months_remaining if months_remaining > 0 else outstanding_total_tax_shortfall
current_immediate_tax_reserve = personal_tax_arrears
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
    st.write("Sequential tracking with smart tax distribution:")
    
    st.metric(label="💎 Safely Disposable Income (Current Month)", value=format_indian_currency(safely_disposable_income))
    st.metric(label="📉 Monthly Tax Savings Target", value=format_indian_currency(amortized_monthly_tax_runway_target), delta="Target Allocation Per Month Left", delta_color="inverse")
    
    pers_ledger = [
        {"Sequence Steps": "1. Current Personal Savings Balance", "Value": format_indian_currency(savings_initial), "Context Description": "Core starting savings account balance baseline."},
        {"Sequence Steps": "2. New Monthly Fund Influx", "Value": format_indian_currency(max_safe_net_takehome), "Context Description": "Fresh net extraction from corporate clearing engine."},
        {"Sequence Steps": "3. Total Summation Balance", "Value": format_indian_currency(combined_total_savings), "Context Description": "Aggregated cash pool inside your account right now."},
        {"Sequence Steps": "4. Deduct: Immediate Past Year Arrears", "Value": f"- {format_indian_currency(current_immediate_tax_reserve)}", "Context Description": "Legacy debt subtracted directly to secure current year safety."}
    ]
    st.table(pd.DataFrame(pers_ledger))

st.write("---")
st.subheader("🛡️ Strategic Tax Runway Summary")
st.markdown(f"Your total projected personal tax liability across the entire financial year is **{format_indian_currency(annual_tax_liability)}**. After accounting for all credits, your true outstanding net tax gap is **{format_indian_currency(outstanding_total_tax_shortfall)}**.") 
st.info(f"💡 **The Capital Multiplier Strategy:** You only need to save an average of **{format_indian_currency(amortized_monthly_tax_runway_target)}** per month over your remaining **{months_remaining} months**, keeping **{format_indian_currency(safely_disposable_income)}** completely fluid and at your disposal right now.")
