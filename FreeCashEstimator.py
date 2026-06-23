import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="True Free Cash Engine", page_icon="💰", layout="wide")

st.title("💼 True Free Cash & EOY Tax Forecasting Engine")
st.write("Automatically grosses up your net director salary to track real-world business deductions and optimize corporate tax reservations.")
st.write("---")

# Define the Indian Financial Year sequence (April to March)
FY_MONTHS = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# Default baseline assumptions
BASELINE_REV = 500000
BASELINE_NET_SALARY = 300000
BASELINE_OH = 150000

# ==========================================
# 2. AUTOMATED SALARY GROSS-UP FUNCTION (Section 192 Slabs)
# ==========================================
def calculate_gross_salary_and_tds(target_net_monthly):
    """
    Back-calculates the required Gross Monthly Salary and Monthly TDS 
    to yield the user's targeted monthly net take-home pay.
    Accounts for standard deduction (₹75,000) and default New Tax Regime slabs.
    """
    if target_net_monthly <= 0:
        return 0.0, 0.0
        
    target_net_annual = target_net_monthly * 12
    
    # Numerical convergence to find exact gross matching net after slab layout
    low_gross = target_net_annual
    high_gross = target_net_annual * 2
    exact_gross_annual = target_net_annual
    
    for _ in range(50): # 50 iterations provides precise decimal accuracy
        mid_gross = (low_gross + high_gross) / 2
        taxable_salary = max(0, mid_gross - 75000) # Standard Deduction
        
        # Apply standard tax regime slab logic
        tax = 0
        if taxable_salary > 2400000:
            tax += (taxable_salary - 2400000) * 0.30 + 300000
        elif taxable_salary > 2000000:
            tax += (taxable_salary - 2000000) * 0.25 + 200000
        elif taxable_salary > 1600000:
            tax += (taxable_salary - 1600000) * 0.20 + 120000
        elif taxable_salary > 1200000:
            tax += (taxable_salary - 1200000) * 0.15 + 60000
        elif taxable_salary > 800000:
            tax += (taxable_salary - 800000) * 0.10 + 20000
        elif taxable_salary > 400000:
            tax += (taxable_salary - 400000) * 0.05
            
        # Add 4% Health & Education Cess
        total_personal_tax = tax * 1.04
        
        # Apply Section 87A rebate safety net if taxable income is <= 12 Lakhs
        if taxable_salary <= 1200000:
            total_personal_tax = 0
            
        calculated_net = mid_gross - total_personal_tax
        
        if abs(calculated_net - target_net_annual) < 1:
            exact_gross_annual = mid_gross
            break
        elif calculated_net < target_net_annual:
            low_gross = mid_gross
        else:
            high_gross = mid_gross

    gross_monthly = exact_gross_annual / 12
    tds_monthly = (exact_gross_annual - target_net_annual) / 12
    return gross_monthly, tds_monthly

# ==========================================
# 3. INTERACTIVE CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.header("🛠️ Engine Controls")

current_month = st.sidebar.selectbox(
    "Select the Current Active Month:", 
    options=FY_MONTHS, 
    index=2 # Defaults to June
)
current_month_idx = FY_MONTHS.index(current_month)

# --- SIDEBAR SECTION 1: PAST MONTHS ACTUALS ---
st.sidebar.write("---")
st.sidebar.subheader("📜 Past Months (Historical Actuals)")
st.sidebar.caption("Input your true actual revenues for already closed months:")

past_revenues = {}
for idx in range(current_month_idx):
    m_name = FY_MONTHS[idx]
    past_revenues[m_name] = st.sidebar.number_input(
        f"Actual Revenue for {m_name}:",
        min_value=0,
        value=BASELINE_REV,
        step=25000,
        key=f"past_rev_{m_name}"
    )

# --- SIDEBAR SECTION 2: CURRENT MONTH TUNING ---
st.sidebar.write("---")
st.sidebar.subheader("📊 Current Month Tuning")
st.sidebar.markdown(f"**Current Month ({current_month})**")

current_active_revenue = st.sidebar.number_input(
    f"Revenue for {current_month}:",
    min_value=0,
    value=BASELINE_REV,
    step=25000,
    key="current_rev"
)

current_net_target = st.sidebar.number_input(
    f"Target NET Take-Home Salary ({current_month}):",
    min_value=0,
    value=BASELINE_NET_SALARY,
    step=10000,
    key="current_net_salary"
)
current_gross_salary, current_monthly_tds = calculate_gross_salary_and_tds(current_net_target)

# --- SIDEBAR SECTION 3: FUTURE MONTHS PROJECTIONS ---
st.sidebar.write("---")
st.sidebar.subheader("🔮 Remaining Months Projections")
st.sidebar.caption("Independently adjust expected revenue and operational constraints:")

# ==========================================
# 4. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
final_monthly_records = []

for idx, m_name in enumerate(FY_MONTHS):
    if idx < current_month_idx:
        status = "Past (Closed)"
        revenue = past_revenues[m_name]
        net_sal = BASEION_NET_SALARY if 'current_net_target' not in locals() else current_net_target
        gross_sal, tds
