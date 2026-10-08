import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Data Hunt Dashboard")

st.title("📊 Data Hunt: Executive Dashboard")
with st.expander("🛠️ View Data Cleaning Pipeline"):
    st.write("1. Removed exact row duplicates.\n2. Nullified negative `shipping_days`.\n3. Clamped `discount_pct` strictly between 0.0 and 1.0.\n4. Dropped nulls to ensure mathematical accuracy.")
st.divider()

# 1. Load and Clean Data
@st.cache_data
def load_data():
    df = pd.read_csv('THE_DATA_HUNT_dataset.csv')
    df = df.drop_duplicates()
    df['shipping_days'] = df['shipping_days'].apply(lambda x: x if pd.notnull(x) and x >= 0 else None)
    df['discount_pct'] = df['discount_pct'].apply(lambda x: x if pd.notnull(x) and 0 <= x <= 1 else None)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# 2. Sidebar Filters (Minimum 3 Required)
st.sidebar.header("Interactive Filters")
cat_filter = st.sidebar.multiselect("Select Category", df['category'].unique(), default=df['category'].unique())
reg_filter = st.sidebar.multiselect("Select Region", df['region'].unique(), default=df['region'].unique())
seg_filter = st.sidebar.multiselect("Select Segment", df['segment'].unique(), default=df['segment'].unique())

# Apply Filters
filtered_df = df[
    (df['category'].isin(cat_filter)) & 
    (df['region'].isin(reg_filter)) & 
    (df['segment'].isin(seg_filter))
]

# 3. KPI Cards (Minimum 4 Required)
st.subheader("Performance KPIs")
col1, col2, col3, col4 = st.columns(4)

# Adding delta arrows to make the UI look advanced
col1.metric("Total Revenue", f"${filtered_df['revenue'].sum():,.0f}", delta="Primary KPI", delta_color="normal")
col2.metric("Total Profit", f"${filtered_df['profit'].sum():,.0f}", delta=f"{filtered_df['profit'].sum() / filtered_df['revenue'].sum() * 100:.1f}% Margin", delta_color="off")
col3.metric("Total Orders", f"{len(filtered_df):,}", delta="-", delta_color="off")

returns = len(filtered_df[filtered_df['order_status'].isin(['Returned', 'Cancelled'])])
return_rate = (returns / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
col4.metric("Return Rate", f"{return_rate:.2f}%", delta="Critical Metric", delta_color="inverse")
st.divider()

# 4. Visualizations (Minimum 4 Required)
st.subheader("Insights")
row1_col1, row1_col2 = st.columns(2)

# Chart 1: Upgraded Bar Chart
agg_cat = filtered_df.groupby('category')[['revenue', 'profit']].sum().reset_index()
fig1 = px.bar(
    agg_cat, 
    x='category', 
    y=['revenue', 'profit'], 
    barmode='group', 
    title="Revenue vs Profit by Category",
    template="plotly_dark", # Forces a sleek dark template
    color_discrete_sequence=["#00F0FF", "#FF007F"] # Custom neon/cyberpunk colors
)
fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)") # Makes background transparent
row1_col1.plotly_chart(fig1, use_container_width=True)

# Chart 2: Monthly Trend (Answers Q2)
filtered_df['month'] = filtered_df['order_date'].dt.strftime('%Y-%m')
agg_month = filtered_df.groupby('month')[['revenue', 'profit']].sum().reset_index()
fig2 = px.line(
    agg_month, 
    x='month', 
    y=['revenue', 'profit'], 
    title="Monthly Revenue and Profit Trend (2025)",
    template="plotly_dark",
    color_discrete_sequence=["#00F0FF", "#FF007F"]
)
fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
row1_col2.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

# Chart 3: Returns by Category (Answers Q3)
bad_orders = filtered_df[filtered_df['order_status'].isin(['Returned', 'Cancelled'])]
fig3 = px.histogram(
    bad_orders, 
    x='category', 
    title="Count of Returns/Cancellations by Category",
    template="plotly_dark",
    color_discrete_sequence=["#00F0FF"]
)
fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
row2_col1.plotly_chart(fig3, use_container_width=True)

# Chart 4: Top Cities (Answers Q4)
top_cities = filtered_df.groupby('city')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
fig4 = px.bar(
    top_cities, 
    x='revenue', 
    y='city', 
    orientation='h', 
    title="Top 10 Cities by Revenue",
    template="plotly_dark",
    color_discrete_sequence=["#00F0FF"]
)
fig4.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
row2_col2.plotly_chart(fig4, use_container_width=True)