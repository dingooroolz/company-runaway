import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Corporate & Personal Wealth Engine", page_icon="💰", layout="wide")

st.title("💰 Script 5: Corporate Drain & Personal Wealth Engine")
st.write("Drains corporate funds efficiently while isolating your personal savings, past tax arrears, slab liabilities, and safely disposable income.")
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
rem_future = st.sidebar.number_input("Projected Future Remuneration (Rest of Year):", min_value=0.0, value=0.0, step=50000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏦 Personal Savings Vault Inputs")
savings_initial = st.sidebar.number_input("Current Savings Balance (Baseline):", min_value=0.0, value=500000.0, step=50000.0)
advance_tax_paid = st.sidebar.number_input("Personal Advance Taxes Paid So Far (YTD):", min_value=0.0, value=0.0, step=10000.0)
# --- NEW PERSONAL TAX ARREARS FIELD ---
personal_tax_arrears = st.sidebar.number_input("Personal Tax Arrears from Previous Years:", min_value=0.0, value=0.0, step=5000.0,
                                               help="Outstanding personal tax debts from prior fiscal cycles requiring clearance out of personal savings.")

st.sidebar.write("---")
st.sidebar.subheader("🏛️ Corporate Settings")
corp_tax_arrears = st.sidebar.number_input("Company Tax Arrears from Previous Years:", min_value=0.0, value=0.0, step=5000.0)
base_tds_rate = st.sidebar.slider("Standard Transactional TDS Rate (%)", min_value=0.0, max_value=30.0, value=10.0, step=1.0) / 100.0

# ==========================================
# 3. MATHEMATICAL COMPUTATION MATRICES
# ==========================================
# 1. Process YTD Split Details
ytd_remuneration_net = rem_ytd * (rem_split_pct / 100.0)
ytd_dividends_net = rem_ytd * (1.0 - (rem_split_pct / 100.0))

# Gross up variables to map to standard regime brackets
assumed_ytd_rem_gross = ytd_remuneration_net / (1.0 - base_tds_rate) if base_tds_rate < 1.0 else ytd_remuneration_net
assumed_ytd_rem_tds = assumed_ytd_rem_gross - ytd_remuneration_net

assumed_ytd_div_gross = ytd_dividends_net / 0.90
assumed_ytd_div_tds = assumed_ytd_div_gross - ytd_dividends_net

# 2. Corporate Account Optimization Logic
total_monthly_revenue = rev_received + rev_expected
total_month_overhead = overhead_incurred + overhead_projected
free_floating_operating_cash = total_monthly_revenue - total_month_overhead
cash_available_for_remuneration_pool = free_floating_operating_cash - corp_tax_arrears

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

    # Full Annual Personal Income Model
    total_projected_annual_gross = (assumed_ytd_rem_gross + max_safe_gross_remuneration + rem_future) + assumed_ytd_div_gross
    annual_tax_liability = calculate_personal_tax(total_projected_annual_gross)
    
    # Calculate slab deficit adjustment check
    total_tax_credits_cleared = advance_tax_paid + assumed_ytd_rem_tds + assumed_ytd_div_tds + calculated_immediate_tds
    uncovered_tax_shortfall = (annual_tax_liability + personal_tax_arrears) - total_tax_credits_cleared
    
    if uncovered_tax_shortfall > 0:
        max_safe_net_takehome = base_net_takehome - uncovered_tax_shortfall
        max_safe_net_takehome = max(0.0, max_safe_net_takehome)
    else:
        max_safe_net_takehome = base_net_takehome

# --- USER MANDATED 4-STEP PERSONAL SAVINGS EQUATIONS (UPDATED FOR PERSONAL ARREARS) ---
# Step 1: Current Balance -> mapping to user control 'savings_initial'
# Step 2: New Influx -> mapping to optimized monthly take-home 'max_safe_net_takehome'
# Step 3: Combined Total Balance
combined_total_savings = savings_initial + max_safe_net_takehome

# Step 4: Total Liabilities calculation (Current Year Slab + Past Personal Arrears)
total_gross_personal_liabilities = annual_tax_liability + personal_tax_arrears
net_withheld_credits = advance_tax_paid + assumed_ytd_rem_tds + assumed_ytd_div_tds + calculated_immediate_tds
outstanding_personal_tax_due = max(0.0, total_gross_personal_liabilities - net_withheld_credits)

# Final Deduction: Subtracting outstanding liability directly out of the combined balance pool
safely_disposable_income = combined_total_savings - outstanding_personal_tax_due

# ==========================================
# 4. SIDE-BY-SIDE LEDGER DISPLAY RENDER
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
# RIGHT VIEWPORT: PERSONAL SAVINGS ARCHITECTURE
# ------------------------------------------
with col_pers:
    st.subheader("🏦 Personal Savings & Tax Asset Ledger")
    st.write("Sequential tracking of personal net assets:")
    
    st.metric(label="💎 Safely Disposable Income", value=format_indian_currency(safely_disposable_income), delta="Protected Fluid Cash")
    st.metric(label="🏛️ Net Pending Tax Liability", value=format_indian_currency(outstanding_personal_tax_due), delta="Remaining Total Debt Balance", delta_color="inverse")
    
    # Render exactly to matching user definitions 1-4
    pers_ledger = [
        {"Sequence Steps": "1. Current Personal Savings Balance", "Value": format_indian_currency(savings_initial), "Context Description": "Core starting savings account balance baseline."},
        {"Sequence Steps": "2. New Monthly Fund Influx", "Value": format_indian_currency(max_safe_net_takehome), "Context Description": "Fresh post-TDS extraction from corporate clearing engine."},
        {"Sequence Steps": "3. Total Summation Balance", "Value": format_indian_currency(combined_total_savings), "Context Description": "Aggregated cash pool inside your account right now."},
        {"Sequence Steps": "4. Net Tax Liability Remaining", "Value": f"- {format_indian_currency(outstanding_personal_tax_due)}", "Context Description": f"Includes annual slab ({format_indian_currency(annual_tax_liability)}) + past personal arrears ({format_indian_currency(personal_tax_arrears)}) minus credits."}
    ]
    st.table(pd.DataFrame(pers_ledger))

st.write("---")
st.subheader("🛡️ Compliance & Safety Lock Audit")
st.markdown(f"Your aggregated savings account balance stands at **{format_indian_currency(combined_total_savings)}**. By factoring in your **{format_indian_currency(advance_tax_paid)}** in advance taxes along with YTD withholding credits, your pending personal tax debt is isolated at **{format_indian_currency(outstanding_personal_tax_due)}**. This leaves you with exactly **{format_indian_currency(safely_disposable_income)}** in risk-free spending power.")
