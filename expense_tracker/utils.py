import pandas as pd
import io

BUDGET_LIMITS = {
    "Food": 3000,
    "Transport": 2000,
    "Entertainment": 1500,
}

def categorize_expenses(df):
    if "Category" not in df.columns:
        df["Category"] = df["Description"].apply(auto_categorize)
    return df

def auto_categorize(desc):
    desc = str(desc).lower()
    if "food" in desc or "grocer" in desc:
        return "Food"
    elif "fuel" in desc or "uber" in desc:
        return "Transport"
    elif "movie" in desc or "netflix" in desc:
        return "Entertainment"
    else:
        return "Other"

def show_budget_alert(category_summary):
    import streamlit as st
    for cat, total in category_summary.items():
        limit = BUDGET_LIMITS.get(cat)
        if limit and total > limit:
            st.error(f"⚠️ You have exceeded the budget for {cat} (Spent: ₹{total}, Limit: ₹{limit})")
        else:
            st.success(f"{cat}: ₹{total} / ₹{limit if limit else 'N/A'}")

def export_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses")
    output.seek(0)
    return output
