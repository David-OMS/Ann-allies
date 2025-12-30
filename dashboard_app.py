"""
Interactive FreshDay Yoghurt Dashboard
Streamlit web application for exploring sales and production analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="FreshDay Yoghurt Analysis",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #06A77D;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    sales = pd.read_csv('cleaned_data/daily_sales_cleaned.csv')
    production = pd.read_csv('cleaned_data/production_stock_cleaned.csv')
    sales['date'] = pd.to_datetime(sales['date'])
    production['date'] = pd.to_datetime(production['date'])
    return sales, production

sales, production = load_data()

# Header
st.markdown('<p class="main-header">🥛 FreshDay Yoghurt Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">March–April 2024 | Sales & Production Summary</p>', unsafe_allow_html=True)

# Calculate KPIs
total_revenue = sales['total_sales'].sum()
total_units_sold = sales['quantity_sold'].sum()
total_produced = production['quantity_produced'].sum()
unique_products = sales['product_name'].nunique()
sales_days = sales['date'].nunique()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue", f"₦{total_revenue/1e6:.2f}M", help="Total revenue from recorded sales")

with col2:
    st.metric("Units Sold", f"{total_units_sold:,}", help="Total units sold across all products")

with col3:
    st.metric("Units Produced", f"{total_produced:,}", help="Total units produced")

with col4:
    st.metric("Active Products", f"{unique_products}", help="Number of unique SKUs")

# Main Charts
st.markdown("---")

# Chart 1: Monthly Revenue Trend
st.subheader("📈 Monthly Revenue Trend")
monthly_revenue = sales.groupby(sales['date'].dt.to_period('M'))['total_sales'].sum().reset_index()
monthly_revenue['date'] = monthly_revenue['date'].astype(str)
fig1 = px.line(monthly_revenue, x='date', y='total_sales', 
               markers=True, line_shape='linear',
               labels={'date': 'Month', 'total_sales': 'Revenue (₦)'},
               color_discrete_sequence=['#06A77D'])
fig1.update_traces(line_width=3, marker_size=10)
fig1.update_layout(height=400, showlegend=False,
                  xaxis_title="Month", yaxis_title="Revenue (₦)",
                  yaxis=dict(tickformat=".0f"))
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 & 3: Side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Units Sold by Product")
    product_sales = sales.groupby('product_name')['quantity_sold'].sum().sort_values(ascending=True).tail(10)
    fig2 = px.bar(product_sales, orientation='h', 
                 labels={'value': 'Units Sold', 'index': 'Product'},
                 color_discrete_sequence=['#F18F01'])
    fig2.update_layout(height=400, showlegend=False,
                      xaxis_title="Units Sold", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("🏭 Production vs Sales (Top 8)")
    prod_by_product = production.groupby('product_name')['quantity_produced'].sum()
    sales_by_product = sales.groupby('product_name')['quantity_sold'].sum()
    comparison = pd.DataFrame({
        'Produced': prod_by_product,
        'Sold': sales_by_product
    }).fillna(0).sort_values('Produced', ascending=False).head(8)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name='Produced', x=comparison.index, y=comparison['Produced'],
                         marker_color='#06A77D'))
    fig3.add_trace(go.Bar(name='Recorded Sales', x=comparison.index, y=comparison['Sold'],
                         marker_color='#C73E1D'))
    fig3.update_layout(barmode='group', height=400, 
                      xaxis_title="Product", yaxis_title="Units",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: 250ml vs 500ml Performance
st.subheader("🥤 250ml vs 500ml Performance")
size_comparison = sales.groupby('product_size').agg({
    'quantity_sold': 'sum',
    'total_sales': 'sum'
}).reset_index()

fig4 = make_subplots(specs=[[{"secondary_y": True}]])
fig4.add_trace(
    go.Bar(name='Units Sold', x=size_comparison['product_size'], 
           y=size_comparison['quantity_sold'], marker_color='#F18F01'),
    secondary_y=False,
)
fig4.add_trace(
    go.Bar(name='Revenue', x=size_comparison['product_size'], 
           y=size_comparison['total_sales'], marker_color='#A23B72'),
    secondary_y=True,
)
fig4.update_xaxes(title_text="Size")
fig4.update_yaxes(title_text="Units Sold", secondary_y=False)
fig4.update_yaxes(title_text="Revenue (₦)", secondary_y=True, tickformat=".0f")
fig4.update_layout(height=400, barmode='group',
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig4, use_container_width=True)

# Chart 5 & 6: Side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("🍓 Revenue by Flavor")
    flavor_revenue = sales.groupby('product_flavor')['total_sales'].sum().sort_values(ascending=True)
    fig5 = px.bar(flavor_revenue, orientation='h',
                 labels={'value': 'Revenue (₦)', 'index': 'Flavor'},
                 color_discrete_sequence=['#A23B72'])
    fig5.update_layout(height=400, showlegend=False,
                      xaxis_title="Revenue (₦)", yaxis_title="",
                      xaxis=dict(tickformat=".0f"))
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("💰 Top 5 Products by Revenue")
    top_products = sales.groupby('product_name')['total_sales'].sum().sort_values(ascending=True).tail(5)
    fig6 = px.bar(top_products, orientation='h',
                 labels={'value': 'Revenue (₦)', 'index': 'Product'},
                 color_discrete_sequence=['#06A77D'])
    fig6.update_layout(height=400, showlegend=False,
                      xaxis_title="Revenue (₦)", yaxis_title="",
                      xaxis=dict(tickformat=".0f"))
    st.plotly_chart(fig6, use_container_width=True)

# Data Limitations
st.markdown("---")
st.markdown("### 📋 Data Limitations & Reporting Confidence")
st.info("""
**Figures reflect recorded entries only; manual logging may cause gaps or inconsistencies.**

- Sales data recorded on **42 days** out of ~60 business days (10 days missing from logs)
- Production records are irregular (18 production days over 2 months)
- No expiry, batch, or waste tracking data available
- Some sales may be unlogged (manual entry system)
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7F8C8D; font-size: 0.9rem;'>
    FreshDay Yoghurt Analysis | March–April 2024
</div>
""", unsafe_allow_html=True)

