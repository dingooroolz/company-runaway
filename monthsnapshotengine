import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Corporate Drain Optimizer", page_icon="💰", layout="wide")

st.title("💰 Script 5: Corporate Account Drain & Maximum Payout Optimizer")
st.write("Input your incoming revenue, current overhead, and YTD historic drawings to find the absolute maximum safe personal drawdown.")
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
st.sidebar.header("📥 Inflow & Outflow Tracker")

st.sidebar.subheader("💵 Monthly Revenue Capture")
rev_received = st.sidebar.number_input("1. Revenue Already Received (This Month):", min_value=0.0, value=500000.0, step=50000.0)
rev_expected = st.sidebar.number_input("2. Additional Expected Revenue (By End of Month):", min_value=0.0, value=250000.0, step=50000.0)
total_monthly_revenue = rev_received + rev_expected

st.sidebar.write("---")
st.sidebar.subheader("🛠️ Monthly Corporate Overhead")
overhead_incurred = st.sidebar.number_input("1. Expenses Already Billed / Paid:", min_value=0.0, value=250000.0, step=10000.0)
overhead_projected = st.sidebar.number_input("2. Expected Remaining Overhead Tasks:", min_value=0.0, value=124000.0, step=10000.0)
total_month_overhead = overhead_incurred + overhead_projected

st.sidebar.write("---")
st.sidebar.subheader("👤 Historical YTD & Future Run Rates")
# --- NEW CUMULATIVE INPUT FIELD ---
rem_ytd = st.sidebar.number_input("Remuneration Withdrawn So Far (YTD Actual Net):", min_value=0.0, value=700000.0, step=50000.0,
                                 help="The total net amount you have already withdrawn into your personal account from April 1st to date.")
rem_future = st.sidebar.number_input("Projected Total Payouts (Future Months Only):", min_value=0.0, value=0.0, step=50000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏛️ Statutory Tax Settlement Checks")
advance_tax_paid = st.sidebar.number_input("Advance Taxes Paid So Far (YTD):", min_value=0.0, value=0.0, step=10000.0)
past_tax_arrears = st.sidebar.number_input("Pending Tax Arrears from Previous Years:", min_value=0.0, value=0.0, step=5000.0)
base_tds_rate = st.sidebar.slider("Standard Transactional TDS Rate (%)", min_value=0.0, max_value=30.0, value=10.0, step=1.0) / 100.0

# ==========================================
# 3. THE ADVANCED ACCOUNT DRAIN ENGINE LOGIC
# ==========================================
# Step 1: Liquid operational cash left over this month before director distribution
free_floating_operating_cash = total_monthly_revenue - total_month_overhead

# Step 2: Clear historical tax debt first out of the available corporate pool
cash_available_for_remuneration_pool = free_floating_operating_cash - past_tax_arrears

if cash_available_for_remuneration_pool <= 0:
    max_safe_gross_remuneration = 0.0
    max_safe_net_takehome = 0.0
    calculated_immediate_tds = 0.0
    uncovered_tax_shortfall = 0.0
    annual_tax_liability = 0.0
    total_projected_annual_gross = 0.0
else:
    # Algebraic split: Maximum gross distribution matching remaining liquid cash exactly
    max_safe_gross_remuneration = cash_available_for_remuneration_pool
    base_net_takehome = max_safe_gross_remuneration * (1.0 - base_tds_rate)
    calculated_immediate_tds = max_safe_gross_remuneration - base_net_takehome

    # Step 3: Factor in YTD cumulative history to determine true progressive tax slabs
    assumed_ytd_tds_withheld = rem_ytd * (base_tds_rate / (1.0 - base_tds_rate))
    total_ytd_gross_remuneration = rem_ytd + assumed_ytd_tds_withheld
    
    # Combined annual projection formula
    total_projected_annual_gross = total_ytd_gross_remuneration + max_safe_gross_remuneration + rem_future
    annual_tax_liability = calculate_personal_tax(total_projected_annual_gross)
    
    # Check what credits are already submitted to government vs actual progressive liability
    total_tax_credits_cleared = advance_tax_paid + assumed_ytd_tds_withheld + calculated_immediate_tds
    uncovered_tax_shortfall = (annual_tax_liability + past_tax_arrears) - total_tax_credits_cleared
    
    # If high-tier annual brackets create a deficit, protect the account by reducing current cash-out bounds
    if uncovered_tax_shortfall > 0:
        max_safe_net_takehome = base_net_takehome - uncovered_tax_shortfall
        max_safe_net_takehome = max(0.0, max_safe_net_takehome)
    else:
        max_safe_net_takehome = base_net_takehome

# Final accounting checks
leftover_corporate_cash_buffer = free_floating_operating_cash - (max_safe_net_takehome if cash_available_for_remuneration_pool > 0 else 0.0) - calculated_immediate_tds

# ==========================================
# 4. EXECUTIVE METRIC DISPLAY RENDER
# ==========================================
st.subheader("📊 Maximum Allowable Drawdown Strategy Blueprint")
st.write("Calculated thresholds to safely maximize extraction while keeping your tax accounts perfectly funded:")

col_k1, col_k2, col_k3 = st.columns(3)
col_k1.metric(
    label="🚀 Max Net Take-Home (Your Pocket)",
    value=format_indian_currency(max_safe_net_takehome),
    delta="Safe to Liquidate Immediately"
)
col_k2.metric(
    label="🔒 Required TDS Reserve (Leave in Bank)",
    value=format_indian_currency(calculated_immediate_tds),
    delta="Static Tax Remittance",
    delta_color="inverse"
)
col_k3.metric(
    label="🌊 Free-Floating Cash (Before Salary)",
    value=format_indian_currency(free_floating_operating_cash),
    delta=f"Total Month Revenue: {format_indian_currency(total_monthly_revenue)}"
)

st.write("---")

# ==========================================
# 5. GRANULAR FUND ROUTING LEDGER
# ==========================================
st.subheader("📜 Step-by-Step Corporate Clearing Sequence")

ledger_data = [
    {"Financial Matrix Layer": "1. Gross Monthly Inflow Volume", "Allocation Value": format_indian_currency(total_monthly_revenue), "Strategic Breakdown Description": f"Combines ₹{rev_received:,} received + ₹{rev_expected:,} expected billing lines."},
    {"Financial Matrix Layer": "2. Deduct: Total Monthly Overhead Costs", "Allocation Value": f"- {format_indian_currency(total_month_overhead)}", "Dynamic Context": f"Absorbed entirely by ₹{overhead_incurred:,} actuals + ₹{overhead_projected:,} projections."},
    {"Financial Matrix Layer": "3. Available Operating Fund Ceiling", "Allocation Value": format_indian_currency(free_floating_operating_cash), "Dynamic Context": "Liquid cash available for tax clearance and director allocations."},
    {"Financial Matrix Layer": "4. Deduct: Past Years Tax Arrears Cleared", "Allocation Value": f"- {format_indian_currency(past_tax_arrears)}", "Dynamic Context": "Cleared immediately out of the available corporate pool."},
    {"Financial Matrix Layer": "5. Allocated Gross Director Remuneration", "Allocation Value": format_indian_currency(max_safe_gross_remuneration), "Dynamic Context": "Total expense chunk assigned to your payroll name before deductions."},
    {"Financial Matrix Layer": f"6. Deduct: Immediate TDS Withholding ({base_tds_rate*100:.1f}%)", "Allocation Value": f"- {format_indian_currency(calculated_immediate_tds)}", "Dynamic Context": "Pre-withheld by the company and locked for PAN credit deposit."},
    {"Financial Matrix Layer": "🎯 7. MAX ALLOWABLE PERSONAL DRAWDOWN", "Allocation Value": format_indian_currency(max_safe_net_takehome), "Dynamic Context": "The final amount you can transfer to your personal bank account to empty the firm safely."}
]

df_ledger = pd.DataFrame(ledger_data)
st.dataframe(df_ledger, use_container_width=True)

# ==========================================
# 6. RETENTION ACCURACY VERIFICATION FOOTER
# ==========================================
st.write("---")
st.subheader("🛡️ Account Balances Post-Optimization Verification")
col_v1, col_v2 = st.columns(2)
col_v1.info(f"🏦 **Leftover Corporate Bank Balance:** {format_indian_currency(leftover_corporate_cash_buffer)} (Holds any extra safety reserves matching progressive slab differentials).")
col_v2.warning(f"🏛️ **Projected Total Personal Annual Income:** {format_indian_currency(total_projected_annual_gross)} (Driving an estimated year-end tax liability of {format_indian_currency(annual_tax_liability)} based on YTD + Current projections).")
