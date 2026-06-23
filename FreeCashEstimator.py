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
# 2. AUTOMATED SALARY GROSS-UP FUNCTION
# ==========================================
def calculate_gross_salary_and_tds(target_net_monthly):
    """
    Safely back-calculates required Gross Monthly Salary and Monthly TDS.
    """
    try:
        target_net_monthly = float(target_net_monthly)
        if target_net_monthly <= 0:
            return 0.0, 0.0
            
        target_net_annual = target_net_monthly * 12.0
        
        low_gross = target_net_annual
        high_gross = target_net_annual * 3.0
        exact_gross_annual = target_net_annual
        
        # Safe bounded loop
        for _ in range(40):
            mid_gross = (low_gross + high_gross) / 2.0
            taxable_salary = max(0.0, mid_gross - 75000.0)
            
            tax = 0.0
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
                
            total_personal_tax = tax * 1.04
            
            if taxable_salary <= 1200000:
                total_personal_tax = 0.0
                
            calculated_net = mid_gross - total_personal_tax
            
            if abs(calculated_net - target_net_annual) < 10.0:
                exact_gross_annual = mid_gross
                break
            elif calculated_net < target_net_annual:
                low_gross = mid_gross
            else:
                high_gross = mid_gross

        gross_monthly = exact_gross_annual / 12.0
        tds_monthly = (exact_gross_annual - target_net_annual) / 12.0
        return float(gross_monthly), float(tds_monthly)
    except Exception:
