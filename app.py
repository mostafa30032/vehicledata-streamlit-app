import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fleet Dashboard", layout="wide")

st.title("🚛 Fleet Maintenance Analysis Dashboard")

uploaded_file = st.file_uploader("Upload File", type=["xlsx", "csv"])

if uploaded_file:

    # =========================
    # قراءة البيانات
    # =========================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # =========================
    # تنظيف الأعمدة
    # =========================
    df.columns = df.columns.str.strip()

    # تحويل القيم الرقمية
    df["Net Amount"] = pd.to_numeric(df["Net Amount"], errors="coerce")

    # حذف القيم الفارغة في الأساسيات
    df = df.dropna(subset=["Net Amount"])

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # =====================================================
    # 🔥 Filters
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:
        area_filter = st.multiselect(
            "Select Area",
            options=df["Area区域"].dropna().unique()
        )

    with col2:
        vehicle_filter = st.multiselect(
            "Select Vehicle Type",
            options=df["Vehicle Type车型"].dropna().unique()
        )

    # تطبيق الفلاتر
    if area_filter:
        df = df[df["Area区域"].isin(area_filter)]

    if vehicle_filter:
        df = df[df["Vehicle Type车型"].isin(vehicle_filter)]

    # =====================================================
    # 1. Area Analysis
    # =====================================================
    st.subheader("📍 Expense by Area")

    area_cost = df.groupby("Area区域")["Net Amount"].sum().sort_values(ascending=False)

    fig1 = px.bar(
        area_cost,
        x=area_cost.index,
        y=area_cost.values,
        labels={"x": "Area", "y": "Net Expense"},
        title="Expense by Area"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # =====================================================
    # 2. Top 20 Vehicles
    # =====================================================
    st.subheader("🚗 Top 20 Vehicles by Expense")

    vehicle_cost = df.groupby("Vehicle Type车型")["Net Amount"].sum().sort_values(ascending=False).head(20)

    fig2 = px.bar(
        vehicle_cost,
        x=vehicle_cost.index,
        y=vehicle_cost.values,
        title="Top 20 Vehicles"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # =====================================================
    # 3. Maintenance Type
    # =====================================================
    st.subheader("🛠 Maintenance Type Analysis")

    type_cost = df.groupby("types of maintenance ")["Net Amount"].sum().sort_values(ascending=False)

    fig3 = px.bar(
        type_cost,
        x=type_cost.index,
        y=type_cost.values,
        title="Maintenance Types"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # =====================================================
    # 4. KPI Total
    # =====================================================
    total = df["Net Amount"].sum()

    st.metric("💰 Total Net Expense", f"{total:,.2f}")
