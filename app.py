import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fleet Expenses Dashboard", layout="wide")

st.title("🚛 Fleet Maintenance & Expenses Dashboard")

# Upload file
file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if file:
    # Read file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.success("File loaded successfully!")

    # Show raw data
    st.subheader("📊 Raw Data")
    st.dataframe(df)

    # Clean column names (optional safety)
    df.columns = [col.strip() for col in df.columns]

    # KPIs
    total_amount = df["Amount"].sum()
    total_net = df["Net Amount"].sum()
    vat = df["VAT 14%"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Amount", f"{total_amount:,.0f}")
    col2.metric("Total Net", f"{total_net:,.0f}")
    col3.metric("Total VAT", f"{vat:,.0f}")

    # Top vehicles spending
    st.subheader("🚗 Top Vehicles by Expense")
    top_vehicles = df.groupby("Vplate Number")["Amount"].sum().sort_values(ascending=False).head(10)
    fig1 = px.bar(top_vehicles, x=top_vehicles.index, y=top_vehicles.values)
    st.plotly_chart(fig1, use_container_width=True)

    # Expenses by Area
    st.subheader("📍 Expenses by Area")
    area = df.groupby("Area")["Amount"].sum().sort_values(ascending=False)
    fig2 = px.pie(values=area.values, names=area.index)
    st.plotly_chart(fig2, use_container_width=True)

    # Expense categories
    st.subheader("🧾 Expense Categories")
    cat = df.groupby("Expense Category费用类型")["Amount"].sum().sort_values(ascending=False)
    fig3 = px.bar(cat, x=cat.index, y=cat.values)
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload a file to start analysis")
