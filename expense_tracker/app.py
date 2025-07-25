import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import categorize_expenses, show_budget_alert, export_to_excel

st.title("💸 Expense Tracker with Visuals")
uploaded_file = st.file_uploader("Upload your expense CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    df = categorize_expenses(df)

    st.subheader("📊 Expense Overview")
    category_summary = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_summary)

    fig, ax = plt.subplots()
    category_summary.plot.pie(ax=ax, autopct="%1.1f%%")
    st.pyplot(fig)

    st.subheader("🚨 Budget Alerts")
    show_budget_alert(category_summary)

    st.subheader("📥 Export Report")
    excel = export_to_excel(df)
    st.download_button("Download Excel Report", excel, "report.xlsx")

else:
    st.info("Upload a CSV to get started.")
