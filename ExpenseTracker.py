import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import re

# ==========================================
# 1. PAGE SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Operational Expense Tracker", page_icon="📊", layout="wide")

st.title("📊 Script 3: Autonomous Operational Expense Tracker")
st.write("Log, edit, and audit company operational overhead on the fly with real-time categorical bifurcation.")
st.write("---")

CSV_FILE = "company_expenses.csv"

# Define standard corporate expense categories
EXPENSE_CATEGORIES = [
    "🛠️ Fixed Operational Overhead (Rent, Utilities)",
    "💻 Software Subscriptions & IT Cloud Costs",
    "📈 Business Growth, Marketing & Ads",
    "👤 Director Remuneration, Travel & Perks",
    "📦 Office Supplies & Miscellaneous Logistics"
]

# ==========================================
# INDIAN NUMBER FORMATTING FUNCTION
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
            
        return f"-₹{result}.{dec_part}" if is_negative else f"₹{result}.{dec_part}"
    except Exception:
        return f"₹{val}"

# ==========================================
# DATA STORAGE METHODS (CSV)
# ==========================================
def load_expense_data():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Log ID", "Date", "Expense Name", "Category", "Amount (₹)", "Payment Mode"])
        df.to_csv(CSV_FILE, index=False)
        return df
    try:
        df = pd.read_csv(CSV_FILE)
        df["Log ID"] = df["Log ID"].astype(str)
        return df
    except Exception:
        return pd.DataFrame(columns=["Log ID", "Date", "Expense Name", "Category", "Amount (₹)", "Payment Mode"])

def save_all_data(df):
    df.to_csv(CSV_FILE, index=False)

# Initialize session state tracking
if "expense_df" not in st.session_state:
    st.session_state.expense_df = load_expense_data()

# ==========================================
# 2. SCREEN SPLIT LAYOUT
# ==========================================
col_left, col_right = st.columns([3, 2])

# ------------------------------------------
# LEFT COLUMN: INPUT CONTROLS & MANAGEMENT
# ------------------------------------------
with col_left:
    st.subheader("📥 Log New Transaction")
    
    with st.form("add_expense_form", clear_on_submit=True):
        exp_date = st.date_input("Transaction Date:", datetime.today())
        exp_name = st.text_input("Expense Title / Vendor Name:", placeholder="e.g., AWS Cloud Server Bill")
        exp_cat = st.selectbox("Assign Expense Category:", options=EXPENSE_CATEGORIES)
        exp_amt = st.number_input("Amount (INR):", min_value=0.0, step=500.0)
        exp_mode = st.selectbox("Payment Channel:", options=["Corporate Credit Card", "Net Banking Transfer", "Director Wallet Reimbursement", "Petty Cash"])
        
        submit_btn = st.form_submit_button("Lock Entry into CSV Ledger")
        
        if submit_btn:
            if exp_name.strip() == "" or exp_amt <= 0:
                st.error("⚠️ Failed to log entry. Please provide a valid vendor name and amount.")
            else:
                unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
                new_row = pd.DataFrame([{
                    "Log ID": str(unique_id),
                    "Date": exp_date.strftime("%Y-%m-%d"),
                    "Expense Name": exp_name,
                    "Category": exp_cat,
                    "Amount (₹)": float(exp_amt),
                    "Payment Mode": exp_mode
                }])
                
                st.session_state.expense_df = pd.concat([st.session_state.expense_df, new_row], ignore_index=True)
                save_all_data(st.session_state.expense_df)
                st.success(f"✓ Locked successfully: '{exp_name}' added to permanent storage ledger.")
                st.rerun()

# ------------------------------------------
# RIGHT COLUMN: REAL-TIME PIE BIFURCATION CHART
# ------------------------------------------
with col_right:
    st.subheader("📊 Live Burn-Rate Bifurcation")
    current_ledger = st.session_state.expense_df
    
    if current_ledger.empty:
        st.info("No corporate expenses logged yet. Graph will render automatically upon data injection.")
    else:
        total_sum = current_ledger["Amount (₹)"].sum()
        st.metric(label="Total Logged Run Rate Costs", value=format_indian_currency(total_sum))
        
        chart_df = current_ledger.groupby("Category")["Amount (₹)"].sum().reset_index()
        
        fig = px.pie(
            chart_df, 
            values="Amount (₹)", 
            names="Category", 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=300)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

st.write("---")

# ==========================================
# 3. INTERACTIVE EDIT & DELETE MANAGEMENT PANEL
# ==========================================
st.subheader("📜 Master Expense Ledger Audit & Correction Vault")

if st.session_state.expense_df.empty:
    st.caption("Permanent CSV database is currently pristine and empty.")
else:
    display_df = st.session_state.expense_df.copy()
    display_df["Formatted Amount"] = display_df["Amount (₹)"].apply(format_indian_currency)
    
    st.dataframe(
        display_df[["Date", "Expense Name", "Category", "Formatted Amount", "Payment Mode"]],
        use_container_width=True
    )
    
    st.markdown("#### 🛠️ Entry Modification & Deletion Console")
    st.caption("Select a transaction title below to modify its records or purge it from the underlying CSV database:")
    
    id_options = {row["Log ID"]: f"{row['Date']} | {row['Expense Name']} ({format_indian_currency(row['Amount (₹)'])})" for _, row in st.session_state.expense_df.iterrows()}
    
    selected_id = st.selectbox("Choose entry to alter:", options=list(id_options.keys()), format_func=lambda x: id_options[x])
    
    target_row = st.session_state.expense_df[st.session_state.expense_df["Log ID"] == selected_id].iloc[0]
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        edit_name = st.text_input("Modify Name:", value=target_row["Expense Name"])
        edit_cat = st.selectbox("Modify Category:", options=EXPENSE_CATEGORIES, index=EXPENSE_CATEGORIES.index(target_row["Category"]))
    with col_e2:
        edit_amt = st.number_input("Modify Amount (₹):", min_value=0.0, value=float(target_row["Amount (₹)"]), step=500.0)
        edit_mode = st.selectbox("Modify Payment Channel:", options=["Corporate Credit Card", "Net Banking Transfer", "Director Wallet Reimbursement", "Petty Cash"], index=["Corporate Credit Card", "Net Banking Transfer", "Director Wallet Reimbursement", "Petty Cash"].index(target_row["Payment Mode"]))
        
    col_b1, col_b2, _ = st.columns([1, 1, 4])
    
    with col_b1:
        if st.button("💾 Save Modifications", type="primary"):
            idx = st.session_state.expense_df[st.session_state.expense_df["Log ID"] == selected_id].index[0]
            st.session_state.expense_df.at[idx, "Expense Name"] = edit_name
            st.session_state.expense_df.at[idx, "Category"] = edit_cat
            st.session_state.expense_df.at[idx, "Amount (₹)"] = float(edit_amt)
            st.session_state.expense_df.at[idx, "Payment Mode"] = edit_mode
            
            save_all_data(st.session_state.expense_df)
            st.success("✓ CSV file records successfully overwritten.")
            st.rerun()
            
    with col_b2:
        if st.button("🗑️ Purge Entry Entirely"):
            st.session_state.expense_df = st.session_state.expense_df[st.session_state.expense_df["Log ID"] != selected_id]
            save_all_data(st.session_state.expense_df)
            st.warning("🗑️ Entry permanently expunged from database records.")
            st.rerun()
