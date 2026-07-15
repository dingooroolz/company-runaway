import streamlit as st
import pandas as pd
import re

# ---------------------------------------------------------
# 1. SECURITY GATE: Private Dashboard Lock
# ---------------------------------------------------------
def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Private Financial Access")
    pwd = st.text_input("Enter the firm's scenario engine access key:", type="password")
    
    if st.button("Unlock Sandbox Dashboard"):
        if pwd == "MyFirm2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("🚫 Incorrect key.")
    return False

if not check_password():
    st.stop()

# ==========================================
# PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Annual Scenario Simulator", page_icon="📊", layout="wide")

st.title("📊 Annual Strategic Scenario Simulator")
st.write("Imagine full-year revenue/draw scenarios to project your integrated corporate and personal tax positions.")
st.write("---")

# ==========================================
# INDIAN NUMBER FORMATTING ENGINE
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
# 2026 PROGRESSIVE PERSONAL TAX SLAB CALCULATOR
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
# INTERACTIVE SCENARIO SIDEBAR PANEL
# ==========================================
st.sidebar.header("⚙️ Scenario Parameters")

st.sidebar.subheader("🏢 Projected Annual Corporate Matrix")
scen_annual_revenue = st.sidebar.number_input("Imagined Annual Corporate Gross Revenue (₹):", min_value=0.0, value=8500000.0, step=500000.0)
scen_annual_overhead = st.sidebar.number_input("Projected Annual Corporate Overheads (₹):", min_value=0.0, value=3000000.0, step=100000.0)
scen_corp_arrears = st.sidebar.number_input("Legacy Corporate Arrears to Clear (₹):", min_value=0.0, value=0.0, step=50000.0)

st.sidebar.write("---")
st.sidebar.subheader("👤 Imagined Annual Personal Drawings")
scen_rem_gross = st.sidebar.number_input("Projected Gross Director Remuneration (₹):", min_value=0.0, value=360000.0, step=10000.0)
scen_bonus_gross = st.sidebar.number_input("Projected Gross Salary Bonuses (₹):", min_value=0.0, value=0.0, step=10000.0)
scen_div_gross = st.sidebar.number_input("Projected Retained Earnings / Dividends Withdrawal (Gross) (₹):", min_value=0.0, value=0.0, step=10000.0)
scen_rent_gross = st.sidebar.number_input("Projected Annual Gross House Rent Income (₹):", min_value=0.0, value=0.0, step=10000.0)
scen_other_gross = st.sidebar.number_input("Projected Income from Other Sources (₹):", min_value=0.0, value=0.0, step=5000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏦 Personal Safety Controls")
scen_savings_base = st.sidebar.number_input("Baseline Personal Savings Balance (₹):", min_value=0.0, value=500000.0, step=50000.0)
scen_pers_advance_tax = st.sidebar.number_input("Planned Personal Advance Tax to Pay (₹):", min_value=0.0, value=0.0, step=10000.0)
scen_pers_arrears = st.sidebar.number_input("Personal Tax Arrears from Prior Years (₹):", min_value=0.0, value=0.0, step=5000.0)

# ==========================================
# MATHEMATICAL FORECASTING LOGIC ENGINE
# ==========================================
# 1. Corporate Scenario Computation
total_deductible_drawings = scen_rem_gross + scen_bonus_gross
corporate_taxable_surplus = max(0.0, scen_annual_revenue - scen_annual_overhead - total_deductible_drawings)

modeled_corporate_tax = corporate_taxable_surplus * 0.2517
net_company_retained_surplus = corporate_taxable_surplus - modeled_corporate_tax - scen_corp_arrears

# 2. Personal Scenario Computation
taxable_rental_income = scen_rent_gross * 0.70

total_imagined_personal_gross = (
    scen_rem_gross + 
    scen_bonus_gross + 
    scen_div_gross + 
    taxable_rental_income + 
    scen_other_gross
)
annual_personal_tax_liability = calculate_personal_tax(total_imagined_personal_gross)

imagined_rem_tds = scen_rem_gross * 0.10
imagined_bonus_tds = scen_bonus_gross * 0.10
imagined_div_tds = scen_div_gross * 0.10
total_scenario_credits = imagined_rem_tds + imagined_bonus_tds + imagined_div_tds + scen_pers_advance_tax

net_personal_tax_shortfall = max(0.0, (annual_personal_tax_liability + scen_pers_arrears) - total_scenario_credits)

net_payout_injected = (
    (scen_rem_gross - imagined_rem_tds) + 
    (scen_bonus_gross - imagined_bonus_tds) + 
    (scen_div_gross - imagined_div_tds) + 
    scen_rent_gross + 
    scen_other_gross
)
final_projected_savings_pool = scen_savings_base + net_payout_injected
safely_disposable_annual_surplus = final_projected_savings_pool - net_personal_tax_shortfall

# ==========================================
# 4. SIDE-BY-SIDE LEDGER DISPLAY RENDER
# ==========================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏢 Projected Corporate Scenario Breakdown")
    
    st.metric(label="📊 Estimated Corporate Tax Owed", value=format_indian_currency(modeled_corporate_tax))
    st.metric(label="🏛️ Net Company Retained Earnings Surplus", value=format_indian_currency(net_company_retained_surplus))
    
    corp_matrix = [
        {"Operational Item": "Imagined Gross Revenue", "Value": format_indian_currency(scen_annual_revenue)},
        {"Operational Item": "Less: Annual Overheads", "Value": f"- {format_indian_currency(scen_annual_overhead)}"},
        {"Operational Item": "Less: Deductible Compensation (Remuneration + Bonus)", "Value": f"- {format_indian_currency(total_deductible_drawings)}"},
        {"Operational Item": "Corporate Taxable Income Base", "Value": format_indian_currency(corporate_taxable_surplus)}
    ]
    st.table(pd.DataFrame(corp_matrix))

with col_right:
    st.subheader("🏦 Projected Personal Wealth Matrix")
    
    st.metric(label="💎 Safe Disposable Income Buffer", value=format_indian_currency(safely_disposable_annual_surplus))
    st.metric(label="🏛️ Net Remaining Personal Tax Shortfall", value=format_indian_currency(net_personal_tax_shortfall), delta_color="inverse")
    
    pers_matrix = [
        {"Wealth Item": "Starting Cash Balance Baseline", "Value": format_indian_currency(scen_savings_base)},
        {"Wealth Item": "Add: Net Income Payout Influx", "Value": format_indian_currency(net_payout_injected)},
        {"Wealth Item": "Projected Year-End Total Savings Balance", "Value": format_indian_currency(final_projected_savings_pool)},
        {"Wealth Item": "Less: Outstanding Personal Year-End Tax Shortfall", "Value": f"- {format_indian_currency(net_personal_tax_shortfall)}"}
    ]
    st.table(pd.DataFrame(pers_matrix))

st.write("---")
st.subheader("🛡️ Integrated Scenario Audit Summary")
st.markdown(f"Under this imagined scenario, your total pooled annual personal gross income hits **{format_indian_currency(total_imagined_personal_gross)}** (factoring in the **{format_indian_currency(taxable_rental_income)}** taxable portion of your house rent). Your baseline annual progressive tax liability is modeled at **{format_indian_currency(annual_personal_tax_liability)}**. After tracking all locked transaction TDS and planned advance taxes, your total personal savings account reaches **{format_indian_currency(final_projected_savings_pool)}**, leaving you with a completely clear, protected wealth threshold of **{format_indian_currency(safely_disposable_annual_surplus)}**.")
