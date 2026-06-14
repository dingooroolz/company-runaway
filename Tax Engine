import streamlit as st

# ---------------------------------------------------------
# 1. SECURITY PASS-THROUGH GATE
# ---------------------------------------------------------
def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Private Financial Access")
    pwd = st.text_input("Enter the firm's access key:", type="password")
    
    if st.button("Unlock Dashboard"):
        if pwd == "MyFirm2026":  
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("🚫 Incorrect key.")
    return False

if not check_password():
    st.stop()

# ---------------------------------------------------------
# 2. PAGE CONFIGURATION & FORMATTING ENGINE
# ---------------------------------------------------------
st.set_page_config(page_title="Executive Tax Engine", layout="centered")

def format_indian_currency(val):
    try:
        is_negative = val < 0
        abs_val = abs(int(round(val)))
        num_str = str(abs_val)
        if len(num_str) <= 3:
            result = num_str
        else:
            last_three = num_str[-3:]
            remaining = num_str[:-3]
            out = []
            while len(remaining) > 2:
                out.append(remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                out.append(remaining)
            out.reverse()
            result = ",".join(out) + "," + last_three
        return f"-₹{result}" if is_negative else f"₹{result}"
    except Exception:
        return f"₹{val}"

# ---------------------------------------------------------
# 3. STATUTORY TDS MODELER (NEW TAX REGIME LABS)
# ---------------------------------------------------------
def calculate_personal_tax(annual_gross_salary):
    # Standard deduction automatically applied under the New Regime
    taxable_income = max(0, annual_gross_salary - 75000)
    
    tax = 0
    if taxable_income > 400000:  tax += min(400000, taxable_income - 400000) * 0.05
    if taxable_income > 800000:  tax += min(400000, taxable_income - 800000) * 0.10
    if taxable_income > 1200000: tax += min(400000, taxable_income - 1200000) * 0.15
    if taxable_income > 1600000: tax += min(400000, taxable_income - 1600000) * 0.20
    if taxable_income > 2000000: tax += min(400000, taxable_income - 2000000) * 0.25
    if taxable_income > 2400000: tax += (taxable_income - 2400000) * 0.30
    
    # Section 87A Rebate holds tax to zero for net incomes up to 12 Lakhs
    if taxable_income <= 1200000:
        return 0
        
    surcharge_rate = 0.0
    if annual_gross_salary > 5000000 and annual_gross_salary <= 10000000:
        surcharge_rate = 0.10
    elif annual_gross_salary > 10000000:
        surcharge_rate = 0.15
        
    total_tax = tax * (1 + surcharge_rate) * 1.04  # Standard 4% Education/Health Cess
    return int(total_tax)

# ---------------------------------------------------------
# 4. FLEXIBLE CONTROL INTERFACE PANEL
# ---------------------------------------------------------
st.title("🎯 Executive Profit & Tax Planning Dashboard")
st.write("Full-Year Macro View: Cross-analyze corporate targets, advance tax windows, and personal wealth extraction seamlessly.")

st.header("🔧 Macro Variables")

# Variable 1: Month-by-Month Inflow Matrix
st.subheader("💰 1. Revenue Baseline")
with st.expander("Expand to Modify Month-by-Month Inflows", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        inf_apr = st.number_input("April Revenue", value=549000, step=25000)
        inf_may = st.number_input("May Revenue", value=555000, step=25000)
        inf_jun = st.number_input("June Revenue", value=1021382, step=25000)
        inf_jul = st.number_input("July Revenue", value=1000000, step=25000)
    with col_b:
        inf_aug = st.number_input("August Revenue", value=1000000, step=25000)
        inf_sep = st.number_input("September Revenue", value=1000000, step=25000)
        inf_oct = st.number_input("October Revenue", value=1000000, step=25000)
        inf_nov = st.number_input("November Revenue", value=1000000, step=25000)
    with col_c:
        inf_dec = st.number_input("December Revenue", value=1000000, step=25000)
        inf_jan = st.number_input("January Revenue", value=1000000, step=25000)
        inf_feb = st.number_input("February Revenue", value=1000000, step=25000)
        inf_mar = st.number_input("March Revenue", value=1000000, step=25000)

total_annual_revenue = (
    inf_apr + inf_may + inf_jun + inf_jul + inf_aug + inf_sep + 
    inf_oct + inf_nov + inf_dec + inf_jan + inf_feb + inf_mar
)

# Variables 2, 3 & 4: Business Expenses, Salaries, and PAT Targets
st.subheader("⚙️ 2. Core Operational & Profit Allocations")
col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    monthly_ops = st.number_input("Monthly Business Expenses (₹)", value=264000, step=10000)
    total_annual_expenses = monthly_ops * 12
with col_v2:
    monthly_director_remun = st.number_input("Director Monthly Remuneration (₹)", value=300000, step=10000)
    total_annual_director_salary = monthly_director_remun * 12
with col_v3:
    desired_pat_val = st.number_input("Desired Corporate PAT (₹)", value=1000000, step=50000)

# ---------------------------------------------------------
# 5. TAX ALLOCATION ENGINE LOGIC
# ---------------------------------------------------------
corporate_tax_rate = 0.2517  # Section 115BAA Domestic Rate

# Calculate the precise Profit Before Tax (PBT) needed to hit the desired Net Corporate Profit (PAT)
required_pbt = desired_pat_val / (1 - corporate_tax_rate)
calculated_corporate_tax = required_pbt * corporate_tax_rate

# Total outlays required to meet your chosen variables
total_modeled_outlays = total_annual_expenses + total_annual_director_salary + required_pbt
unallocated_reserve_balance = total_annual_revenue - total_modeled_outlays

# Personal Tax Deductions Engine Call
total_annual_personal_tax = calculate_personal_tax(total_annual_director_salary)
monthly_tds_deduction = total_annual_personal_tax / 12
net_annual_personal_savings = total_annual_director_salary - total_annual_personal_tax

# ---------------------------------------------------------
# 6. EXECUTIVE MATRICES VISUALIZATION
# ---------------------------------------------------------
st.markdown("---")
st.header("📊 Full-Year Macro Summary")

if unallocated_reserve_balance < 0:
    st.error(f"⚠️ **Revenue Deficit Warning:** Your current parameters demand an annual total of {format_indian_currency(total_modeled_outlays)}, which exceeds your total annual revenue by **{format_indian_currency(abs(unallocated_reserve_balance))}**. Lower your variables or increase revenue projections to balance the engine safely.")
else:
    st.success(f"✅ **Financial System Balanced:** Safe operations confirmed. After factoring in expenses, salaries, and corporate PAT goals, you have an unallocated year-end liquid buffer of **{format_indian_currency(unallocated_reserve_balance)}** remaining on your books.")

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Total Annual Revenue", format_indian_currency(total_annual_revenue))
with col_m2:
    st.metric("Target Corporate PAT", format_indian_currency(desired_pat_val))
with col_m3:
    pat_margin_pct = (desired_pat_val / total_annual_revenue * 100) if total_annual_revenue > 0 else 0
    st.metric("Modeled PAT Margin", f"{pat_margin_pct:.1f}%")

st.markdown("---")

# Distinct Operational Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🏢 Corporate Advance Tax Reserves", 
    "👨‍💼 Director TDS Reserve (Co. Account)", 
    "🏦 Personal Savings Account Reserve"
])

with tab1:
    st.subheader("📅 Statutory Corporate Advance Tax Timeline")
    st.write("To completely insulate your firm from Section 234C late interest penalties, make sure your corporate account has successfully reserved and transferred these precise cumulative installment figures:")
    
    q1_tax = calculated_corporate_tax * 0.15
    q2_tax = calculated_corporate_tax * 0.45
    q3_tax = calculated_corporate_tax * 0.75
    q4_tax = calculated_corporate_tax * 1.00

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.info(f"**Q1 (By June 15):**\n\n**{format_indian_currency(q1_tax)}** *(15% Cumulative)*")
        st.info(f"**Q3 (By Dec 15):**\n\n**{format_indian_currency(q3_tax)}** *(75% Cumulative)*")
    with col_q2:
        st.info(f"**Q2 (By Sept 15):**\n\n**{format_indian_currency(q2_tax)}** *(45% Cumulative)*")
        st.info(f"**Q4 (By March 15):**\n\n**{format_indian_currency(q4_tax)}** *(100% Cumulative)*")
        
    st.success(f"**Total Annual Corporate Advance Tax Obligation:** {format_indian_currency(calculated_corporate_tax)}")

with tab2:
    st.subheader("🛡️ Monthly Director TDS Allocation")
    st.write("Based on your customized monthly salary input, keep this exact amount locked inside your company account every single month to clear individual slab liabilities systematically:")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.metric("Monthly TDS to Withhold", format_indian_currency(monthly_tds_deduction))
    with col_t2:
        st.metric("Gross Monthly Salary Payout", format_indian_currency(monthly_director_remun))
        
    st.caption(f"Total projected personal income tax to clear via corporate payroll filings over the entire year: {format_indian_currency(total_annual_personal_tax)}")

with tab3:
    st.subheader("💵 Personal Savings Account Liquidity")
    st.write("This is the exact net amount that safely transfers from corporate payroll straight to your personal savings account every single month. This cash is fully post-tax and free for personal deployment:")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Net Monthly Savings Transfer", format_indian_currency(net_annual_personal_savings / 12))
    with col_s2:
        st.metric("Total Annual Net Wealth Extracted", format_indian_currency(net_annual_personal_savings))
