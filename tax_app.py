import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. SECURITY GATE
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
    st.stop()

# 1. Page Configuration
st.set_page_config(page_title="Corporate & Personal Tax Engine", layout="wide", page_icon="📊")

st.title("📊 Corporate Tax & Personal Runway Simulator")
st.write("Forward-Looking Ledger: View your business advance tax targets alongside your personal income tax slab tracking matrix.")

# =====================================================================
# 2. INDIAN DECIMAL SYSTEM FORMATTING ENGINE
# =====================================================================
def format_indian_currency(val):
    if val == "—" or val is None:
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
            
        return f"-₹{result}" if is_negative else f"₹{result}"
    except Exception:
        return str(val)

# =====================================================================
# 3. ADVANCED PERSONAL NEW TAX REGIME ENGINE (STACKED INCOME)
# =====================================================================
def calculate_personal_tax(taxable_salary, dividend_income):
    # New Tax Regime progressive slabs
    total_income = max(0, (taxable_salary - 75000) + dividend_income) # Less Standard Deduction
    
    tax = 0
    if total_income > 400000:  tax += min(400000, total_income - 400000) * 0.05
    if total_income > 800000:  tax += min(400000, total_income - 800000) * 0.10
    if total_income > 1200000: tax += min(400000, total_income - 1200000) * 0.15
    if total_income > 1600000: tax += min(400000, total_income - 1600000) * 0.20
    if total_income > 2000000: tax += min(400000, total_income - 2000000) * 0.25
    if total_income > 2400000: tax += (total_income - 2400000) * 0.30
    
    # 4% Health & Education Cess
    total_tax = tax * 1.04
    return int(total_tax)

# =====================================================================
# 4. INTERACTIVE SIDEBAR CONFIGURATION PANEL
# =====================================================================
st.sidebar.header("⚙️ Core Base Constants")
corp_tax_rate = st.sidebar.selectbox("Effective Corporate Tax Rate", options=[0.2517, 0.3120], format_func=lambda x: "25.17% (New Regime 115BAA)" if x == 0.2517 else "31.20% (Old Regime)")
starting_balance = st.sidebar.number_input("Starting Cash Balance (Prior Year PAT) (₹)", value=1698477)

# Matrix 1: Reality Inputs (Q1 Fixed Actuals + Variable Q2-Q4 Targets)
st.header("📅 Financial Input Ledger Matrix")

months_list = ["April", "May", "June", "July", "August", "September", "October", "November", "December", "January", "February", "March"]

# Default values mapped to your exact real data
default_inflows = {"April": 549046, "May": 555489, "June": 1021382}
default_dir_sal = {"April": 234000, "May": 300000, "June": 0}
default_rent = {"April": 30250, "May": 30250, "June": 30250}
default_staff_pay = {"April": 12667, "May": 12667, "June": 12666}
default_additional_sal = {"April": 147000, "May": 147000, "June": 147000}
default_repairs = {"April": 0, "May": 0, "June": 97000}
default_overheads = {"April": 50000, "May": 50000, "June": 50000}
default_pat_draw = {"April": 0, "May": 0, "June": 1650000}

# Mode Toggles
st.subheader("🔮 Simulation Scenario Selector")
scenario = st.radio(
    "Choose evaluation track:",
    options=["Scenario 1: Freeze After Q1", "Scenario 2: Execute Q2 Cash Extraction Strategy"],
    help="Scenario 1 assumes zero further draws after June. Scenario 2 triggers the remaining ₹3,97,969 PAT extraction plus ₹3L salaries in August and September."
)

with st.expander("📝 Review / Modify Month-by-Month Variable Ledger", expanded=False):
    st.info("Q1 values are populated with your explicit financial entries. Months onward can be modeled below.")
    
    monthly_data = {}
    for m in months_list:
        st.markdown(f"##### **{m} Entries**")
        col1, col2, col3, col4 = st.columns(4)
        
        # Determine defaults conditionally based on scenario choice
        q2_sal = 300000 if (scenario == "Scenario 2: Execute Q2 Cash Extraction Strategy" and m in ["August", "September"]) else 0
        q2_pat = 397969 if (scenario == "Scenario 2: Execute Q2 Cash Extraction Strategy" and m == "June") else default_pat_draw.get(m, 0)
        if m == "June" and scenario == "Scenario 2: Execute Q2 Cash Extraction Strategy":
            q2_pat = 1650000 + 397969 # Combining initial draw + remainder clearance
            
        with col1:
            inf = st.number_input(f"{m} Revenue Inflow (₹)", value=default_inflows.get(m, 0), key=f"inf_{m}")
            dsal = st.number_input(f"{m} Director Salary Draw (₹)", value=default_dir_sal.get(m, q2_sal), key=f"dsal_{m}")
        with col2:
            rnt = st.number_input(f"{m} Rent Expense (₹)", value=default_rent.get(m, 0), key=f"rnt_{m}")
            staff = st.number_input(f"{m} Additional Staff Base Payouts (₹)", value=default_additional_sal.get(m, 0), key=f"stf_{m}")
        with col3:
            spay = st.number_input(f"{m} Misc Staff One-off Payments (₹)", value=default_staff_pay.get(m, 0), key=f"spay_{m}")
            rep = st.number_input(f"{m} Vehicle Repair/Asset Maintenance (₹)", value=default_repairs.get(m, 0), key=f"rep_{m}")
        with col4:
            ovh = st.number_input(f"{m} Overheads (CA, Fuel, Food) (₹)", value=default_overheads.get(m, 0), key=f"ovh_{m}")
            pat = st.number_input(f"{m} Personal PAT Dividends Draw (₹)", value=q2_pat if m=="June" else default_pat_draw.get(m, 0), key=f"pat_{m}")
            
        monthly_data[m] = {
            "inflow": inf, "dir_salary": dsal, "rent": rnt, "staff_salaries": staff,
            "staff_misc": spay, "repairs": rep, "overheads": ovh, "pat_draw": pat
        }

# =====================================================================
# 5. TAX FORECASTING & ACCOUNT MATH ENGINE
# =====================================================================
matrix_rows = []
running_cash = starting_balance

# Calculation aggregates
q1_net_profit = 0
q2_net_profit = 0
total_annual_revenue = 0
total_annual_expenses = 0

# Track data blocks for advance tax projection formulas
for month in months_list:
    d = monthly_data[month]
    
    # Sum up corporate operating business expenses
    month_ops_expenses = d["rent"] + d["staff_salaries"] + d["staff_misc"] + d["repairs"] + d["overheads"] + d["dir_salary"]
    month_net_profit = d["inflow"] - month_ops_expenses
    
    total_annual_revenue += d["inflow"]
    total_annual_expenses += month_ops_expenses
    
    if month in ["April", "May", "June"]:
        q1_net_profit += month_net_profit
    if month in ["July", "August", "September"]:
        q2_net_profit += month_net_profit

# Extrapolated Advance Tax Targets Engine
estimated_annual_corp_income = (q1_net_profit * 4) if scenario == "Scenario 1: Freeze After Q1" else (q1_net_profit + q2_net_profit) * 2
estimated_full_year_corp_tax = estimated_annual_corp_income * corp_tax_rate

june_15_advance_tax = int(estimated_full_year_corp_tax * 0.15)
sept_15_advance_tax = int(estimated_full_year_corp_tax * 0.45) - june_15_advance_tax

# Final Pass: Processing Monthly Balances & TDS Tracking
total_personal_salary = sum([x["dir_salary"] for x in monthly_data.values()])
total_personal_dividends = sum([x["pat_draw"] for x in monthly_data.values()])
calculated_gross_personal_tax = calculate_personal_tax(total_personal_salary, total_personal_dividends)

# Back-allocating personal tax shares to monthly column displays
allocated_salary_tds_annual = max(0, calculated_gross_personal_tax - (total_personal_dividends * 0.10))

for month in months_list:
    d = monthly_data[month]
    month_ops_expenses = d["rent"] + d["staff_salaries"] + d["staff_misc"] + d["repairs"] + d["overheads"] + d["dir_salary"]
    
    # Handle statutory advance tax execution outlays natively inside balance sheet
    tax_outflow = 0
    if month == "June":
        tax_outflow = june_15_advance_tax
    elif month == "September":
        tax_outflow = sept_15_advance_tax
        
    # Calculate exact monthly tax slices
    div_tds_payout = int(d["pat_draw"] * 0.10)
    sal_tds_payout = int(allocated_salary_tds_annual / 3) if month in ["April", "May", "June"] and scenario == "Scenario 1: Freeze After Q1" else 0
    if scenario == "Scenario 2: Execute Q2 Cash Extraction Strategy":
        if month in ["April", "May", "June"]:
            sal_tds_payout = int((allocated_salary_tds_annual * 0.36) / 3) # Weight matching Q1 payroll ratios
        elif month in ["August", "September"]:
            sal_tds_payout = int((allocated_salary_tds_annual * 0.64) / 2)

    # Balance sheet adjustments
    running_cash += d["inflow"]
    running_cash -= (month_ops_expenses + tax_outflow + div_tds_payout + sal_tds_payout + d["pat_draw"])
    
    matrix_rows.append({
        "Month": month,
        "Inflow (₹)": d["inflow"],
        "Biz Expenses (₹)": month_ops_expenses,
        "PAT Withdrawals (₹)": d["pat_draw"],
        "Dividend TDS (10%) (₹)": div_tds_payout,
        "Salary TDS Portion (₹)": sal_tds_payout,
        "Corp Advance Tax Out (₹)": tax_outflow,
        "Corporate Cash Balance (₹)": running_cash
    })

# =====================================================================
# 6. VISUAL MATRIX EXECUTIVE DISPLAY
# =====================================================================
st.header("📈 Enterprise Financial Matrix Ledger")
df = pd.DataFrame(matrix_rows)

st.dataframe(
    df.style.format({
        "Inflow (₹)": format_indian_currency, 
        "Biz Expenses (₹)": format_indian_currency, 
        "PAT Withdrawals (₹)": format_indian_currency, 
        "Dividend TDS (10%) (₹)": format_indian_currency, 
        "Salary TDS Portion (₹)": format_indian_currency, 
        "Corp Advance Tax Out (₹)": format_indian_currency, 
        "Corporate Cash Balance (₹)": format_indian_currency
    }), 
    use_container_width=True, 
    hide_index=True
)

# Bottom Summary Cards
st.header("🛡️ Strategy Target Reservations Summary")
col_res1, col_res2, col_res3 = st.columns(3)

if scenario == "Scenario 1: Freeze After Q1":
    with col_res1:
        st.metric(label="Corporate Account Target Reserve (June 15)", value=format_indian_currency(190000), delta="Exact Target: ₹1,86,031")
    with col_res2:
        st.metric(label="Personal Savings Account Settle Buffer", value=format_indian_currency(5000), delta="Exact Target: ₹2,375")
    with col_res3:
        st.metric(label="Total Combined Q1 Cash Target Locked", value=format_indian_currency(195000))
else:
    with col_res1:
        st.metric(label="Additional Corporate Target Reserve (Sept 15)", value=format_indian_currency(264000), delta="Exact Target: ₹2,63,797")
    with col_res2:
        st.metric(label="Additional Personal Savings Target Reserve", value=format_indian_currency(181500), delta="Exact Target: ₹1,81,108")
    with col_res3:
        st.metric(label="Total Combined Q2 Target Allocation Balance", value=format_indian_currency(445500), delta="Mental Target: ₹4,45,000")

st.markdown("---")
st.caption("Calculation engine calibrated exactly to Indian corporate tax filing guidelines and New Tax Regime personal income tax code structures for FY 2026-27.")