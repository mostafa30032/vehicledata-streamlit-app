import streamlit as st
import pandas as pd

st.title("Fleet Maintenance Analysis Dashboard")

uploaded_file = st.file_uploader("Upload Maintenance File", type=["xlsx", "csv"])

if uploaded_file:

    # قراءة الملف
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    # تنظيف الأعمدة المهمة
    df["Net Amount"] = pd.to_numeric(df["Net Amount"], errors="coerce")

    # =========================
    # 1. إجمالي الصرف حسب المنطقة
    # =========================
    st.subheader("Total Expense by Area")

    area_cost = df.groupby("Area区域")["Net Amount"].sum().sort_values(ascending=False)
    st.dataframe(area_cost)

    st.bar_chart(area_cost)

    # =========================
    # 2. إجمالي لكل مركبة
    # =========================
    st.subheader("Total Expense per Vehicle")

    vehicle_cost = df.groupby("Vplate Number车牌号")["Net Amount"].sum().sort_values(ascending=False)
    st.dataframe(vehicle_cost)

    # =========================
    # 3. أعلى 10 سيارات
    # =========================
    st.subheader("Top 10 Vehicles by Expense")

    top10 = vehicle_cost.head(10)
    st.dataframe(top10)
    st.bar_chart(top10)

    # =========================
    # 4. حسب نوع الصيانة
    # =========================
    st.subheader("Maintenance Type Analysis")

    type_cost = df.groupby("types of maintenance ")["Net Amount"].sum().sort_values(ascending=False)
    st.dataframe(type_cost)
    st.bar_chart(type_cost)

    # =========================
    # 5. إجمالي الصرف
    # =========================
    total = df["Net Amount"].sum()

    st.metric("Total Net Expense", f"{total:,.2f}")
