"""
Interactive FreshDay Yoghurt Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="FreshDay Yoghurt Analysis", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { 
        background-color: #FFFFFF; 
        background-image: linear-gradient(to bottom, #FAFBFC 0%, #FFFFFF 100%);
    }
    .main .block-container { 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
        max-width: 100%; 
    }
    h1, h2, h3 { 
        color: #2C3E50; 
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    .stSubheader {
        font-weight: 700 !important;
        color: #2C3E50 !important;
        margin-bottom: 1rem !important;
        font-size: 1.3rem !important;
        visibility: visible !important;
        display: block !important;
    }
    h3 {
        color: #2C3E50 !important;
        font-weight: 700 !important;
        visibility: visible !important;
        display: block !important;
    }
    /* Remove Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    /* Chart containers */
    .element-container {
        border-radius: 8px;
        padding: 0.5rem;
        background-color: #FFFFFF;
    }
    /* Ensure all text is visible */
    .js-plotly-plot .xtitle, .js-plotly-plot .ytitle {
        fill: #34495E !important;
        font-weight: 600 !important;
    }
    .js-plotly-plot text {
        fill: #34495E !important;
        font-weight: bold !important;
    }
    .js-plotly-plot .ytick text, .js-plotly-plot .xtick text {
        fill: #34495E !important;
        font-weight: bold !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
</style>
""", unsafe_allow_html=True)

# Colors
kpi_colors = ['#2E86AB', '#06A77D', '#F18F01', '#A23B72']
product_colors = {
    'Plain': '#2E86AB',
    'Strawberry': '#C73E1D',
    'Banana': '#F18F01',
    'Coconut': '#06A77D',
    'Pineapple': '#A23B72'
}

@st.cache_data
def load_data():
    sales = pd.read_csv('cleaned_data/daily_sales_cleaned.csv')
    production = pd.read_csv('cleaned_data/production_stock_cleaned.csv')
    sales['date'] = pd.to_datetime(sales['date'])
    production['date'] = pd.to_datetime(production['date'])
    return sales, production

sales, production = load_data()

# KPIs
total_revenue = sales['total_sales'].sum()
total_units_sold = int(sales['quantity_sold'].sum())
total_produced = int(production['quantity_produced'].sum())
unique_products = sales['product_name'].nunique()

# Header - enhanced
st.markdown('<h1 style="text-align: center; font-size: 2rem; font-weight: 700; color: #2C3E50; margin-bottom: 0.5rem; letter-spacing: -0.5px;">FreshDay Yoghurt Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 0.95rem; color: #7F8C8D; font-style: italic; margin-bottom: 2rem; font-weight: 400;">March–April 2024 | Sales & production summary</p>', unsafe_allow_html=True)

# KPI Cards - enhanced with shadows and gradients
kpi_html = f"""
<div style="display: flex; gap: 1.5rem; margin-bottom: 2.5rem; justify-content: center; padding: 0 1rem;">
    <div style="flex: 0 0 22%; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); border: 2px solid #2E86AB; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 8px rgba(46, 134, 171, 0.15);">
        <div style="font-size: 0.8rem; font-weight: 600; color: #2C3E50; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.5px;">Total Revenue</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #2E86AB; line-height: 1.2;">₦{total_revenue/1e6:.2f}M</div>
    </div>
    <div style="flex: 0 0 22%; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); border: 2px solid #06A77D; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 8px rgba(6, 167, 125, 0.15);">
        <div style="font-size: 0.8rem; font-weight: 600; color: #2C3E50; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.5px;">Total Units Sold</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #06A77D; line-height: 1.2;">{total_units_sold:,}</div>
    </div>
    <div style="flex: 0 0 22%; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); border: 2px solid #F18F01; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 8px rgba(241, 143, 1, 0.15);">
        <div style="font-size: 0.8rem; font-weight: 600; color: #2C3E50; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.5px;">Total Units Produced</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #F18F01; line-height: 1.2;">{total_produced:,}</div>
    </div>
    <div style="flex: 0 0 22%; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); border: 2px solid #A23B72; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 8px rgba(162, 59, 114, 0.15);">
        <div style="font-size: 0.8rem; font-weight: 600; color: #2C3E50; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.5px;">Active Products</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #A23B72; line-height: 1.2;">{unique_products}</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ROW 1: 2 charts side by side
col1, col2 = st.columns(2)

with col1:
    # Get monthly revenue data
    monthly_data = sales.groupby(sales['date'].dt.to_period('M'))['total_sales'].sum()
    monthly_data.index = monthly_data.index.to_timestamp()
    monthly_df = pd.DataFrame({'date': monthly_data.index, 'revenue': monthly_data.values})
    monthly_df['date_str'] = monthly_df['date'].dt.strftime('%b %Y')
    
    # Calculate y-axis range to show variation
    max_rev = float(monthly_df['revenue'].max())
    min_rev = float(monthly_df['revenue'].min())
    diff = max_rev - min_rev
    padding = diff * 0.15 if diff > 0 else max_rev * 0.1
    y_min = max(0, min_rev - padding)
    y_max = max_rev + padding
    
    # Create figure
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=monthly_df['date_str'],
        y=monthly_df['revenue'],
        mode='lines+markers',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=12, color='white', line=dict(width=2.5, color='#2E86AB')),
        hovertemplate='<b>%{x}</b><br>Revenue: ₦%{y:,.0f}<extra></extra>',
        hoverlabel=dict(bgcolor='white', bordercolor='#2E86AB', font_size=12, font_color='#2C3E50')
    ))
    
    # Update layout
    fig1.update_layout(
        title=dict(
            text="Monthly Revenue Trend",
            font=dict(size=16, color='#2C3E50', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        height=400,
        showlegend=False,
        plot_bgcolor='#FAFAFA',
        paper_bgcolor='#FFFFFF',
        hovermode='closest',
        hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=11, font_color='#2C3E50'),
        margin=dict(l=60, r=20, t=80, b=60),
        font=dict(size=11, color='#34495E', family='Arial, sans-serif')
    )
    
    # Use simple automatic formatting with range
    fig1.update_yaxes(
        title="Revenue (₦)",
        title_font=dict(color='#34495E', size=12, family='Arial, sans-serif'),
        tickfont=dict(color='#34495E', size=11, family='Arial, sans-serif'),
        gridcolor='rgba(0,0,0,0.3)',
        gridwidth=0.8,
        griddash='dash',
        showticklabels=True,
        showgrid=True,
        showline=True,
        linecolor='#34495E',
        linewidth=2,
        mirror=True,
        range=[y_min, y_max],
        tickformat=',.0f',
        tickprefix='₦',
        dtick=(y_max - y_min) / 4
    )
    
    fig1.update_xaxes(
        title="Month",
        title_font=dict(color='#34495E', size=12, family='Arial, sans-serif'),
        tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif'),
        showticklabels=True,
        showline=True,
        linecolor='#34495E',
        linewidth=2,
        mirror=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    units_by_product = sales.groupby('product_name')['quantity_sold'].sum().sort_values(ascending=True)
    product_names = [f"{name.split()[0]} {'500' if '500ml' in name else '250'}" for name in units_by_product.index]
    colors_list = [product_colors.get(name.split()[0], '#95A5A6') for name in units_by_product.index]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=units_by_product.values, y=product_names, orientation='h',
        marker=dict(color=colors_list, line=dict(color='white', width=1.5)), opacity=0.85,
        hovertemplate='<b>%{y}</b><br>Units: %{x:,}<extra></extra>',
        hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=12, font_color='#2C3E50')
    ))
    fig2.update_layout(
        title=dict(text="Total Units Sold per Product", font=dict(size=16, color='#2C3E50', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        height=400, showlegend=False,
        plot_bgcolor='#FAFAFA', paper_bgcolor='#FFFFFF',
        hovermode='closest',
        hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=11, font_color='#2C3E50'),
        xaxis=dict(
            title="Units Sold",
            title_font=dict(color='#34495E', size=12, family='Arial, sans-serif', weight='bold'),
            gridcolor='rgba(0,0,0,0.3)', gridwidth=0.8, griddash='dash',
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold')
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold')
        ),
        margin=dict(l=0, r=20, t=70, b=50),
        font=dict(size=10, color='#34495E', family='Arial, sans-serif', weight='bold')
    )
    st.plotly_chart(fig2, use_container_width=True)

# ROW 2: 2 charts side by side
col1, col2 = st.columns(2)

with col1:
    prod_by_product = production.groupby('product_name')['quantity_produced'].sum()
    sales_by_product = sales.groupby('product_name')['quantity_sold'].sum()
    comparison = pd.DataFrame({'Produced': prod_by_product, 'Sold': sales_by_product}).fillna(0).sort_values('Sold', ascending=False).head(8)
    short_names = [f"{name.split()[0]}<br>{'500' if '500ml' in name else '250'}" for name in comparison.index]
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name='Produced', x=short_names, y=comparison['Produced'], marker=dict(color='#06A77D', line=dict(color='white', width=1.5)), opacity=0.85,
                         hovertemplate='<b>%{x}</b><br>Produced: %{y:,}<extra></extra>',
                         hoverlabel=dict(bgcolor='white', bordercolor='#06A77D', font_size=12, font_color='#2C3E50')))
    fig3.add_trace(go.Bar(name='Recorded Sales', x=short_names, y=comparison['Sold'], marker=dict(color='#C73E1D', line=dict(color='white', width=1.5)), opacity=0.85,
                          hovertemplate='<b>%{x}</b><br>Recorded Sales: %{y:,}<extra></extra>',
                          hoverlabel=dict(bgcolor='white', bordercolor='#C73E1D', font_size=12, font_color='#2C3E50')))
    fig3.update_layout(
        title=dict(text="Production vs Recorded Sales", font=dict(size=16, color='#2C3E50', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        barmode='group', height=400,
        plot_bgcolor='#FAFAFA', paper_bgcolor='#FFFFFF',
        hovermode='closest',
        hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=11, font_color='#2C3E50'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor='rgba(255,255,255,0.95)', font=dict(size=11, color='#2C3E50', family='Arial, sans-serif', weight='bold')),
        yaxis=dict(
            title="Units",
            title_font=dict(color='#34495E', size=12, family='Arial, sans-serif', weight='bold'),
            gridcolor='rgba(0,0,0,0.3)', gridwidth=0.8, griddash='dash',
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold')
        ),
        xaxis=dict(
            title="",
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold')
        ),
        margin=dict(l=60, r=20, t=80, b=60),
        font=dict(size=10, color='#34495E', family='Arial, sans-serif', weight='bold')
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    top_5_products = sales.groupby('product_name')['total_sales'].sum().sort_values(ascending=False).head(5)
    product_names = [f"{name.split()[0]} {'500' if '500ml' in name else '250'}" for name in top_5_products.index]
    colors_list = [product_colors.get(name.split()[0], '#95A5A6') for name in top_5_products.index]
    
    max_rev_top5 = top_5_products.max()
    rev_ticks_top5 = []
    rev_labels_top5 = []
    step_top5 = max(100000, max_rev_top5 / 4)
    for i in range(5):
        val = i * step_top5
        if val <= max_rev_top5 * 1.2:
            rev_ticks_top5.append(val)
            if val >= 1e6:
                rev_labels_top5.append(f'{val/1e6:.1f}M')
            else:
                rev_labels_top5.append(f'{val/1e3:.0f}K')
    
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(x=top_5_products.values, y=product_names, orientation='h',
                         marker=dict(color=colors_list, line=dict(color='white', width=1.5)), opacity=0.85,
                         hovertemplate='<b>%{y}</b><br>Revenue: ₦%{x:,.0f}<extra></extra>',
                         hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=12, font_color='#2C3E50')))
    fig6.update_layout(
        title=dict(text="Top 5 Products by Revenue", font=dict(size=16, color='#2C3E50', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        height=400, showlegend=False,
        plot_bgcolor='#FAFAFA', paper_bgcolor='#FFFFFF',
        hovermode='closest',
        hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=11, font_color='#2C3E50'),
        xaxis=dict(
            title="Revenue (₦)",
            title_font=dict(color='#34495E', size=12, family='Arial, sans-serif', weight='bold'),
            gridcolor='rgba(0,0,0,0.3)', gridwidth=0.8, griddash='dash',
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold'),
            tickvals=rev_ticks_top5,
            ticktext=rev_labels_top5
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold')
        ),
        margin=dict(l=0, r=20, t=70, b=50),
        font=dict(size=10, color='#34495E', family='Arial, sans-serif', weight='bold')
    )
    st.plotly_chart(fig6, use_container_width=True)

# ROW 3: 2 charts side by side
col1, col2 = st.columns(2)

with col1:
    size_comparison = sales.groupby('product_size').agg({'quantity_sold': 'sum', 'total_sales': 'sum'}).reset_index()
    
    # Create 4 separate bars: 2 for 250ml (units + revenue), 2 for 500ml (units + revenue)
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Position bars side by side for each size
    x_positions = []
    x_labels = []
    for size in size_comparison['product_size']:
        x_positions.extend([f'{size}_units', f'{size}_revenue'])
        x_labels.extend([f'{size}<br>Units', f'{size}<br>Revenue'])
    
    # 250ml bars
    size_250 = size_comparison[size_comparison['product_size'] == '250ml'].iloc[0]
    fig4.add_trace(go.Bar(name='250ml Units', x=['250ml_units'], y=[size_250['quantity_sold']],
                          marker=dict(color='#F18F01', line=dict(color='white', width=1.5)), opacity=0.85,
                          hovertemplate='<b>250ml Units</b><br>Units: %{y:,}<extra></extra>',
                          hoverlabel=dict(bgcolor='white', bordercolor='#F18F01', font_size=12, font_color='#2C3E50')), secondary_y=False)
    fig4.add_trace(go.Bar(name='250ml Revenue', x=['250ml_revenue'], y=[size_250['total_sales']],
                          marker=dict(color='#A23B72', line=dict(color='white', width=1.5)), opacity=0.85,
                          hovertemplate='<b>250ml Revenue</b><br>Revenue: ₦%{y:,.0f}<extra></extra>',
                          hoverlabel=dict(bgcolor='white', bordercolor='#A23B72', font_size=12, font_color='#2C3E50')), secondary_y=True)
    
    # 500ml bars
    size_500 = size_comparison[size_comparison['product_size'] == '500ml'].iloc[0]
    fig4.add_trace(go.Bar(name='500ml Units', x=['500ml_units'], y=[size_500['quantity_sold']],
                          marker=dict(color='#F18F01', line=dict(color='white', width=1.5)), opacity=0.85,
                          hovertemplate='<b>500ml Units</b><br>Units: %{y:,}<extra></extra>',
                          hoverlabel=dict(bgcolor='white', bordercolor='#F18F01', font_size=12, font_color='#2C3E50')), secondary_y=False)
    fig4.add_trace(go.Bar(name='500ml Revenue', x=['500ml_revenue'], y=[size_500['total_sales']],
                          marker=dict(color='#A23B72', line=dict(color='white', width=1.5)), opacity=0.85,
                          hovertemplate='<b>500ml Revenue</b><br>Revenue: ₦%{y:,.0f}<extra></extra>',
                          hoverlabel=dict(bgcolor='white', bordercolor='#A23B72', font_size=12, font_color='#2C3E50')), secondary_y=True)
    
    fig4.update_xaxes(
        title_text="",
        tickmode='array',
        tickvals=['250ml_units', '250ml_revenue', '500ml_units', '500ml_revenue'],
        ticktext=['250ml<br>Units', '250ml<br>Revenue', '500ml<br>Units', '500ml<br>Revenue'],
        tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold'),
        fixedrange=True
    )
    fig4.update_yaxes(
        title_text="Units Sold", secondary_y=False,
        tickcolor='#F18F01',
        gridcolor='rgba(0,0,0,0.3)', gridwidth=0.8, griddash='dash',
        title_font=dict(color='#F18F01', size=12, family='Arial, sans-serif', weight='bold'),
        tickfont=dict(color='#F18F01', size=10, family='Arial, sans-serif', weight='bold')
    )
    
    # Calculate revenue tick values with auto K/M formatting
    max_revenue = float(size_comparison['total_sales'].max())
    min_revenue = float(size_comparison['total_sales'].min())
    
    # Ensure range starts from 0 and goes up (not inverted)
    revenue_min = 0
    revenue_max = max_revenue * 1.15
    
    # Create evenly spaced ticks from 0 to max
    num_ticks = 5
    tick_step = revenue_max / (num_ticks - 1)
    revenue_ticks = [i * tick_step for i in range(num_ticks)]
    revenue_labels = []
    for val in revenue_ticks:
        val_int = int(round(val))
        if val_int >= 1000000:
            revenue_labels.append(f'{val_int/1000000:.1f}M')
        elif val_int >= 1000:
            revenue_labels.append(f'{val_int/1000:.0f}K')
        else:
            revenue_labels.append(f'{val_int:,}')
    
    fig4.update_yaxes(
        title_text="Revenue (₦)", secondary_y=True,
        tickcolor='#A23B72',
        title_font=dict(color='#A23B72', size=12, family='Arial, sans-serif', weight='bold'),
        tickfont=dict(color='#A23B72', size=10, family='Arial, sans-serif', weight='bold'),
        tickmode='array',
        tickvals=revenue_ticks,
        ticktext=revenue_labels,
        range=[revenue_min, revenue_max],
        showticklabels=True,
        side='right',
        autorange=False,
        fixedrange=True,
        scaleanchor=None,
        scaleratio=None,
        showline=False,
        showgrid=False,
        ticks='',
        ticklen=0,
        tickwidth=0
    )
    fig4.update_layout(
        title=dict(text="250ml vs 500ml Performance", font=dict(size=16, color='#2C3E50', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        height=400, barmode='group', plot_bgcolor='#FAFAFA', paper_bgcolor='#FFFFFF',
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5,
            bgcolor='rgba(255,255,255,0.95)',
            font=dict(size=11, color='#2C3E50', family='Arial, sans-serif', weight='bold')
        ),
        margin=dict(l=60, r=60, t=80, b=90),
        font=dict(size=11, color='#34495E', family='Arial, sans-serif'),
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'zoom2d', 'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d']})

with col2:
    flavor_revenue = sales.groupby('product_flavor')['total_sales'].sum().sort_values(ascending=False)
    colors = [product_colors.get(flavor, '#95A5A6') for flavor in flavor_revenue.index]
    
    max_rev_flavor = flavor_revenue.max()
    rev_ticks_flavor = []
    rev_labels_flavor = []
    step_flavor = max(200000, max_rev_flavor / 4)
    for i in range(5):
        val = i * step_flavor
        if val <= max_rev_flavor * 1.2:
            rev_ticks_flavor.append(val)
            if val >= 1e6:
                rev_labels_flavor.append(f'{val/1e6:.1f}M')
            else:
                rev_labels_flavor.append(f'{val/1e3:.0f}K')
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=flavor_revenue.index, y=flavor_revenue.values,
                         marker=dict(color=colors, line=dict(color='white', width=1.5)), opacity=0.85,
                         hovertemplate='<b>%{x}</b><br>Revenue: ₦%{y:,.0f}<extra></extra>',
                         hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=12, font_color='#2C3E50')))
    fig5.update_layout(
        title=dict(text="Revenue by Flavor", font=dict(size=16, color='#2C3E50', family='Arial, sans-serif', weight='bold'), x=0.5, xanchor='center'),
        height=400, showlegend=False,
        plot_bgcolor='#FAFAFA', paper_bgcolor='#FFFFFF',
        hovermode='closest',
        hoverlabel=dict(bgcolor='white', bordercolor='#34495E', font_size=11, font_color='#2C3E50'),
        yaxis=dict(
            title="Revenue (₦)",
            title_font=dict(color='#34495E', size=12, family='Arial, sans-serif', weight='bold'),
            gridcolor='rgba(0,0,0,0.3)', gridwidth=0.8, griddash='dash',
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold'),
            tickvals=rev_ticks_flavor,
            ticktext=rev_labels_flavor
        ),
        xaxis=dict(
            title="",
            tickfont=dict(color='#34495E', size=10, family='Arial, sans-serif', weight='bold')
        ),
        margin=dict(l=60, r=20, t=80, b=90),
        font=dict(size=10, color='#34495E', family='Arial, sans-serif', weight='bold')
    )
    st.plotly_chart(fig5, use_container_width=True)

# Footer - enhanced
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #95A5A6; font-size: 0.75rem; font-style: italic; padding: 1.5rem 0 0.5rem 0; line-height: 1.6;'>
    Figures reflect recorded entries only; manual logging may cause gaps or inconsistencies.
</div>
""", unsafe_allow_html=True)
