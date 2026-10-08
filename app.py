import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config & Custom CSS
st.set_page_config(layout="wide", page_title="Executive Dashboard", page_icon="📊")

# Inject custom CSS to hide Streamlit header/footer/menu and add sleek aesthetic polish
st.markdown("""
<style>
    /* Hide Streamlit default header, footer, and main menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Modern Dark Theme Background and Container Tweaks */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Custom Styling for Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(38, 39, 48, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 240, 255, 0.4);
    }

    /* Custom Expander Styling */
    div[data-testid="stExpander"] {
        background: rgba(38, 39, 48, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
    }

    /* Custom Tab Styling */
    button[data-baseweb="tab"] {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Header and Interactive Expander for Data Cleaning Pipeline
st.title("📊 Data Hunt: Executive Dashboard")
with st.expander("🛠️ View Data Cleaning Pipeline"):
    st.write(
        "1. **Removed exact row duplicates**.\n"
        "2. **Nullified negative `shipping_days`**.\n"
        "3. **Clamped `discount_pct`** strictly between `0.0` and `1.0`.\n"
        "4. **Dropped null values** to ensure accurate mathematical calculations."
    )
st.divider()

# 3. Load and Clean Data
@st.cache_data
def load_data():
    df = pd.read_csv('THE_DATA_HUNT_dataset.csv')
    # Core Cleaning Steps
    df = df.drop_duplicates()
    df['shipping_days'] = df['shipping_days'].apply(lambda x: x if pd.notnull(x) and x >= 0 else None)
    df['discount_pct'] = df['discount_pct'].apply(lambda x: x if pd.notnull(x) and 0 <= x <= 1 else None)
    df = df.dropna()
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# 4. Interactive Sidebar Filters
st.sidebar.header("⚡ Interactive Filters")
cat_filter = st.sidebar.multiselect("Select Category", df['category'].unique(), default=df['category'].unique())
reg_filter = st.sidebar.multiselect("Select Region", df['region'].unique(), default=df['region'].unique())
seg_filter = st.sidebar.multiselect("Select Segment", df['segment'].unique(), default=df['segment'].unique())

# Dynamically filter dataframe based on sidebar inputs
filtered_df = df[
    (df['category'].isin(cat_filter)) & 
    (df['region'].isin(reg_filter)) & 
    (df['segment'].isin(seg_filter))
]

# 5. Advanced KPI Metrics Section
st.subheader("Performance KPIs")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['revenue'].sum() if len(filtered_df) > 0 else 0
total_profit = filtered_df['profit'].sum() if len(filtered_df) > 0 else 0
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders = len(filtered_df)
returns_count = len(filtered_df[filtered_df['order_status'].isin(['Returned', 'Cancelled'])])
return_rate = (returns_count / total_orders * 100) if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_revenue:,.0f}", delta="Primary KPI", delta_color="normal")
col2.metric("Total Profit", f"${total_profit:,.0f}", delta=f"{profit_margin:.1f}% Margin", delta_color="normal" if profit_margin >= 0 else "inverse")
col3.metric("Total Orders", f"{total_orders:,}", delta="Order Volume", delta_color="off")
col4.metric("Return Rate", f"{return_rate:.2f}%", delta="Critical Metric", delta_color="inverse")

st.divider()

# 6. Tabbed & Multi-Column Visualization Layout
st.subheader("Executive Insights")
tab1, tab2 = st.tabs(["📊 Overview & Financial Trends", "📍 Category & City Analysis"])

# Palette Configuration for Plotly Dark Theme
COLOR_PRIMARY = ["#00F0FF", "#FF007F"]
COLOR_ACCENT = ["#00F0FF"]

with tab1:
    row1_col1, row1_col2 = st.columns(2)

    # Chart 1: Grouped Bar Chart comparing Revenue vs Profit by Category
    with row1_col1:
        agg_cat = filtered_df.groupby('category')[['revenue', 'profit']].sum().reset_index()
        fig1 = px.bar(
            agg_cat, 
            x='category', 
            y=['revenue', 'profit'], 
            barmode='group', 
            title="Revenue vs Profit by Category",
            template="plotly_dark",
            color_discrete_sequence=COLOR_PRIMARY
        )
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title_text="Metric",
            xaxis_title="Category",
            yaxis_title="Amount ($)"
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Line chart showing Monthly Revenue and Profit Trend for 2025
    with row1_col2:
        df_trend = filtered_df.copy()
        df_trend['month'] = df_trend['order_date'].dt.strftime('%Y-%m')
        agg_month = df_trend.groupby('month')[['revenue', 'profit']].sum().reset_index()
        fig2 = px.line(
            agg_month, 
            x='month', 
            y=['revenue', 'profit'], 
            title="Monthly Revenue and Profit Trend (2025)",
            template="plotly_dark",
            color_discrete_sequence=COLOR_PRIMARY
        )
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title_text="Metric",
            xaxis_title="Month",
            yaxis_title="Amount ($)"
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    row2_col1, row2_col2 = st.columns(2)

    # Chart 3: Histogram showing the count of Returns/Cancellations by Category
    with row2_col1:
        bad_orders = filtered_df[filtered_df['order_status'].isin(['Returned', 'Cancelled'])]
        fig3 = px.histogram(
            bad_orders, 
            x='category', 
            title="Count of Returns/Cancellations by Category",
            template="plotly_dark",
            color_discrete_sequence=COLOR_ACCENT
        )
        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Category",
            yaxis_title="Count of Failed Orders"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4: Horizontal bar chart showing Top 10 Cities by Revenue
    with row2_col2:
        top_cities = filtered_df.groupby('city')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
        fig4 = px.bar(
            top_cities, 
            x='revenue', 
            y='city', 
            orientation='h', 
            title="Top 10 Cities by Revenue",
            template="plotly_dark",
            color_discrete_sequence=COLOR_ACCENT
        )
        fig4.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Revenue ($)",
            yaxis_title="City"
        )
        st.plotly_chart(fig4, use_container_width=True)