import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Corporate & Personal Wealth Engine", page_icon="💰", layout="wide")

st.title("💰 Script 5: Corporate Drain & Dual-Source Personal Wealth Engine")
st.write("Optimizes maximum corporate extraction while separating historic YTD drawings into Remuneration vs. Dividends for exact tax slab compliance.")
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
rem_ytd = st.sidebar.number_input("Total Historic Cash Inflows Received YTD Net:", min_value=0.0, value=700000.0, step=50000.0,
                                 help="Total cash that flowed from your company to your personal account since April 1st.")

# --- NEW DYNAMIC BIFURCATION SLIDER ---
rem_split_pct = st.sidebar.slider("What % of this YTD historic cash was Director Remuneration?", min_value=0.0, max_value=100.0, value=100.0, step=5.0,
                                  help="The remaining % will automatically be calculated and treated as pre-taxed corporate dividends.")

rem_future = st.sidebar.number_input("Projected Future Remuneration (Rest of Year):", min_value=0.0, value=0.0, step=50000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏦 Personal Savings Vault Inputs")
savings_initial = st.sidebar.number_input("Starting Personal Savings Balance (Before Payouts):", min_value=0.0, value=500000.0, step=50000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏛️ Tax Credits & Arrears")
advance_tax_paid = st.sidebar.number_input("Advance Taxes Paid So Far (YTD):", min_value=0.0, value=0.0, step=10000.0)
past_tax_arrears = st.sidebar.number_input("Pending Tax Arrears from Previous Years:", min_value=0.0, value=0.0, step=5000.0)
base_tds_rate = st.sidebar.slider("Standard Transactional TDS Rate (%)", min_value=0.0, max_value=30.0, value=10.0, step=1.0) / 100.0

# ==========================================
# 3. MATHEMATICAL COMPUTATION MATRICES
# ==========================================
# Process the YTD split from user inputs
ytd_remuneration_net = rem_ytd * (rem_split_pct / 100.0)
ytd_dividends_net = rem_ytd * (1.0 - (rem_split_pct / 100.0))

# Convert net values back to gross figures to find true tax exposure
# Remuneration is subject to standard base TDS withholding rules
assumed_ytd_rem_gross = ytd_remuneration_net / (1.0 - base_tds_rate) if base_tds_rate < 1.0 else ytd_remuneration_net
assumed_ytd_rem_tds = assumed_ytd_rem_gross - ytd_remuneration_net

# Dividends are also hit with a standard 10% statutory TDS under Section 194
assumed_ytd_div_gross = ytd_dividends_net / 0.90
assumed_ytd_div_tds = assumed_ytd_div_gross - ytd_dividends_net

# Corporate Operations Logic
total_monthly_revenue = rev_received + rev_expected
total_month_overhead = overhead_incurred + overhead_projected
free_floating_operating_cash = total_monthly_revenue - total_month_overhead
cash_available_for_remuneration_pool = free_floating_operating_cash - past_tax_arrears

if cash_available_for_remuneration_pool <= 0:
    max_safe_gross_remuneration = 0.0
    max_safe_net_takehome = 0.0
    calculated_immediate_tds = 0.0
    annual_tax_liability = 0.0
    total_projected_annual_gross = 0.0
    uncovered_tax_shortfall = 0.0
else:
    max_safe_gross_remuneration = cash_available_for_remuneration_pool
    base_net_takehome = max_safe_gross_remuneration * (1.0 - base_tds_rate)
    calculated_immediate_tds = max_safe_gross_remuneration - base_net_takehome

    # Absolute Total Personal Gross Income (Remuneration + Dividends stacked sequentially)
    total_projected_annual_gross = (assumed_ytd_rem_gross + max_safe_gross_remuneration + rem_future) + assumed_ytd_div_gross
    annual_tax_liability = calculate_personal_tax(total_projected_annual_gross)
    
    # Sum up all tax credits already collected by the tax portal
    total_tax_credits_cleared = advance_tax_paid + assumed_ytd_rem_tds + assumed_ytd_div_tds + calculated_immediate_tds
    uncovered_tax_shortfall = (annual_tax_liability + past_tax_arrears) - total_tax_credits_cleared
    
    if uncovered_tax_shortfall > 0:
        max_safe_net_takehome = base_net_takehome - uncovered_tax_shortfall
        max_safe_net_takehome = max(0.0, max_safe_net_takehome)
    else:
        max_safe_net_takehome = base_net_takehome

# Personal Savings Tracker updates
total_drawings_injected = rem_ytd + max_safe_net_takehome
updated_savings_balance = savings_initial + total_drawings_injected

# Calculate personal tax outstanding balances
outstanding_personal_tax_due = max(0.0, annual_tax_liability + past_tax_arrears - (advance_tax_paid + assumed_ytd_rem_tds + assumed_ytd_div_tds + calculated_immediate_tds))
reserve_disposable_income = updated_savings_balance - outstanding_personal_tax_due

# ==========================================
# 4. SIDE-BY-SIDE MOBILE LAYOUT RENDER
# ==========================================
col_corp, col_pers = st.columns(2)

# ------------------------------------------
# LEFT VIEWPORT: CORPORATE ACCOUNT CLEARING
# ------------------------------------------
with col_corp:
    st.subheader("🏢 Corporate Optimization Ledger")
    st.write("Draining corporate liquid funds safely:")
    
    st.metric(label="🚀 Monthly Max Net Take-Home Payout", value=format_indian_currency(max_safe_net_takehome))
    st.metric(label="🔒 Mandatory TDS Leave-Behind", value=format_indian_currency(calculated_immediate_tds))
    
    corp_ledger = [
        {"Matrix Item": "Gross Inflow Focus", "Value": format_indian_currency(total_monthly_revenue)},
        {"Matrix Item": "Deduct: Monthly Overheads", "Value": f"- {format_indian_currency(total_month_overhead)}"},
        {"Matrix Item": "Available Cash Allocation", "Value": format_indian_currency(free_floating_operating_cash)},
        {"Matrix Item": "Assigned Gross Remuneration", "Value": format_indian_currency(max_safe_gross_remuneration)}
    ]
    st.table(pd.DataFrame(corp_ledger))

# ------------------------------------------
# RIGHT VIEWPORT: PERSONAL SAVINGS & DISPOSABLE INCOME
# ------------------------------------------
with col_pers:
    st.subheader("🏦 Personal Savings & Tax Asset Ledger")
    st.write("Real-time accumulation and source tracking:")
    
    st.metric(label="💎 True Reserve Disposable Income", value=format_indian_currency(reserve_disposable_income), delta="Clear Fluid Capital")
    st.metric(label="🏛️ Outstanding Year-End Tax Due", value=format_indian_currency(outstanding_personal_tax_due), delta="Pending Slab Settlement Liability", delta_color="inverse")
    
    pers_ledger = [
        {"Matrix Item": "Initial Savings Baseline", "Value": format_indian_currency(savings_initial)},
        {"Matrix Item": "Add: YTD Remuneration (Net Portion)", "Value": format_indian_currency(ytd_remuneration_net)},
        {"Matrix Item": "Add: YTD Dividends (Net Portion)", "Value": format_indian_currency(ytd_dividends_net)},
        {"Matrix Item": "Add: Current Month Net Influx", "Value": format_indian_currency(max_safe_net_takehome)},
        {"Matrix Item": "⭐ Updated Savings Account Balance", "Value": format_indian_currency(updated_savings_balance)}
    ]
    st.table(pd.DataFrame(pers_ledger))

st.write("---")
st.subheader("🛡️ Source Bifurcation Audit Summary")
st.markdown(f"Out of your **{format_indian_currency(rem_ytd)}** historic YTD cash withdrawals, the engine has successfully isolated **{format_indian_currency(ytd_remuneration_net)}** as standard corporate remuneration and **{format_indian_currency(ytd_dividends_net)}** as post-tax corporate dividends. This allows the progressive tax calculations to remain perfectly compliant at your true projected annual gross of **{format_indian_currency(total_projected_annual_gross)}**.")
