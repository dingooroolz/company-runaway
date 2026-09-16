import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & SECURITY
# ==========================================
st.set_page_config(page_title="Dynamic Target Revenue & Tax Runway Simulator", page_icon="🎯", layout="wide")

def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Private Financial Access")
    pwd = st.text_input("Enter access key:", type="password")
    if st.button("Unlock Simulator"):
        if pwd == "MyFirm2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("🚫 Incorrect key.")
    return False

if not check_password():
    st.stop()

# ==========================================
# FORMATTING & TAX CALCULATION ENGINES
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
# 2. CURRENT FINANCIAL POSITION (SIDEBAR)
# ==========================================
st.sidebar.header("📥 Current Financial Position")

ytd_revenue_deposited = st.sidebar.number_input(
    "Total Gross Revenue Received / Deposited YTD (₹):",
    min_value=0.0,
    value=2500000.0,
    step=100000.0,
    help="Gross income earned and deposited so far since April 1st."
)

current_savings_balance = st.sidebar.number_input(
    "Current Cash / Savings Balance Remaining (₹):",
    min_value=0.0,
    value=1200000.0,
    step=50000.0,
    help="Liquid cash physically available in your bank account today."
)

advance_tax_paid = st.sidebar.number_input(
    "Total Advance Tax Paid So Far (₹):",
    min_value=0.0,
    value=150000.0,
    step=25000.0,
    help="Direct advance tax instalments paid through challans."
)

tds_deducted_so_far = st.sidebar.number_input(
    "TDS Already Deducted / Withheld at Source (₹):",
    min_value=0.0,
    value=250000.0,
    step=25000.0,
    help="Tax withheld by clients or corporate accounts (reflecting in Form 26AS/AIS)."
)

months_remaining = st.sidebar.slider(
    "Months Remaining Until Financial Year-End:",
    min_value=1,
    max_value=12,
    value=7,
    help="Number of months over which to spread the remaining tax liability reserve."
)

# ==========================================
# 3. INTERACTIVE SLIDER CONTROL
# ==========================================
st.title("🎯 Year-End Target Revenue & Tax Runway Simulator")
st.write("Slide to adjust your desired full-year gross revenue target. All projections, liabilities, and monthly reserve targets update instantly.")

slider_min = max(1000000.0, float(ytd_revenue_deposited))
slider_max = max(slider_min * 2.5, 15000000.0)

target_total_revenue = st.slider(
    "🎯 Select Target Full-Year Gross Revenue / Cash Flow (₹):",
    min_value=float(slider_min),
    max_value=float(slider_max),
    value=max(float(slider_min), 6000000.0),
    step=100000.0,
    format="%f"
)

# ==========================================
# 4. MATHEMATICAL ENGINE
# ==========================================
# Additional revenue required to hit target
additional_revenue_required = max(0.0, target_total_revenue - ytd_revenue_deposited)

# Projected total tax liability on the target total revenue
total_projected_tax = calculate_personal_tax(target_total_revenue)

# Total pre-paid tax credits
total_tax_credits_accumulated = advance_tax_paid + tds_deducted_so_far

# Remaining tax payable
remaining_tax_payable = max(0.0, total_projected_tax - total_tax_credits_accumulated)

# Average monthly tax reserve required
monthly_tax_reserve_required = (
    remaining_tax_payable / months_remaining if months_remaining > 0 else remaining_tax_payable
)

# Projected year-end post-tax retention
projected_year_end_post_tax = target_total_revenue - total_projected_tax

# Projected safe final cash position (starting cash + new inflow after tax)
projected_safe_bank_balance = current_savings_balance + additional_revenue_required - remaining_tax_payable

# Ratios
effective_tax_rate_pct = f"{(total_projected_tax / target_total_revenue * 100):.2f}%" if target_total_revenue > 0 else "0.00%"
retention_rate_pct = f"{(projected_year_end_post_tax / target_total_revenue * 100):.2f}%" if target_total_revenue > 0 else "0.00%"

# ==========================================
# 5. CORE KPIS DISPLAY
# ==========================================
st.write("---")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="🚀 Additional Revenue Needed",
        value=format_indian_currency(additional_revenue_required),
        delta=f"Target: {format_indian_currency(target_total_revenue)}"
    )

with kpi2:
    st.metric(
        label="🏛️ Total Projected Tax Liability",
        value=format_indian_currency(total_projected_tax),
        delta=f"Effective Rate: {effective_tax_rate_pct}",
        delta_color="off"
    )

with kpi3:
    st.metric(
        label="📉 Remaining Tax Payable",
        value=format_indian_currency(remaining_tax_payable),
        delta=f"Credits: {format_indian_currency(total_tax_credits_accumulated)}",
        delta_color="off"
    )

with kpi4:
    st.metric(
        label="💎 Year-End Post-Tax Retention",
        value=format_indian_currency(projected_year_end_post_tax),
        delta=f"{retention_rate_pct} of Target Retained",
        delta_color="normal"
    )

# ==========================================
# 6. ACTION RUNWAY & BREAKDOWN LEDGERS
# ==========================================
st.write("---")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📅 Monthly Tax Reserve Runway")
    st.info(
        f"To arrive at March 31st with zero tax debt, allocate **{format_indian_currency(monthly_tax_reserve_required)}** "
        f"into a protected reserve account each month across the remaining **{months_remaining} months**."
    )
    
    runway_table = [
        {"Action / Milestone": "Total Remaining Tax Shortfall", "Amount": format_indian_currency(remaining_tax_payable)},
        {"Action / Milestone": "Months Left to Spread Liability", "Amount": f"{months_remaining} Months"},
        {"Action / Milestone": "Mandatory Monthly Reserve Target", "Amount": format_indian_currency(monthly_tax_reserve_required)},
        {"Action / Milestone": "Current Safe Cash Buffer Today", "Amount": format_indian_currency(current_savings_balance - monthly_tax_reserve_required)}
    ]
    st.table(pd.DataFrame(runway_table))

with col_right:
    st.subheader("📊 Full-Year Target Reconciliation")
    
    reconciliation_table = [
        {"Ledger Item": "Selected Target Revenue (100%)", "Amount": format_indian_currency(target_total_revenue), "Ratio (%)": "100.00%"},
        {"Ledger Item": "Less: Total Estimated Tax Liability", "Amount": format_indian_currency(-total_projected_tax), "Ratio (%)": effective_tax_rate_pct},
        {"Ledger Item": "Net Post-Tax Income Retained", "Amount": format_indian_currency(projected_year_end_post_tax), "Ratio (%)": retention_rate_pct},
        {"Ledger Item": "Advance Tax Paid YTD", "Amount": format_indian_currency(advance_tax_paid), "Ratio (%)": "—"},
        {"Ledger Item": "TDS Credits Accumulated YTD", "Amount": format_indian_currency(tds_deducted_so_far), "Ratio (%)": "—"},
        {"Ledger Item": "Final Out-of-Pocket Tax Balance", "Amount": format_indian_currency(remaining_tax_payable), "Ratio (%)": f"{(remaining_tax_payable / target_total_revenue * 100):.2f}%"}
    ]
    st.table(pd.DataFrame(reconciliation_table))import streamlit as st
import pandas as pd
import re

# ==========================================
# 1. PAGE SETUP & SECURITY
# ==========================================
st.set_page_config(page_title="Dynamic Target Revenue & Tax Runway Simulator", page_icon="🎯", layout="wide")

def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Private Financial Access")
    pwd = st.text_input("Enter access key:", type="password")
    if st.button("Unlock Simulator"):
        if pwd == "MyFirm2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("🚫 Incorrect key.")
    return False

if not check_password():
    st.stop()

# ==========================================
# FORMATTING & TAX CALCULATION ENGINES
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
# 2. CURRENT FINANCIAL POSITION (SIDEBAR)
# ==========================================
st.sidebar.header("📥 Current Financial Position")

ytd_revenue_deposited = st.sidebar.number_input(
    "Total Gross Revenue Received / Deposited YTD (₹):",
    min_value=0.0,
    value=2500000.0,
    step=100000.0,
    help="Gross income earned and deposited so far since April 1st."
)

current_savings_balance = st.sidebar.number_input(
    "Current Cash / Savings Balance Remaining (₹):",
    min_value=0.0,
    value=1200000.0,
    step=50000.0,
    help="Liquid cash physically available in your bank account today."
)

advance_tax_paid = st.sidebar.number_input(
    "Total Advance Tax Paid So Far (₹):",
    min_value=0.0,
    value=150000.0,
    step=25000.0,
    help="Direct advance tax instalments paid through challans."
)

tds_deducted_so_far = st.sidebar.number_input(
    "TDS Already Deducted / Withheld at Source (₹):",
    min_value=0.0,
    value=250000.0,
    step=25000.0,
    help="Tax withheld by clients or corporate accounts (reflecting in Form 26AS/AIS)."
)

months_remaining = st.sidebar.slider(
    "Months Remaining Until Financial Year-End:",
    min_value=1,
    max_value=12,
    value=7,
    help="Number of months over which to spread the remaining tax liability reserve."
)

# ==========================================
# 3. INTERACTIVE SLIDER CONTROL
# ==========================================
st.title("🎯 Year-End Target Revenue & Tax Runway Simulator")
st.write("Slide to adjust your desired full-year gross revenue target. All projections, liabilities, and monthly reserve targets update instantly.")

slider_min = max(1000000.0, float(ytd_revenue_deposited))
slider_max = max(slider_min * 2.5, 15000000.0)

target_total_revenue = st.slider(
    "🎯 Select Target Full-Year Gross Revenue / Cash Flow (₹):",
    min_value=float(slider_min),
    max_value=float(slider_max),
    value=max(float(slider_min), 6000000.0),
    step=100000.0,
    format="%f"
)

# ==========================================
# 4. MATHEMATICAL ENGINE
# ==========================================
# Additional revenue required to hit target
additional_revenue_required = max(0.0, target_total_revenue - ytd_revenue_deposited)

# Projected total tax liability on the target total revenue
total_projected_tax = calculate_personal_tax(target_total_revenue)

# Total pre-paid tax credits
total_tax_credits_accumulated = advance_tax_paid + tds_deducted_so_far

# Remaining tax payable
remaining_tax_payable = max(0.0, total_projected_tax - total_tax_credits_accumulated)

# Average monthly tax reserve required
monthly_tax_reserve_required = (
    remaining_tax_payable / months_remaining if months_remaining > 0 else remaining_tax_payable
)

# Projected year-end post-tax retention
projected_year_end_post_tax = target_total_revenue - total_projected_tax

# Projected safe final cash position (starting cash + new inflow after tax)
projected_safe_bank_balance = current_savings_balance + additional_revenue_required - remaining_tax_payable

# Ratios
effective_tax_rate_pct = f"{(total_projected_tax / target_total_revenue * 100):.2f}%" if target_total_revenue > 0 else "0.00%"
retention_rate_pct = f"{(projected_year_end_post_tax / target_total_revenue * 100):.2f}%" if target_total_revenue > 0 else "0.00%"

# ==========================================
# 5. CORE KPIS DISPLAY
# ==========================================
st.write("---")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="🚀 Additional Revenue Needed",
        value=format_indian_currency(additional_revenue_required),
        delta=f"Target: {format_indian_currency(target_total_revenue)}"
    )

with kpi2:
    st.metric(
        label="🏛️ Total Projected Tax Liability",
        value=format_indian_currency(total_projected_tax),
        delta=f"Effective Rate: {effective_tax_rate_pct}",
        delta_color="off"
    )

with kpi3:
    st.metric(
        label="📉 Remaining Tax Payable",
        value=format_indian_currency(remaining_tax_payable),
        delta=f"Credits: {format_indian_currency(total_tax_credits_accumulated)}",
        delta_color="off"
    )

with kpi4:
    st.metric(
        label="💎 Year-End Post-Tax Retention",
        value=format_indian_currency(projected_year_end_post_tax),
        delta=f"{retention_rate_pct} of Target Retained",
        delta_color="normal"
    )

# ==========================================
# 6. ACTION RUNWAY & BREAKDOWN LEDGERS
# ==========================================
st.write("---")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📅 Monthly Tax Reserve Runway")
    st.info(
        f"To arrive at March 31st with zero tax debt, allocate **{format_indian_currency(monthly_tax_reserve_required)}** "
        f"into a protected reserve account each month across the remaining **{months_remaining} months**."
    )
    
    runway_table = [
        {"Action / Milestone": "Total Remaining Tax Shortfall", "Amount": format_indian_currency(remaining_tax_payable)},
        {"Action / Milestone": "Months Left to Spread Liability", "Amount": f"{months_remaining} Months"},
        {"Action / Milestone": "Mandatory Monthly Reserve Target", "Amount": format_indian_currency(monthly_tax_reserve_required)},
        {"Action / Milestone": "Current Safe Cash Buffer Today", "Amount": format_indian_currency(current_savings_balance - monthly_tax_reserve_required)}
    ]
    st.table(pd.DataFrame(runway_table))

with col_right:
    st.subheader("📊 Full-Year Target Reconciliation")
    
    reconciliation_table = [
        {"Ledger Item": "Selected Target Revenue (100%)", "Amount": format_indian_currency(target_total_revenue), "Ratio (%)": "100.00%"},
        {"Ledger Item": "Less: Total Estimated Tax Liability", "Amount": format_indian_currency(-total_projected_tax), "Ratio (%)": effective_tax_rate_pct},
        {"Ledger Item": "Net Post-Tax Income Retained", "Amount": format_indian_currency(projected_year_end_post_tax), "Ratio (%)": retention_rate_pct},
        {"Ledger Item": "Advance Tax Paid YTD", "Amount": format_indian_currency(advance_tax_paid), "Ratio (%)": "—"},
        {"Ledger Item": "TDS Credits Accumulated YTD", "Amount": format_indian_currency(tds_deducted_so_far), "Ratio (%)": "—"},
        {"Ledger Item": "Final Out-of-Pocket Tax Balance", "Amount": format_indian_currency(remaining_tax_payable), "Ratio (%)": f"{(remaining_tax_payable / target_total_revenue * 100):.2f}%"}
    ]
    st.table(pd.DataFrame(reconciliation_table))
