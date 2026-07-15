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

st.title("📊 Annual Strategic Scenario Simulator (With Percentage Analytics)")
st.write("Imagine full-year revenue/draw scenarios to project your integrated corporate and personal tax positions alongside explicit revenue ratio tracking.")
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
scen_annual_revenue = st.sidebar.number_input("Imagined Annual Corporate Gross Revenue (₹):", min_value=0.0, value=10000000.0, step=500000.0)
scen_annual_overhead = st.sidebar.number_input("Projected Annual Corporate Overheads (₹):", min_value=0.0, value=4800000.0, step=100000.0)
scen_corp_arrears = st.sidebar.number_input("Legacy Corporate Arrears to Clear (₹):", min_value=0.0, value=0.0, step=50000.0)

st.sidebar.write("---")
st.sidebar.subheader("👤 Imagined Annual Personal Drawings")
scen_rem_gross = st.sidebar.number_input("Projected Gross Director Remuneration (₹):", min_value=0.0, value=5200000.0, step=100000.0)
scen_bonus_gross = st.sidebar.number_input("Projected Gross Salary Bonuses (₹):", min_value=0.0, value=0.0, step=50000.0)
scen_div_gross = st.sidebar.number_input("Projected Retained Earnings / Dividends Withdrawal (Gross) (₹):", min_value=0.0, value=0.0, step=50000.0)
scen_rent_gross = st.sidebar.number_input("Projected Annual Gross House Rent Income (₹):", min_value=0.0, value=0.0, step=30000.0)
scen_other_gross = st.sidebar.number_input("Projected Income from Other Sources (₹):", min_value=0.0, value=0.0, step=10000.0)

st.sidebar.write("---")
st.sidebar.subheader("🏦 Personal Safety Controls")
scen_savings_base = st.sidebar.number_input("Baseline Personal Savings Balance (₹):", min_value=0.0, value=0.0, step=50000.0)
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
total_corporate_withheld_tds = imagined_rem_tds + imagined_bonus_tds + imagined_div_tds
total_scenario_credits = total_corporate_withheld_tds + scen_pers_advance_tax

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
# PERCENTAGE RATIO ANALYTICS MATH
# ==========================================
# Corporate percentage conversions (Base = scen_annual_revenue)
def get_corp_pct(val):
    return f"{(val / scen_annual_revenue * 100):.2f}%" if scen_annual_revenue > 0 else "0.00%"

corp_net_profit_pct   = get_corp_pct(net_company_retained_surplus)
corp_tax_pct         = get_corp_pct(modeled_corporate_tax)
corp_tds_pct         = get_corp_pct(total_corporate_withheld_tds)
corp_drawings_pct    = get_corp_pct(total_deductible_drawings)

# Personal percentage conversions (Base = net_payout_injected)
def get_pers_pct(val):
    return f"{(val / net_payout_injected * 100):.2f}%" if net_payout_injected > 0 else "0.00%"

pers_tds_subtracted_pct = get_pers_pct(total_corporate_withheld_tds)
pers_tax_liability_pct  = get_pers_pct(annual_personal_tax_liability)

# Share of actual incoming funds that are saved completely clean
pers_net_surplus_of_influx_pct = f"{(safely_disposable_annual_surplus / net_payout_injected * 100):.2f}%" if net_payout_injected > 0 else "0.00%"

# Absolute macro wealth efficiency (Safe cash out vs total corporate turnover)
overall_extraction_efficiency_pct = f"{(safely_disposable_annual_surplus / scen_annual_revenue * 100):.2f}%" if scen_annual_revenue > 0 else "0.00%"

# ==========================================
# 4. SIDE-BY-SIDE LEDGER DISPLAY RENDER
# ==========================================
col_left, col_right = st.columns(2)

# LEFT VIEWPORT: CORPORATE ANALYTICS
with col_left:
    st.subheader("🏢 Projected Corporate Scenario Breakdown")
    
    st.metric(label="📊 Estimated Corporate Tax Owed", value=format_indian_currency(modeled_corporate_tax), delta=f"{corp_tax_pct} of Revenue", delta_color="off")
    st.metric(label="🏛️ Net Company Retained Surplus (Profit)", value=format_indian_currency(net_company_retained_surplus), delta=f"{corp_net_profit_pct} of Revenue", delta_color="off")
    
    corp_matrix = [
        {"Operational Item": "Imagined Gross Revenue", "Value": format_indian_currency(scen_annual_revenue), "Ratio (%)": "100.00%"},
        {"Operational Item": "Less: Annual Overheads", "Value": f"- {format_indian_currency(scen_annual_overhead)}", "Ratio (%)": get_corp_pct(scen_annual_overhead)},
        {"Operational Item": "Less: Deductible Salaries/Bonuses", "Value": f"- {format_indian_currency(total_deductible_drawings)}", "Ratio (%)": corp_drawings_pct},
        {"Operational Item": "Mandatory Total Corporate TDS Withheld", "Value": format_indian_currency(total_corporate_withheld_tds), "Ratio (%)": corp_tds_pct},
        {"Operational Item": "Corporate Taxable Income Base", "Value": format_indian_currency(corporate_taxable_surplus), "Ratio (%)": get_corp_pct(corporate_taxable_surplus)}
    ]
    st.table(pd.DataFrame(corp_matrix))

# RIGHT VIEWPORT: PERSONAL SAVINGS ANALYTICS
with col_right:
    st.subheader("🏦 Projected Personal Wealth Matrix")
    
    st.metric(label="💎 True Safe Disposable Annual Surplus", value=format_indian_currency(safely_disposable_annual_surplus), delta=f"{pers_net_surplus_of_influx_pct} of Net Influx Saved", delta_color="normal")
    st.metric(label="🏛️ Net Remaining Personal Tax Shortfall", value=format_indian_currency(net_personal_tax_shortfall), delta_color="inverse")
    
    pers_matrix = [
        {"Wealth Item": "Starting Cash Balance Baseline", "Value": format_indian_currency(scen_savings_base), "Ratio (% of Cash Influx)": "—"},
        {"Wealth Item": "Add: Net Income Payout Influx (Post-TDS)", "Value": format_indian_currency(net_payout_injected), "Ratio (% of Cash Influx)": "100.00%"},
        {"Wealth Item": "TDS Subtracted from Company", "Value": format_indian_currency(total_corporate_withheld_tds), "Ratio (% of Cash Influx)": pers_tds_subtracted_pct},
        {"Wealth Item": "Annual Personal Progressive Tax Liability", "Value": format_indian_currency(annual_personal_tax_liability), "Ratio (% of Cash Influx)": pers_tax_liability_pct},
        {"Wealth Item": "Projected Year-End Total Savings (After ALL Taxes)", "Value": format_indian_currency(safely_disposable_annual_surplus), "Ratio (% of Cash Influx)": pers_net_surplus_of_influx_pct}
    ]
    st.table(pd.DataFrame(pers_matrix))

# ==========================================
# STRATEGIC EFFICIENCY SUMMARY PANEL
# ==========================================
st.write("---")
st.subheader("📊 Strategic Wealth Extraction Analytics")

col_eff1, col_eff2 = st.columns(2)
with col_eff1:
    st.info(
        f"💡 **Global Wealth Extraction Efficiency Ratings:**\n\n"
        f"*   **Of Corporate Gross Revenue:** **{overall_extraction_efficiency_pct}** of every rupee your firm generated successfully bypasses all tax filters to become risk-free wealth.\n"
        f"*   **Of Personal Net Influx:** **{pers_net_surplus_of_influx_pct}** of the cash that physically entered your personal accounts is completely protected and cleared for spending."
    )

with col_eff2:
    if corporate_taxable_surplus > 0:
        st.warning(f"⚡ **Tax Leakage Mitigation Warning:**\n\nYour company is leaving **{format_indian_currency(corporate_taxable_surplus)}** exposed to corporate income tax (~25.17%), costing you **{format_indian_currency(modeled_corporate_tax)}** in tax drift. Consider scaling up your deductible Director Remuneration configuration in the sidebar to suppress this corporate taxable base toward zero.")
