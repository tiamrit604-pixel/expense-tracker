import streamlit as st
import pandas as pd
from datetime import date

# --------------------
# Load or create files
# --------------------
def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()

expenses = load_data("expenses.csv")
income = load_data("income.csv")

# --------------------
# App title
# --------------------
st.title("💰 Personal Expense Tracker")

# --------------------
# Sidebar menu
# --------------------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Expense",
        "Add Income",
        "Monthly Summary",
        "Delete Expense",
        "Delete Income"
    ]
)

# --------------------
# Add Expense
# --------------------
if menu == "Add Expense":
    st.header("Add Expense")

    exp_date = st.date_input("Date", date.today())
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox(
        "Category",
        ["Sellers Bro","HEB", "SAMS", "Walmart", "Indian Grocery", "Rent", "Internet & Phone", "Others"]
    )
    note = st.text_input("Note (optional)")

    if st.button("Save Expense"):
        new_expense = pd.DataFrame(
            [[exp_date, amount, category, note]],
            columns=["Date", "Amount", "Category", "Note"]
        )
        expenses = pd.concat([expenses, new_expense], ignore_index=True)
        expenses.to_csv("expenses.csv", index=False)
        st.success("Expense saved successfully!")

# --------------------
# Add Income
# --------------------
elif menu == "Add Income":
    st.header("Add Income")

    inc_date = st.date_input("Date", date.today())
    amount = st.number_input("Amount", min_value=0.0)
    source = st.text_input("Source")

    if st.button("Save Income"):
        new_income = pd.DataFrame(
            [[inc_date, amount, source]],
            columns=["Date", "Amount", "Source"]
        )
        income = pd.concat([income, new_income], ignore_index=True)
        income.to_csv("income.csv", index=False)
        st.success("Income saved successfully!")

# --------------------
# Monthly Summary
# --------------------
# --------------------
# Monthly Summary
# --------------------
elif menu == "Monthly Summary":
    st.header("📊 Monthly Summary")

    month = st.selectbox("Select Month", range(1, 13))
    year = st.selectbox("Select Year", [2025, 2026, 2027])

    grocery_categories = [
        "Sellers Bro",
        "HEB",
        "SAMS",
        "Walmart",
        "Indian Grocery"
    ]

    if not expenses.empty:
        expenses["Date"] = pd.to_datetime(expenses["Date"])

        monthly_expenses = expenses[
            (expenses["Date"].dt.month == month) &
            (expenses["Date"].dt.year == year)
        ]

        total_expense = monthly_expenses["Amount"].sum()

        # Grocery total
        grocery_expenses = monthly_expenses[
            monthly_expenses["Category"].isin(grocery_categories)
        ]
        grocery_total = grocery_expenses["Amount"].sum()

        # Category-wise totals
        category_totals = (
            monthly_expenses
            .groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

    else:
        total_expense = 0
        grocery_total = 0
        monthly_expenses = pd.DataFrame()
        category_totals = pd.DataFrame()

    if not income.empty:
        income["Date"] = pd.to_datetime(income["Date"])

        monthly_income = income[
            (income["Date"].dt.month == month) &
            (income["Date"].dt.year == year)
        ]

        total_income = monthly_income["Amount"].sum()
    else:
        total_income = 0

    net_savings = total_income - total_expense

    # --------------------
    # Summary Cards
    # --------------------
    st.subheader("💡 Summary")
    st.write(f"💵 **Total Income:** ${total_income:.2f}")
    st.write(f"💸 **Total Expenses:** ${total_expense:.2f}")
    st.write(f"🛒 **Groceries Total:** ${grocery_total:.2f}")
    st.write(f"💰 **Net Savings:** ${net_savings:.2f}")

    # --------------------
    # Category-wise totals
    # --------------------
    if not category_totals.empty:
        st.subheader("📦 Category-wise Expense Total")
        st.dataframe(category_totals)

    # --------------------
    # Detailed expenses
    # --------------------
    if not monthly_expenses.empty:
        st.subheader("🧾 Detailed Expenses")
        st.dataframe(monthly_expenses)



# --------------------yy
# Delete Expense
# --------------------
elif menu == "Delete Expense":
    st.header("🗑️ Delete Expense")

    if expenses.empty:
        st.info("No expenses available to delete.")
    else:
        expenses["Date"] = pd.to_datetime(expenses["Date"])

        st.subheader("All Expenses (use left index to delete)")
        st.dataframe(expenses)

        index_to_delete = st.number_input(
            "Enter row number (index) to delete",
            min_value=0,
            max_value=len(expenses) - 1,
            step=1
        )

        st.warning("⚠️ This action cannot be undone.")

        if st.button("Delete Expense"):
            expenses = expenses.drop(index_to_delete).reset_index(drop=True)
            expenses.to_csv("expenses.csv", index=False)
            st.success("Expense deleted successfully!")
# --------------------
# Delete Income
# --------------------
elif menu == "Delete Income":
    st.header("🗑️ Delete Income")

    if income.empty:
        st.info("No income records available to delete.")
    else:
        income["Date"] = pd.to_datetime(income["Date"])

        st.subheader("All Income Records (use left index)")
        st.dataframe(income)

        index_to_delete = st.number_input(
            "Enter row number (index) to delete",
            min_value=0,
            max_value=len(income) - 1,
            step=1
        )

        st.warning("⚠️ This action cannot be undone.")

        if st.button("Delete Income"):
            income = income.drop(index_to_delete).reset_index(drop=True)
            income.to_csv("income.csv", index=False)
            st.success("Income record deleted successfully!")


