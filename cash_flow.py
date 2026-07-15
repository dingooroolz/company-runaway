# ==========================================
# 4. SIDE-BY-SIDE LEDGER DISPLAY RENDER
# ==========================================
col_left, col_right = st.columns(2)

# LEFT VIEWPORT: CORPORATE ANALYTICS
with col_left:
    st.subheader("🏢 Projected Corporate Scenario Breakdown")
    
    st.metric(label="📊 Estimated Corporate Tax Owed", value=format_indian_currency(modeled_corporate_tax), delta=f"{corp_tax_pct} of Revenue", delta_color="off")
    st.metric(label="🏛️ Net Company Retained Surplus (Profit)", value=format_indian_currency(net_company_retained_surplus), delta=f"{corp_net_profit_pct} of Revenue", delta_color="off")
    
    corp_matrix = [
        {"Operational Item": "Imagined Gross Revenue", "Value": format_indian_currency(scen_annual_revenue), "Ratio (%)": "100.00%"},
        {"Operational Item": "Less: Annual Overheads", "Value": f"- {format_indian_currency(scen_annual_overhead)}", "Ratio (%)": get_corp_pct(scen_annual_overhead)},
        {"Operational Item": "Less: Deductible Salaries/Bonuses", "Value": f"- {format_indian_currency(total_deductible_drawings)}", "Ratio (%)": corp_drawings_pct},
        {"Operational Item": "Mandatory Total Corporate TDS Withheld", "Value": format_indian_currency(total_corporate_withheld_tds), "Ratio (%)": corp_tds_pct},
        {"Operational Item": "Corporate Taxable Income Base", "Value": format_indian_currency(corporate_taxable_surplus), "Ratio (%)": get_corp_pct(corporate_taxable_surplus)}
    ]
    st.table(pd.DataFrame(corp_matrix))

# RIGHT VIEWPORT: PERSONAL SAVINGS ANALYTICS
with col_right:
    st.subheader("🏦 Projected Personal Wealth Matrix")
    
    # Calculate what percentage your true net safe surplus is out of the personal influx received
    pers_net_surplus_of_influx_pct = f"{(safely_disposable_annual_surplus / net_payout_injected * 100):.2f}%" if net_payout_injected > 0 else "0.00%"
    
    st.metric(label="💎 True Safe Disposable Annual Surplus", value=format_indian_currency(safely_disposable_annual_surplus), delta=f"{pers_net_surplus_of_influx_pct} of Net Influx Saved", delta_color="normal")
    st.metric(label="🏛️ Net Remaining Personal Tax Shortfall", value=format_indian_currency(net_personal_tax_shortfall), delta_color="inverse")
    
    pers_matrix = [
        {"Wealth Item": "Starting Cash Balance Baseline", "Value": format_indian_currency(scen_savings_base), "Ratio (% of Cash Influx)": "—"},
        {"Wealth Item": "Add: Net Income Payout Influx (Post-TDS)", "Value": format_indian_currency(net_payout_injected), "Ratio (% of Cash Influx)": "100.00%"},
        {"Wealth Item": "TDS Subtracted from Company", "Value": format_indian_currency(total_corporate_withheld_tds), "Ratio (% of Cash Influx)": pers_tds_subtracted_pct},
        {"Wealth Item": "Annual Personal Progressive Tax Liability", "Value": format_indian_currency(annual_personal_tax_liability), "Ratio (% of Cash Influx)": pers_tax_liability_pct},
        {"Wealth Item": "Projected Year-End Total Savings (After ALL Taxes)", "Value": format_indian_currency(safely_disposable_annual_surplus), "Ratio (% of Cash Influx)": pers_net_surplus_of_influx_pct}
    ]
    st.table(pd.DataFrame(pers_matrix))

# ==========================================
# STRATEGIC EFFICIENCY SUMMARY PANEL
# ==========================================
st.write("---")
st.subheader("📊 Strategic Wealth Extraction Analytics")

col_eff1, col_eff2 = st.columns(2)
with col_eff1:
    st.info(
        f"💡 **Global Wealth Extraction Efficiency Ratings:**\n\n"
        f"*   **Of Corporate Gross Revenue:** **{overall_extraction_efficiency_pct}** of every rupee your firm generated successfully bypasses all tax filters to become risk-free wealth.\n"
        f"*   **Of Personal Net Influx:** **{pers_net_surplus_of_influx_pct}** of the cash that physically entered your personal accounts is completely protected and cleared for spending."
    )

with col_eff2:
    if corporate_taxable_surplus > 0:
        st.warning(f"⚡ **Tax Leakage Mitigation Warning:**\n\nYour company is leaving **{format_indian_currency(corporate_taxable_surplus)}** exposed to corporate income tax (~25.17%), costing you **{format_indian_currency(modeled_corporate_tax)}** in tax drift. Consider scaling up your deductible Director Remuneration configuration in the sidebar to suppress this corporate taxable base toward zero.")
