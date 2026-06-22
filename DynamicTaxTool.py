import streamlit as st
import pandas as pd

# Set page config for a clean dashboard look
st.set_page_config(page_title="Ecosystem Forecasting Engine", layout="wide")

st.title("🛡️ Corporate Runway & Tax Optimization Dashboard")
st.markdown("---")

# ==========================================
# SIDEBAR - GLOBAL LIVE CONSTANTS
# ==========================================
st.sidebar.header("⚙️ Global Ecosystem Inputs")
current_cash_pool = st.sidebar.number_input("Current Bank Active Pool (₹)", value=629000, step=1000)
fixed_overhead = st.sidebar.number_input("Monthly Operating Overhead (₹)", value=236826, step=500)
target_net_salary = st.sidebar.number_input("Target Monthly Net Take-Home (₹)", value=300000, step=10000)

# ==========================================
# MODULE 1: STATIC Q1 CLEANUP MATRIX
# ==========================================
st.header("1. Static Q1 Cleanup Matrix & June Clearance")

# Hardcoded true calculated liabilities for the closed Q1 ledger
q1_corporate_tax = 117066
historical_pat_tds = 165000
standard_payroll_tds = 68965
june_bonus_tds = 86726

total_q1_liability = q1_corporate_tax + historical_pat_tds + standard_payroll_tds + june_bonus_tds
ca_portal_payment = 150000
required_corporate_reserve = total_q1_liability - ca_portal_payment
safe_immediate_withdrawal = current_cash_pool - required_corporate_reserve

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Generated Q1 Tax Debt", f"₹{total_q1_liability:,}")
with col2:
    st.metric("Required Corporate Reserve (Frozen)", f"₹{required_corporate_reserve:,}")
with col3:
    st.metric("Safe Personal Extraction (Today)", f"₹{safe_immediate_withdrawal:,}", delta_color="inverse")

# Compliance Warning Box
if current_cash_pool < required_corporate_reserve:
    st.error(f"🚨 ALERT: Bank balance is below the compliance guardrail! Shortfall: ₹{required_corporate_reserve - current_cash_pool:,}")
else:
    st.success("✅ Compliance Shield Active: Corporate reserve is fully funded for Q1 payouts.")

# ==========================================
# MODULE 2: ROLLING JULY - MARCH ZERO-PROFIT PIPELINE
# ==========================================
st.markdown("---")
st.header("2. Rolling July - March Forecasting (9 Months)")

# The Dynamic Gross-Up Math (31.2% Top Marginal Bracket Filter)
marginal_tax_rate = 0.312
required_monthly_gross_salary = int(target_net_salary / (1 - marginal_tax_rate))
monthly_payroll_tds = required_monthly_gross_salary - target_net_salary
required_monthly_invoice_target = fixed_overhead + required_monthly_gross_salary

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Monthly Grossed-Up Payroll")
    st.write(f"**Required Gross Salary:** ₹{required_monthly_gross_salary:,}")
    st.write(f"**Payroll TDS Intercepted (31.2%):** ₹{monthly_payroll_tds:,}")
    st.write(f"**Clean Net to Pocket:** ₹{target_net_salary:,}")

with col2:
    st.subheader("Zero-Profit Target")
    st.write(f"**Fixed Business Expenses:** ₹{fixed_overhead:,}")
    st.write(f"**Gross Salary Drag:** ₹{required_monthly_gross_salary:,}")
    st.info(f"**Minimum Monthly Invoice Target:** ₹{required_monthly_invoice_target:,}")

with col3:
    st.subheader("Ecosystem Balance Check")
    accounting_net_profit = required_monthly_invoice_target - fixed_overhead - required_monthly_gross_salary
    st.metric("Projected Corporate Net Profit", f"₹{accounting_net_profit}")
    st.caption("Keeping this at exactly 0 avoids all future corporate tax double-dipping.")

# ==========================================
# MODULE 3: MACRO YEAR-END WEALTH FORECAST
# ==========================================
st.markdown("---")
st.header("3. Macro Year-End Wealth Forecast (Personal Savings Pool)")

# Accumulation math
q1_historical_cash = 2484000
june_extraction_bonus = safe_immediate_withdrawal
future_salary_stream = target_net_salary * 9
total_projected_personal_wealth = q1_historical_cash + june_extraction_bonus + future_salary_stream

# Hidden personal PAT tax trap handler
remaining_personal_pat_tax_gap = 349800
unencumbered_net_surplus_wealth = total_projected_personal_wealth - remaining_personal_pat_tax_gap

col1, col2 = st.columns(2)
with col1:
    st.subheader("Cumulative Personal Account Inflows")
    forecast_data = {
        "Financial Component": ["Q1 Cash Already Received", "June Safe Extraction Bonus", "July-March Salary Stream (9 months)", "Total Projected Cash Pool"],
        "Amount (₹)": [f"₹{q1_historical_cash:,}", f"₹{june_extraction_bonus:,}", f"₹{future_salary_stream:,}", f"₹{total_projected_personal_wealth:,}"]
    }
    st.table(pd.DataFrame(forecast_data))

with col2:
    st.subheader("🛡️ Net Wealth Protection Shield")
    st.metric("Total Pooled Bank Balance", f"₹{total_projected_personal_wealth:,}")
    st.metric("Isolated Individual PAT Tax Reserve", f"₹{remaining_personal_pat_tax_gap:,}", delta="-31.2% Trap", delta_color="inverse")
    st.highlight(f"**True Tax-Clear Personal Surplus by March 31:** ₹{unencumbered_net_surplus_wealth:,}")