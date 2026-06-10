import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. SECURITY GATE: This stops the app unless the key is right
# ---------------------------------------------------------
def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Private Financial Access")
    pwd = st.text_input("Enter the firm's access key:", type="password")
    
    if st.button("Unlock Dashboard"):
        if pwd == "MyFirm2026":  # <--- CHANGE THIS TO YOUR PASSWORD
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("🚫 Incorrect key.")
    return False

if not check_password():
    st.stop()  # This prevents the rest of the code from running
# ---------------------------------------------------------
# SECURITY END - YOUR ORIGINAL CODE CONTINUES BELOW
# ---------------------------------------------------------

# 1. Page Configuration
st.set_page_config(page_title="Runway Engine", layout="wide")

st.title("📊 Company Runway Simulator")
st.write("Forward-Looking Ledger: View your optimized monthly disposable income buffer alongside your live running tracking matrix.")

# =====================================================================
# 2. INDIAN DECIMAL SYSTEM FORMATTING ENGINE
# =====================================================================
def format_indian_currency(val):
    if val == "—":
        return val
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
            
        return f"-{result}" if is_negative else result
    except Exception:
        return str(val)

# =====================================================================
# 3. STATUTORY TDS CALCULATOR
# =====================================================================
def calculate_statutory_tds(monthly_net_salary):
    if monthly_net_salary <= 0:
        return 0
    annual_net_target = monthly_net_salary * 12
    low_gross, high_gross = annual_net_target, annual_net_target * 4
    precise_gross = low_gross
    
    for _ in range(50):
        mid_gross = (low_gross + high_gross) / 2
        taxable_income = max(0, mid_gross - 75000)
        
        tax = 0
        if taxable_income > 400000:  tax += min(400000, taxable_income - 400000) * 0.05
        if taxable_income > 800000:  tax += min(400000, taxable_income - 800000) * 0.10
        if taxable_income > 1200000: tax += min(400000, taxable_income - 1200000) * 0.15
        if taxable_income > 1600000: tax += min(400000, taxable_income - 1600000) * 0.20
        if taxable_income > 2000000: tax += min(400000, taxable_income - 2000000) * 0.25
        if taxable_income > 2400000: tax += (taxable_income - 2400000) * 0.30
            
        surcharge_rate = 0.0
        if mid_gross > 5000000 and mid_gross <= 10000000:
            surcharge_rate = 0.10
        elif mid_gross > 10000000 and mid_gross <= 20000000:
            surcharge_rate = 0.15
        elif mid_gross > 20000000:
            surcharge_rate = 0.25
            
        total_tax = tax * (1 + surcharge_rate) * 1.04
        
        if mid_gross - total_tax < annual_net_target:
            low_gross = mid_gross
        else:
            high_gross = mid_gross; precise_gross = mid_gross
            
    return int((precise_gross - annual_net_target) / 12)

def highlight_negatives(row):
    try:
        val = row['Running Balance (₹)']
        if isinstance(val, (int, float)) and val < 0:
            return ['background-color: #FADBD8; color: #78281F'] * len(row)
    except:
        pass
    return [''] * len(row)

# =====================================================================
# 4. INTERACTIVE CONFIGURATION PANEL
# =====================================================================
st.header("🔧 App Variables")

months_list = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# Real-World Balance Anchor
st.subheader("📍 Real-World Balance Anchor")
col_anc1, col_anc2 = st.columns(2)
with col_anc1:
    anchor_month = st.selectbox("Select Active Reality Month", options=months_list, index=1) 
with col_anc2:
    anchor_balance = st.number_input(f"Actual Net Balance for {anchor_month} (Post-all Inflows/PAT/Draws) (₹)", value=295000, step=50000)

# Core Overheads Panel
st.subheader("🏢 Monthly Fixed Overheads")
col_main1, col_main2, col_main3 = st.columns(3)
with col_main1:
    Staff_Salaries  = st.number_input("Staff Salaries Total (₹)", value=174000, step=5000)
with col_main2:
    Rent            = st.number_input("Office Rent (₹)", value=27500, step=500)
with col_main3:
    Other_Expenses  = st.number_input("Other Expenses (Food, Stationery, Fuel, Fees) (₹)", value=60000, step=1000)

# Matrix 1: Revenue Inflows
st.subheader("💰 Monthly Revenue Inflow Matrix")
monthly_inflows = {}
with st.expander("📅 Expand Month-by-Month Revenue Inputs", expanded=False):
    inf_col1, inf_col2, inf_col3, inf_col4 = st.columns(4)
    with inf_col1:
        monthly_inflows["April"]     = st.number_input("April Inflow (₹)", value=698069, step=10000)
        monthly_inflows["May"]       = st.number_input("May Inflow (₹)", value=698069, step=10000)
        monthly_inflows["June"]      = st.number_input("June Inflow (₹)", value=698069, step=10000)
    with inf_col2:
        monthly_inflows["July"]      = st.number_input("July Inflow (₹)", value=698069, step=10000)
        monthly_inflows["August"]    = st.number_input("August Inflow (₹)", value=698069, step=10000)
        monthly_inflows["September"] = st.number_input("Sept Inflow (₹)", value=698069, step=10000)
    with inf_col3:
        monthly_inflows["October"]   = st.number_input("Oct Inflow (₹)", value=698069, step=10000)
        monthly_inflows["November"]  = st.number_input("Nov Inflow (₹)", value=698069, step=10000)
        monthly_inflows["December"]  = st.number_input("Dec Inflow (₹)", value=698069, step=10000)
    with inf_col4:
        monthly_inflows["January"]   = st.number_input("Jan Inflow (₹)", value=698069, step=10000)
        monthly_inflows["February"]  = st.number_input("Feb Inflow (₹)", value=698069, step=10000)
        monthly_inflows["March"]     = st.number_input("March Inflow (₹)", value=698069, step=10000)

# Matrix 2: Director Regular Remuneration (Subject to TDS)
st.subheader("👨‍💼 Director Regular Remuneration (TDS Tracked)")
director_salaries = {}
with st.expander("📅 Expand Month-by-Month Base Salary Inputs", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        director_salaries["April"]     = st.number_input("April Salary Net (₹)", value=300000, step=10000)
        director_salaries["May"]       = st.number_input("May Salary Net (₹)", value=300000, step=10000)
        director_salaries["June"]      = st.number_input("June Salary Net (₹)", value=300000, step=10000)
    with col2:
        director_salaries["July"]      = st.number_input("July Salary Net (₹)", value=300000, step=10000)
        director_salaries["August"]    = st.number_input("August Salary Net (₹)", value=300000, step=10000)
        director_salaries["September"] = st.number_input("Sept Salary Net (₹)", value=300000, step=10000)
    with col3:
        director_salaries["October"]   = st.number_input("Oct Salary Net (₹)", value=300000, step=10000)
        director_salaries["November"]  = st.number_input("Nov Salary Net (₹)", value=300000, step=10000)
        director_salaries["December"]  = st.number_input("Dec Salary Net (₹)", value=300000, step=10000)
    with col4:
        director_salaries["January"]   = st.number_input("Jan Salary Net (₹)", value=300000, step=10000)
        director_salaries["February"]  = st.number_input("Feb Salary Net (₹)", value=300000, step=10000)
        director_salaries["March"]     = st.number_input("March Salary Net (₹)", value=300000, step=10000)

# Isolated Total Tax on Last Year's PAT Configurator
st.subheader("📋 Prior-Year PAT Tax Settings (Distributed Column)")
total_pat_tax = st.number_input("Total Corporate Tax Levied on Last Year's PAT (₹)", value=802846, step=12000)
tax_monthly_split = int(total_pat_tax / 12)

# =====================================================================
# 5. TWO-PASS MATHEMATICAL FORECASTING ENGINE
# =====================================================================
total_monthly_ops = Staff_Salaries + Rent + Other_Expenses
total_annual_revenue = sum(monthly_inflows.values())

# --- PASS 1: Calculate Year-End Surplus Pre-emptively ---
calc_balance = 0
past_anc = False
for m in months_list:
    if m == anchor_month:
        calc_balance = anchor_balance
        past_anc = True
    elif past_anc:
        calc_balance += monthly_inflows[m]
        calc_balance -= total_monthly_ops
        calc_balance -= tax_monthly_split
        calc_balance -= calculate_statutory_tds(director_salaries[m])
        calc_balance -= director_salaries[m]

final_surplus = calc_balance if past_anc else 0
# Safe monthly extraction slice (only generated if company finishes in net positive surplus)
monthly_disposable_buffer = int(final_surplus / 12) if final_surplus > 0 else 0

# --- PASS 2: Construct Visual Grid Matrix Ledger ---
current_balance = 0
past_the_anchor = False
total_annual_director_tds = 0
matrix_rows = []

for month in months_list:
    month_inflow   = monthly_inflows[month]
    month_salary   = director_salaries[month]
    month_tds      = calculate_statutory_tds(month_salary)
    
    total_annual_director_tds += month_tds
    
    if month == anchor_month:
        current_balance = anchor_balance
        balance_display = current_balance
        buffer_display  = monthly_disposable_buffer
        past_the_anchor = True
    elif past_the_anchor:
        current_balance += month_inflow
        current_balance -= total_monthly_ops
        current_balance -= tax_monthly_split
        current_balance -= month_tds
        current_balance -= month_salary
        balance_display = current_balance
        buffer_display  = monthly_disposable_buffer
    else:
        balance_display = "—"
        buffer_display  = "—"
    
    matrix_rows.append({
        "Month": month,
        "Monthly Inflow (₹)": month_inflow,
        "Operating Overheads (₹)": total_monthly_ops,
        "PAT Tax (1/12 Split) (₹)": tax_monthly_split,
        "Director TDS Column (₹)": month_tds,
        "Director Base Salary (₹)": month_salary,
        "Safe Extra Disposable / Mo (₹)": buffer_display,
        "Running Balance (₹)": balance_display
    })

# =====================================================================
# 6. VISUAL MATRIX EXECUTIVE DISPLAY
# =====================================================================
st.header("📈 Financial Projections Matrix Ledger")
df = pd.DataFrame(matrix_rows)

styled_df = df.style.apply(highlight_negatives, axis=1).format({
    "Monthly Inflow (₹)": format_indian_currency, 
    "Operating Overheads (₹)": format_indian_currency, 
    "PAT Tax (1/12 Split) (₹)": format_indian_currency, 
    "Director TDS Column (₹)": format_indian_currency, 
    "Director Base Salary (₹)": format_indian_currency, 
    "Safe Extra Disposable / Mo (₹)": format_indian_currency, 
    "Running Balance (₹)": format_indian_currency
})

st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Percentage of Revenue Calculations (Safe Guard against Division by Zero)
if total_annual_revenue > 0:
    pct_pat = (total_pat_tax / total_annual_revenue) * 100
    pct_tds = (total_annual_director_tds / total_annual_revenue) * 100
    pct_surplus = (current_balance / total_annual_revenue) * 100
    
    delta_pat = f"{pct_pat:.2f}% of Revenue"
    delta_tds = f"{pct_tds:.2f}% of Revenue"
    delta_surplus = f"{pct_surplus:.2f}% of Revenue"
else:
    delta_pat = "0.00% of Revenue"
    delta_tds = "0.00% of Revenue"
    delta_surplus = "0.00% of Revenue"

col_res1, col_res2, col_res3, col_res4 = st.columns(4)

with col_res1:
    st.metric(
        label="Total Modeled Annual Revenue", 
        value=f"₹{format_indian_currency(total_annual_revenue)}"
    )

with col_res2:
    st.metric(
        label="Total Annual PAT Tax Settled", 
        value=f"₹{format_indian_currency(total_pat_tax)}",
        delta=delta_pat,
        delta_color="off"
    )

with col_res3:
    st.metric(
        label="Total Annual Director TDS", 
        value=f"₹{format_indian_currency(total_annual_director_tds)}",
        delta=delta_tds,
        delta_color="off"
    )

with col_res4:
    # Keeps the red error color context if the business drops into deficit
    warning_label = delta_surplus if current_balance >= 0 else f"{delta_surplus} | DEFICIT WARNING"
    st.metric(
        label="March 31 Fiscal Surplus", 
        value=f"₹{format_indian_currency(current_balance)}",
        delta=warning_label,
        delta_color="off" if current_balance >= 0 else "inverse"
    )
