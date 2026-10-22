import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("📊 Interactive Sales Dashboard")
st.write("Analyze sales using filters, KPIs, and interactive charts.")

# Generate sample sales data
@st.cache_data
def create_sales_data():
    rng = np.random.default_rng(42)

    # Generate dates across 2022, 2023, and 2024
    all_dates = pd.date_range(
        start="2022-01-01",
        end="2024-12-31",
        freq="D"
    )

    df = pd.DataFrame({
        "Date": rng.choice(all_dates, size=200, replace=False),
        "Region": rng.choice(
            ["North", "South", "East", "West"], size=200
        ),
        "Product": rng.choice(
            ["A", "B", "C"], size=200
        ),
        "Sales": rng.integers(1000, 10000, size=200)
    })

    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year

    return df.sort_values("Date").reset_index(drop=True)


df = create_sales_data()

# Sidebar filters
st.sidebar.header("Filters")

years = sorted(df["Year"].unique().tolist())
regions = sorted(df["Region"].unique().tolist())
products = sorted(df["Product"].unique().tolist())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    products,
    default=products
)

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(
        df["Date"].min().date(),
        df["Date"].max().date()
    ),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

# Filter data
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered = df[
        (df["Year"].isin(selected_years))
        & (df["Region"].isin(selected_regions))
        & (df["Product"].isin(selected_products))
        & (df["Date"].dt.date >= start_date)
        & (df["Date"].dt.date <= end_date)
    ]
else:
    st.sidebar.warning("Please select both dates.")
    filtered = df.iloc[0:0]

# KPI metrics
st.subheader("Key Performance Indicators")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Sales",
    f"₹{filtered['Sales'].sum():,}"
)

average_sales = (
    f"₹{filtered['Sales'].mean():,.0f}"
    if not filtered.empty else "N/A"
)

c2.metric("Average Sales", average_sales)
c3.metric("Total Records", len(filtered))

# Display filtered data and charts
st.subheader("Filtered Sales Data")
st.dataframe(filtered, use_container_width=True)

if filtered.empty:
    st.warning("No data matches your filters. Change the filter selections.")

else:
    # Sales by Region
    st.subheader("Sales by Region")

    region_sales = (
        filtered.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_sales)

    # Sales by Year
    st.subheader("Sales by Year")

    year_sales = (
        filtered.groupby("Year")["Sales"]
        .sum()
        .sort_index()
    )

    st.line_chart(year_sales)

    # Exercise 1: Pie chart of sales by product
    st.subheader("Sales by Product")

    pie_data = (
        filtered.groupby("Product", as_index=False)["Sales"]
        .sum()
    )

    fig = px.pie(
        pie_data,
        names="Product",
        values="Sales",
        title="Sales Distribution by Product"
    )

    st.plotly_chart(fig, use_container_width=True)

# Exercise 2: Download filtered CSV
st.subheader("Download Filtered Data")

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="filtered_sales.csv",
    mime="text/csv"
)
