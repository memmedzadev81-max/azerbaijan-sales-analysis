"""
Azərbaycan Satış Analizi Dashboard
Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Azərbaycan Satış Dashboard",
    page_icon="🇦🇿",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sales.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filterlər")

years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("İl", years, default=years)

regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(df["category"].unique())
selected_categories = st.sidebar.multiselect("Kateqoriya", categories, default=categories)

salespeople = sorted(df["salesperson"].unique())
selected_sp = st.sidebar.multiselect("Satış nümayəndəsi", salespeople, default=salespeople)

mask = (
    df["year"].isin(selected_years) &
    df["region"].isin(selected_regions) &
    df["category"].isin(selected_categories) &
    df["salesperson"].isin(selected_sp)
)
f = df[mask].copy()

# Header
st.title("🇦🇿 Azərbaycan Satış Analizi Dashboard")
st.caption("Python → SQL → Streamlit | 500 sifariş | 2024–2025")

if f.empty:
    st.warning("Seçilmiş filterlərə uyğun data yoxdur.")
    st.stop()

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Ümumi Gəlir", f"{f['total_amount'].sum():,.0f} ₼")
c2.metric("Sifariş sayı", f"{len(f):,}")
c3.metric("Unikal müştəri", f"{f['customer_id'].nunique():,}")
c4.metric("Orta sifariş", f"{f['total_amount'].mean():,.0f} ₼")
c5.metric("Satılan ədəd", f"{f['quantity'].sum():,}")

st.divider()

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Aylıq satış trendi")
    monthly = f.groupby("year_month", as_index=False)["total_amount"].sum().sort_values("year_month")
    fig = px.line(monthly, x="year_month", y="total_amount", markers=True,
                  labels={"year_month": "Ay", "total_amount": "Satış (₼)"})
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Region üzrə satış")
    reg = f.groupby("region", as_index=False)["total_amount"].sum().sort_values("total_amount", ascending=False)
    fig = px.bar(reg, x="region", y="total_amount", color="total_amount",
                 color_continuous_scale="Blues",
                 labels={"region": "Region", "total_amount": "Satış (₼)"})
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Kateqoriya üzrə satış")
    cat = f.groupby("category", as_index=False)["total_amount"].sum()
    fig = px.pie(cat, values="total_amount", names="category", hole=0.4)
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Satış nümayəndəsi performansı")
    sp = f.groupby("salesperson", as_index=False).agg(
        sales=("total_amount", "sum"), orders=("order_id", "count")
    ).sort_values("sales", ascending=False)
    fig = px.bar(sp, x="salesperson", y="sales", text="orders",
                 color="salesperson",
                 labels={"salesperson": "Nümayəndə", "sales": "Satış (₼)"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Row 3
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 10 məhsul (gəlirə görə)")
    top = (f.groupby(["category", "product"], as_index=False)
           .agg(revenue=("total_amount", "sum"), qty=("quantity", "sum"))
           .sort_values("revenue", ascending=False).head(10))
    fig = px.bar(top, y="product", x="revenue", orientation="h", color="category",
                 labels={"product": "", "revenue": "Gəlir (₼)"})
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Endirim analizi")
    f["discount_status"] = f["discount"].apply(lambda x: "Endirimli" if x > 0 else "Endirimsiz")
    disc = f.groupby("discount_status", as_index=False).agg(
        orders=("order_id", "count"), sales=("total_amount", "sum")
    )
    fig = px.bar(disc, x="discount_status", y="sales", text="orders",
                 color="discount_status",
                 labels={"discount_status": "", "sales": "Satış (₼)"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Nümunə data")
st.dataframe(
    f[["order_id", "order_date", "region", "category", "product",
       "quantity", "unit_price", "discount", "total_amount", "salesperson"]].head(50),
    use_container_width=True
)

st.caption("Mənbə: sales_data.csv (Azərbaycan regionları) • Python + SQLite + Streamlit + Plotly")
