import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="True Free Cash Engine", page_icon="💰", layout="wide")

st.title("💼 True Free Cash & EOY Tax Forecasting Engine")
st.write("Strip away business overhead and accrued/predicted tax liabilities to see exactly what you can withdraw right now.")
st.write("---")

# Define the Indian Financial Year sequence (April to March)
FY_MONTHS = [
    "April", "May", "June", "July", "August", "September", 
    "October", "November", "December", "January", "February", "March"
]

# ==========================================
# 2. SIMULATED HISTORICAL DATA (DATABASE)
# ==========================================
# In a real setup, this data matches your historical actuals.
# We assume a baseline revenue of ₹5,00,000 and baseline overhead of ₹1,50,000 per month.
baseline_data = {
    "Month": FY_MONTHS,
    "Actual_Revenue": [500000] * 12,
    "Fixed_Overhead": [150000] * 12,
}
df_base = pd.DataFrame(baseline_data)

# ==========================================
# 3. INTERACTIVE CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.header("🛠️ Engine Controls")

# Control 1: Choose the active simulation month
current_month = st.sidebar.selectbox(
    "Select the Current Month:", 
    options=FY_MONTHS, 
    index=2 # Defaults to June
)
current_month_idx = FY_MONTHS.index(current_month)

st.sidebar.write("---")
st.sidebar.subheader("🔮 Future Monthly Overhead Adjustments")
st.sidebar.caption("Tweak overhead constraints for individual remaining months:")

# Track custom overhead inputs for each month
custom_overheads = {}

# ==========================================
# 4. CORE ENGINE LOGIC & CALCULATIONS
# ==========================================
# We loop through the fiscal year to separate Past, Present, and Future data arrays
final_monthly_records = []

# First, capture the user input for the CURRENT month's changeable overhead
st.sidebar.markdown(f"**Current Month ({current_month})**")
current_changeable_overhead = st.sidebar.number_input(
    f"Overhead for {current_month}:",
    min_value=0,
    value=int(df_base.loc[current_month_idx, "Fixed_Overhead"]),
    step=5000,
    key="current_oh"
)

# Build the 12-month matrix dynamically based on selections
for idx, row in df_base.iterrows():
    month_name = row["Month"]
    revenue = row["Actual_Revenue"]
    
    if idx < current_month_idx:
        # PAST MONTHS: Locked history
        status = "Past (Closed)"
        overhead = row["Fixed_Overhead"]
    elif idx == current_month_idx:
        # CURRENT MONTH: Driven by our main changeable variable
        status = "Present (Active)"
        overhead = current_changeable_overhead
    else:
        # FUTURE MONTHS: Default to current month's variable, but editable individually
        status = "Future (Projected)"
        overhead = st.sidebar.number_input(
            f"Projected Overhead ({month_name}):",
            min_value=0,
            value=int(current_changeable_overhead), # Pre-populates with current month's choice
            step=5000,
            key=f"oh_{month_name}"
        )
        
    net_profit = max(0, revenue - overhead)
    # Approximate Tax liability calculation (e.g., flat 25% corporate tax rate threshold)
    calculated_tax = net_profit * 0.25
    # Approximate TDS calculation (e.g., standard 10% on corporate revenue sourcing)
    calculated_tds = revenue * 0.10
    
    final_monthly_records.append({
        "Month": month_name,
        "Status": status,
        "Revenue": revenue,
        "Overhead": overhead,
        "Net Profit": net_profit,
        "Tax Liability": calculated_tax,
        "TDS": calculated_tds
    })

df_engine = pd.DataFrame(final_monthly_records)

# ==========================================
# 5. MAIN WINDOW DISPLAY & DASHBOARD INPUTS
# ==========================================
col_input1, col_input2 = st.columns(2)
with col_input1:
    bank_balance = st.number_input(
        "💵 Enter Your Current Bank Balance (₹):", 
        min_value=0, 
        value=1000000, 
        step=10000
    )
with col_input2:
    st.info(f"**Timeline Status:** Months before **{current_month}** are treated as finalized past quarters. Remaining months are auto-calculated extensions.")

st.write("---")

# Compute Present-Day True Cash Liquidity Blocks
past_and_present_df = df_engine.iloc[:current_month_idx + 1]
total_accrued_tax_liabilities = past_and_present_df["Tax Liability"].sum()
current_month_overhead_commitment = df_engine.loc[current_month_idx, "Overhead"]

# Ultimate Equation Execution
freely_withdrawable_cash = bank_balance - current_month_overhead_commitment - total_accrued_tax_liabilities

# ==========================================
# 6. VISUAL METRICS DISPLAY
# ==========================================
st.subheader("💰 Real-Time Wallet Authorization")

if freely_withdrawable_cash >= 0:
    st.success(f"### Freely Withdrawable Cash: **₹{freely_withdrawable_cash:,.2f}**")
else:
    st.error(f"### Shortfall Warning! Negative Liquidity Balance: **₹{freely_withdrawable_cash:,.2f}** (Reserve Capital Needed)")

# Explanatory Waterfall Breakdown
with st.expander("🔍 See Exactly How Your Balance Is Carved Up"):
    st.write(f"**Starting Bank Balance:** ₹{bank_balance:,.2f}")
    st.write(f"⚠️ *Minus* Current Month Business Overhead Reserve ({current_month}): -₹{current_month_overhead_commitment:,.2f}")
    st.write(f"⚠️ *Minus* Accrued Tax Ledger (All historical months up to and including {current_month}): -₹{total_accrued_tax_liabilities:,.2f}")
    st.write("---")
    st.write(f"**Final Liquid Free Capital Balance:** ₹{freely_withdrawable_cash:,.2f}")

st.write("---")

# ==========================================
# 7. END OF YEAR FORECASTING BLOCKS
# ==========================================
st.subheader("📊 Full-Year Fiscal Projections (EOY Estimates)")

eoy_revenue = df_engine["Revenue"].sum()
eoy_tax = df_engine["Tax Liability"].sum()
eoy_tds = df_engine["TDS"].sum()
eoy_corporate_tax_est = max(0, (eoy_revenue - df_engine["Overhead"].sum()) * 0.25)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Total Projected Revenue", value=f"₹{eoy_revenue:,.2f}")
with col_m2:
    st.metric(label="Est. Corporate Tax Owed", value=f"₹{eoy_corporate_tax_est:,.2f}")
with col_m3:
    st.metric(label="Estimated TDS Accrued", value=f"₹{eoy_tds:,.2f}")
with col_m4:
    st.metric(label="Net Final Tax Liability Check", value=f"₹{eoy_tax:,.2f}")

# Render complete monthly data matrix data block
st.write("### 📋 Underlying 12-Month Fiscal Spreadsheet Matrix")
st.dataframe(df_engine, use_container_width=True)