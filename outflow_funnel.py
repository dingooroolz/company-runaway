import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="Expense Funnel Logger", page_icon="💧", layout="wide")

DATA_FILE = "expenses_log.csv"
CATEGORIES_FILE = "categories.txt"

DEFAULT_CATEGORIES = [
    "Corporate Overheads",
    "Contractors & Vendors",
    "Statutory & Taxes",
    "Director Remuneration",
    "Personal Discretionary",
    "Capital Investments"
]

def load_categories():
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, "r") as f:
            cats = [line.strip() for line in f if line.strip()]
        return cats if cats else DEFAULT_CATEGORIES
    return DEFAULT_CATEGORIES

def save_categories(cats):
    with open(CATEGORIES_FILE, "w") as f:
        for c in cats:
            f.write(f"{c}\n")

def load_expenses():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        return df
    return pd.DataFrame(columns=["Date", "Amount", "Category", "Note"])

def save_expense(dt, amt, cat, note):
    new_entry = pd.DataFrame([{"Date": dt, "Amount": float(amt), "Category": cat, "Note": note}])
    if os.path.exists(DATA_FILE):
        new_entry.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        new_entry.to_csv(DATA_FILE, index=False)

categories = load_categories()
df_expenses = load_expenses()

# Sidebar: Category Manager
st.sidebar.header("⚙️ Category Controller")
new_cat = st.sidebar.text_input("Add New Category:")
if st.sidebar.button("Add Category") and new_cat:
    if new_cat not in categories:
        categories.append(new_cat)
        save_categories(categories)
        st.sidebar.success(f"Added '{new_cat}'")
        st.rerun()

cat_to_remove = st.sidebar.selectbox("Remove Existing Category:", ["-- None --"] + categories)
if st.sidebar.button("Delete Category") and cat_to_remove != "-- None --":
    categories.remove(cat_to_remove)
    save_categories(categories)
    st.sidebar.warning(f"Removed '{cat_to_remove}'")
    st.rerun()

# Main Interactive Input Funnel
st.title("💧 Outflow Funnel Logger")
action = st.radio("Making an Expense?", ["No", "Yes"], horizontal=True)

if action == "Yes":
    with st.container():
        st.subheader("📝 Record Transaction Details")
        col1, col2 = st.columns(2)
        with col1:
            tx_amount = st.number_input("How much? (₹)", min_value=0.0, step=500.0, value=0.0)
            tx_date = st.date_input("Date of transaction:", value=date.today())
        with col2:
            tx_category = st.selectbox("What category?", categories)
            tx_note = st.text_input("Short note / Description (optional):", "")

        if st.button("Log Expense"):
            if tx_amount > 0:
                save_expense(tx_date, tx_amount, tx_category, tx_note)
                st.success(f"Logged ₹{tx_amount:,.2f} under '{tx_category}' on {tx_date}.")
                st.rerun()
            else:
                st.error("Amount must be greater than zero.")
else:
    st.info("System on standby. Select 'Yes' when an outflow occurs.")

st.write("---")

# Aggregated Analytics, Visuals & Logs
st.subheader("📊 Expense Catchment & Bifurcation Visuals")

if not df_expenses.empty:
    today = date.today()
    current_year = today.year
    current_month = today.month

    daily_total = df_expenses[df_expenses["Date"] == today]["Amount"].sum()
    monthly_total = df_expenses[
        (pd.to_datetime(df_expenses["Date"]).dt.year == current_year) &
        (pd.to_datetime(df_expenses["Date"]).dt.month == current_month)
    ]["Amount"].sum()
    overall_total = df_expenses["Amount"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Today's Outflow", f"₹{daily_total:,.2f}")
    m2.metric(f"Current Month ({today.strftime('%b %Y')})", f"₹{monthly_total:,.2f}")
    m3.metric("Overall Cumulative Outflow", f"₹{overall_total:,.2f}")

    # ==========================================
    # PIE CHART VISUALIZATIONS (REAL-TIME)
    # ==========================================
    st.write("---")
    st.subheader("🥧 Outflow Bifurcation Pies")

    df_viz = df_expenses.copy()
    df_viz["YearMonth"] = pd.to_datetime(df_viz["Date"]).dt.strftime('%B %Y')
    df_viz["SortPeriod"] = pd.to_datetime(df_viz["Date"]).dt.to_period("M")

    available_months_df = df_viz[["YearMonth", "SortPeriod"]].drop_duplicates().sort_values(by="SortPeriod", ascending=False)
    available_months = available_months_df["YearMonth"].tolist()

    selected_month = st.selectbox("📅 Select Month to Inspect Bifurcation:", available_months)
    df_selected_month = df_viz[df_viz["YearMonth"] == selected_month]

    col_pie1, col_pie2 = st.columns(2)

    with col_pie1:
        st.markdown(f"**Monthly Bifurcation: {selected_month}**")
        if not df_selected_month.empty:
            m_grouped = df_selected_month.groupby("Category")["Amount"].sum()
            fig1, ax1 = plt.subplots(figsize=(6, 6))
            ax1.pie(
                m_grouped, 
                labels=m_grouped.index, 
                autopct='%1.1f%%', 
                startangle=140, 
                wedgeprops=dict(width=0.45, edgecolor='w')
            )
            ax1.axis('equal')
            fig1.patch.set_alpha(0.0)
            st.pyplot(fig1)
        else:
            st.info("No records found for the selected month.")

    with col_pie2:
        st.markdown("**Overall Cumulative Bifurcation (All-Time)**")
        o_grouped = df_viz.groupby("Category")["Amount"].sum()
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(
            o_grouped, 
            labels=o_grouped.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            wedgeprops=dict(width=0.45, edgecolor='w')
        )
        ax2.axis('equal')
        fig2.patch.set_alpha(0.0)
        st.pyplot(fig2)

    # Tables and Export Tabs
    st.write("---")
    tab1, tab2 = st.tabs(["By Category Breakdown", "Full Transaction Log & Export"])
    
    with tab1:
        cat_breakdown = df_expenses.groupby("Category")["Amount"].agg(["sum", "count"]).reset_index()
        cat_breakdown.columns = ["Category", "Total Discharged (₹)", "Transaction Count"]
        cat_breakdown["Overall Share (%)"] = (cat_breakdown["Total Discharged (₹)"] / overall_total * 100).map("{:.2f}%".format)
        cat_breakdown["Total Discharged (₹)"] = cat_breakdown["Total Discharged (₹)"].map("₹{:,.2f}".format)
        st.table(cat_breakdown)
        
    with tab2:
        st.dataframe(df_expenses.sort_values(by="Date", ascending=False), use_container_width=True)
        
        csv_data = df_expenses.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Ledger to CSV (Excel Compatible)",
            data=csv_data,
            file_name=f"expense_funnel_ledger_{today}.csv",
            mime="text/csv",
        )
else:
    st.write("No expenses recorded yet.")
