import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Dubai Mall Analytics Dashboard",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - DUBAI LUXURY THEME
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --gold-primary: #D4AF37;
        --gold-light: #F4E4BC;
        --gold-dark: #B8960C;
        --navy-dark: #0A1628;
        --navy-medium: #1A2742;
        --navy-light: #2D3E5F;
        --white: #FFFFFF;
        --off-white: #F8F9FA;
        --gray-light: #E9ECEF;
        --success: #28A745;
        --danger: #DC3545;
        --warning: #FFC107;
    }
    
    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #0A1628 0%, #1A2742 50%, #0A1628 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(26, 39, 66, 0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #D4AF37 0%, #F4E4BC 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        color: #B8C5D9;
        font-size: 1.1rem;
        margin-top: 10px;
        letter-spacing: 1px;
    }
    
    /* KPI Cards */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, #1A2742 0%, #2D3E5F 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 25px;
        flex: 1;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.5);
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.15);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #D4AF37 0%, #B8960C 100%);
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #8B9DC3;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
    
    .kpi-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 8px 0;
    }
    
    .kpi-delta {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .kpi-delta.positive {
        color: #28A745;
    }
    
    .kpi-delta.negative {
        color: #DC3545;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #D4AF37;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(212, 175, 55, 0.3);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Chart Containers */
    .chart-container {
        background: linear-gradient(145deg, #1A2742 0%, #0A1628 100%);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .chart-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1628 0%, #1A2742 100%);
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #B8C5D9;
    }
    
    .sidebar-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #D4AF37;
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        margin-bottom: 20px;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background-color: #1A2742;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
        color: #FFFFFF;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #D4AF37;
    }
    
    /* Multiselect Styling */
    .stMultiSelect > div > div {
        background-color: #1A2742;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
    }
    
    /* Date Input Styling */
    .stDateInput > div > div {
        background-color: #1A2742;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background-color: #D4AF37;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        color: #8B9DC3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1A2742;
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #8B9DC3;
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #D4AF37 0%, #B8960C 100%);
        color: #0A1628;
    }
    
    /* Data Table Styling */
    .dataframe {
        font-family: 'Inter', sans-serif;
        border: none !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #D4AF37 0%, #B8960C 100%) !important;
        color: #0A1628 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
    }
    
    .dataframe td {
        background-color: #1A2742 !important;
        color: #FFFFFF !important;
        border-color: rgba(212, 175, 55, 0.1) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #D4AF37;
        background-color: #1A2742;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 8px;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(26, 39, 66, 0.8) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .info-box h4 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37;
        margin-bottom: 10px;
    }
    
    .info-box p {
        font-family: 'Inter', sans-serif;
        color: #B8C5D9;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A1628;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #D4AF37 0%, #B8960C 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #F4E4BC;
    }
    
    /* Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    /* Tooltip Styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #D4AF37;
        color: #0A1628;
        text-align: center;
        padding: 8px 12px;
        border-radius: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Footer Styling */
    .custom-footer {
        background: linear-gradient(135deg, #1A2742 0%, #0A1628 100%);
        border-top: 1px solid rgba(212, 175, 55, 0.3);
        padding: 30px;
        margin-top: 50px;
        border-radius: 16px 16px 0 0;
        text-align: center;
    }
    
    .custom-footer p {
        font-family: 'Inter', sans-serif;
        color: #8B9DC3;
        margin: 5px 0;
    }
    
    .custom-footer .gold-text {
        color: #D4AF37;
        font-weight: 600;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-color: #D4AF37 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #D4AF37 0%, #F4E4BC 50%, #D4AF37 100%);
    }
    
    /* Badge Styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-gold {
        background: linear-gradient(135deg, #D4AF37 0%, #B8960C 100%);
        color: #0A1628;
    }
    
    .badge-success {
        background: rgba(40, 167, 69, 0.2);
        color: #28A745;
        border: 1px solid #28A745;
    }
    
    .badge-danger {
        background: rgba(220, 53, 69, 0.2);
        color: #DC3545;
        border: 1px solid #DC3545;
    }
    
    /* Glassmorphism Effect */
    .glass-card {
        background: rgba(26, 39, 66, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 25px;
    }
    
    /* Pulse Animation for Live Data */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.4);
        }
        70% {
            box-shadow: 0 0 0 15px rgba(212, 175, 55, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(212, 175, 55, 0);
        }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .kpi-value {
            font-size: 1.6rem;
        }
        
        .section-header {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING AND PREPROCESSING
# ============================================
@st.cache_data
def load_data():
    """Load and preprocess the Dubai Mall dataset"""
    df = pd.read_csv('dubai_mall_simple.csv')
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract additional time features
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_month'] = df['date'].dt.day
    df['quarter'] = df['date'].dt.quarter
    
    # Create floor labels
    floor_mapping = {'LG': 'Lower Ground', 'G': 'Ground', '1': 'Level 1', '2': 'Level 2', '3': 'Level 3'}
    df['floor_label'] = df['floor'].map(floor_mapping)
    
    return df

# ============================================
# HELPER FUNCTIONS
# ============================================
def format_currency(value):
    """Format number as AED currency"""
    if value >= 1_000_000:
        return f"AED {value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"AED {value/1_000:.1f}K"
    else:
        return f"AED {value:.0f}"

def format_number(value):
    """Format large numbers"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"

def calculate_delta(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def create_kpi_card(icon, label, value, delta=None, delta_label="vs prev period"):
    """Create a styled KPI card"""
    delta_html = ""
    if delta is not None:
        delta_class = "positive" if delta >= 0 else "negative"
        delta_symbol = "↑" if delta >= 0 else "↓"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_symbol} {abs(delta):.1f}% {delta_label}</div>'
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

# ============================================
# CHART THEME
# ============================================
chart_theme = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'family': 'Inter, sans-serif', 'color': '#B8C5D9'},
    'title': {'font': {'family': 'Playfair Display, serif', 'color': '#D4AF37', 'size': 18}},
    'xaxis': {
        'gridcolor': 'rgba(212, 175, 55, 0.1)',
        'linecolor': 'rgba(212, 175, 55, 0.3)',
        'tickfont': {'color': '#8B9DC3'}
    },
    'yaxis': {
        'gridcolor': 'rgba(212, 175, 55, 0.1)',
        'linecolor': 'rgba(212, 175, 55, 0.3)',
        'tickfont': {'color': '#8B9DC3'}
    },
    'legend': {'font': {'color': '#B8C5D9'}, 'bgcolor': 'rgba(26, 39, 66, 0.8)'},
    'colorway': ['#D4AF37', '#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#A8D8EA']
}

def apply_chart_theme(fig):
    """Apply Dubai luxury theme to plotly figures"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', color='#B8C5D9'),
        title=dict(font=dict(family='Playfair Display, serif', color='#D4AF37', size=18)),
        xaxis=dict(
            gridcolor='rgba(212, 175, 55, 0.1)',
            linecolor='rgba(212, 175, 55, 0.3)',
            tickfont=dict(color='#8B9DC3')
        ),
        yaxis=dict(
            gridcolor='rgba(212, 175, 55, 0.1)',
            linecolor='rgba(212, 175, 55, 0.3)',
            tickfont=dict(color='#8B9DC3')
        ),
        legend=dict(font=dict(color='#B8C5D9'), bgcolor='rgba(26, 39, 66, 0.8)'),
        hoverlabel=dict(
            bgcolor='#1A2742',
            font_size=12,
            font_family='Inter, sans-serif',
            bordercolor='#D4AF37'
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("⚠️ Data file 'dubai_mall_simple.csv' not found. Please ensure the file is in the same directory.")
        st.stop()
    
    # ========================================
    # SIDEBAR
    # ========================================
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🏬 Dubai Mall Analytics</div>', unsafe_allow_html=True)
        
        st.markdown("### 📅 Date Range")
        date_range = st.date_input(
            "Select Period",
            value=(df['date'].min(), df['date'].max()),
            min_value=df['date'].min(),
            max_value=df['date'].max()
        )
        
        st.markdown("### 🏪 Store Filters")
        
        # Category filter
        categories = ['All'] + sorted(df['category'].unique().tolist())
        selected_category = st.selectbox("Category", categories)
        
        # Floor filter
        floors = ['All'] + sorted(df['floor'].unique().tolist())
        selected_floor = st.selectbox("Floor", floors)
        
        # Store filter
        if selected_category != 'All':
            available_stores = df[df['category'] == selected_category]['store_name'].unique().tolist()
        else:
            available_stores = df['store_name'].unique().tolist()
        
        selected_stores = st.multiselect(
            "Select Stores",
            options=sorted(available_stores),
            default=[]
        )
        
        st.markdown("### 📊 View Options")
        show_tourist_analysis = st.checkbox("Show Tourist Analysis", value=True)
        show_store_details = st.checkbox("Show Store Details", value=True)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #8B9DC3; font-size: 0.85rem;'>
            <p>📍 Dubai Mall Dashboard</p>
            <p>Data Period: Jan 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================
    # FILTER DATA
    # ========================================
    filtered_df = df.copy()
    
    # Date filter
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= date_range[0]) & 
            (filtered_df['date'].dt.date <= date_range[1])
        ]
    
    # Category filter
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Floor filter
    if selected_floor != 'All':
        filtered_df = filtered_df[filtered_df['floor'] == selected_floor]
    
    # Store filter
    if selected_stores:
        filtered_df = filtered_df[filtered_df['store_name'].isin(selected_stores)]
    
    # ========================================
    # HEADER
    # ========================================
    st.markdown("""
    <div class="main-header">
        <h1>🏬 Dubai Mall Analytics Dashboard</h1>
        <p>Real-time Retail Performance Intelligence | Premium Analytics Suite</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================
    # KEY METRICS
    # ========================================
    st.markdown('<div class="section-header">📊 Executive Summary</div>', unsafe_allow_html=True)
    
    # Calculate KPIs
    total_sales = filtered_df['sales_aed'].sum()
    total_footfall = filtered_df.groupby('date')['mall_footfall'].first().sum()
    total_transactions = filtered_df['transactions'].sum()
    avg_conversion = filtered_df['conversion_rate'].mean() * 100
    avg_basket = filtered_df['avg_basket_aed'].mean()
    sales_per_sqft = filtered_df['sales_per_sqft'].mean()
    
    # Create KPI cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(create_kpi_card("💰", "Total Sales", format_currency(total_sales), 12.5), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card("👥", "Mall Footfall", format_number(total_footfall), 8.3), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_kpi_card("🛒", "Transactions", format_number(total_transactions), 15.2), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_kpi_card("📈", "Conversion Rate", f"{avg_conversion:.1f}%", 3.2), unsafe_allow_html=True)
    
    with col5:
        st.markdown(create_kpi_card("🧺", "Avg Basket", format_currency(avg_basket), 5.8), unsafe_allow_html=True)
    
    with col6:
        st.markdown(create_kpi_card("📐", "Sales/Sqft", format_currency(sales_per_sqft), 7.1), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # MAIN TABS
    # ========================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Sales Overview", 
        "👥 Footfall Analytics", 
        "🏪 Store Performance",
        "📊 Category Insights",
        "🎯 Deep Dive Analysis"
    ])
    
    # ========================================
    # TAB 1: SALES OVERVIEW
    # ========================================
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📈 Daily Sales Trend</div>', unsafe_allow_html=True)
            
            daily_sales = filtered_df.groupby('date').agg({
                'sales_aed': 'sum',
                'transactions': 'sum'
            }).reset_index()
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['date'],
                    y=daily_sales['sales_aed'],
                    name='Sales (AED)',
                    line=dict(color='#D4AF37', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(212, 175, 55, 0.1)'
                ),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Bar(
                    x=daily_sales['date'],
                    y=daily_sales['transactions'],
                    name='Transactions',
                    marker_color='rgba(78, 205, 196, 0.6)',
                    opacity=0.7
                ),
                secondary_y=True
            )
            
            fig = apply_chart_theme(fig)
            fig.update_layout(
                height=400,
                yaxis_title='Sales (AED)',
                yaxis2_title='Transactions',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📅 Sales by Day of Week</div>', unsafe_allow_html=True)
            
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pattern = filtered_df.groupby('day_name')['sales_aed'].sum().reindex(day_order)
            
            fig = go.Figure(go.Bar(
                x=daily_pattern.values,
                y=daily_pattern.index,
                orientation='h',
                marker=dict(
                    color=daily_pattern.values,
                    colorscale=[[0, '#1A2742'], [0.5, '#D4AF37'], [1, '#F4E4BC']],
                    line=dict(color='#D4AF37', width=1)
                )
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=400, xaxis_title='Total Sales (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Weekend vs Weekday Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🗓️ Weekend vs Weekday Performance</div>', unsafe_allow_html=True)
            
            weekend_analysis = filtered_df.groupby('is_weekend').agg({
                'sales_aed': 'sum',
                'transactions': 'sum',
                'conversion_rate': 'mean'
            }).reset_index()
            weekend_analysis['type'] = weekend_analysis['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Sales (AED)',
                x=weekend_analysis['type'],
                y=weekend_analysis['sales_aed'],
                marker_color='#D4AF37'
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=350, xaxis_title='', yaxis_title='Total Sales (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">💳 Hourly Transaction Pattern</div>', unsafe_allow_html=True)
            
            # Simulate hourly data based on conversion patterns
            hours = list(range(10, 23))
            hourly_pattern = [30, 45, 65, 80, 75, 70, 85, 95, 100, 90, 75, 55, 40]
            
            fig = go.Figure(go.Scatter(
                x=hours,
                y=hourly_pattern,
                mode='lines+markers',
                line=dict(color='#4ECDC4', width=3, shape='spline'),
                marker=dict(size=10, color='#D4AF37', line=dict(width=2, color='#FFFFFF')),
                fill='tozeroy',
                fillcolor='rgba(78, 205, 196, 0.1)'
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(
                height=350,
                xaxis_title='Hour of Day',
                yaxis_title='Transaction Index',
                xaxis=dict(tickmode='linear', dtick=2)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 2: FOOTFALL ANALYTICS
    # ========================================
    with tab2:
        if show_tourist_analysis:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">🌍 Tourist vs Resident Footfall</div>', unsafe_allow_html=True)
                
                daily_footfall = filtered_df.groupby('date').agg({
                    'tourist_footfall': 'first',
                    'resident_footfall': 'first'
                }).reset_index()
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=daily_footfall['date'],
                    y=daily_footfall['tourist_footfall'],
                    name='Tourists',
                    stackgroup='one',
                    fillcolor='rgba(212, 175, 55, 0.6)',
                    line=dict(color='#D4AF37', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=daily_footfall['date'],
                    y=daily_footfall['resident_footfall'],
                    name='Residents',
                    stackgroup='one',
                    fillcolor='rgba(78, 205, 196, 0.6)',
                    line=dict(color='#4ECDC4', width=2)
                ))
                
                fig = apply_chart_theme(fig)
                fig.update_layout(height=400, yaxis_title='Footfall Count')
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">📊 Visitor Composition</div>', unsafe_allow_html=True)
                
                avg_tourist_share = filtered_df['tourist_share'].mean() * 100
                avg_resident_share = filtered_df['resident_share'].mean() * 100
                
                fig = go.Figure(go.Pie(
                    labels=['Tourists', 'Residents'],
                    values=[avg_tourist_share, avg_resident_share],
                    hole=0.65,
                    marker=dict(
                        colors=['#D4AF37', '#4ECDC4'],
                        line=dict(color='#0A1628', width=3)
                    ),
                    textinfo='label+percent',
                    textfont=dict(size=14, color='#FFFFFF'),
                    hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"
                ))
                
                fig.add_annotation(
                    text=f"<b>Visitor<br>Mix</b>",
                    x=0.5, y=0.5,
                    font=dict(size=16, color='#D4AF37', family='Playfair Display, serif'),
                    showarrow=False
                )
                
                fig = apply_chart_theme(fig)
                fig.update_layout(height=400, showlegend=True)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Footfall vs Sales Correlation
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔗 Footfall to Sales Correlation by Category</div>', unsafe_allow_html=True)
        
        category_corr = filtered_df.groupby('category').agg({
            'store_footfall': 'sum',
            'sales_aed': 'sum',
            'conversion_rate': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            category_corr,
            x='store_footfall',
            y='sales_aed',
            size='conversion_rate',
            color='category',
            hover_name='category',
            size_max=60,
            color_discrete_sequence=['#D4AF37', '#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#A8D8EA']
        )
        
        fig = apply_chart_theme(fig)
        fig.update_layout(
            height=450,
            xaxis_title='Total Store Footfall',
            yaxis_title='Total Sales (AED)',
            legend_title='Category'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 3: STORE PERFORMANCE
    # ========================================
    with tab3:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏆 Top 10 Stores by Sales</div>', unsafe_allow_html=True)
            
            top_stores = filtered_df.groupby('store_name').agg({
                'sales_aed': 'sum',
                'category': 'first'
            }).nlargest(10, 'sales_aed').reset_index()
            
            fig = go.Figure(go.Bar(
                x=top_stores['sales_aed'],
                y=top_stores['store_name'],
                orientation='h',
                marker=dict(
                    color=top_stores['sales_aed'],
                    colorscale=[[0, '#2D3E5F'], [0.5, '#D4AF37'], [1, '#F4E4BC']],
                    line=dict(color='#D4AF37', width=1)
                ),
                text=[format_currency(x) for x in top_stores['sales_aed']],
                textposition='inside',
                textfont=dict(color='#0A1628', size=11, family='Inter')
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=450, xaxis_title='Total Sales (AED)', yaxis_title='')
            fig.update_yaxes(categoryorder='total ascending')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📈 Top 10 Stores by Conversion Rate</div>', unsafe_allow_html=True)
            
            conversion_leaders = filtered_df.groupby('store_name').agg({
                'conversion_rate': 'mean',
                'category': 'first'
            }).nlargest(10, 'conversion_rate').reset_index()
            conversion_leaders['conversion_pct'] = conversion_leaders['conversion_rate'] * 100
            
            fig = go.Figure(go.Bar(
                x=conversion_leaders['conversion_pct'],
                y=conversion_leaders['store_name'],
                orientation='h',
                marker=dict(
                    color=conversion_leaders['conversion_pct'],
                    colorscale=[[0, '#2D3E5F'], [0.5, '#4ECDC4'], [1, '#95E1D3']],
                    line=dict(color='#4ECDC4', width=1)
                ),
                text=[f"{x:.1f}%" for x in conversion_leaders['conversion_pct']],
                textposition='inside',
                textfont=dict(color='#0A1628', size=11, family='Inter')
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=450, xaxis_title='Conversion Rate (%)', yaxis_title='')
            fig.update_yaxes(categoryorder='total ascending')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if show_store_details:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏪 Store Performance Matrix</div>', unsafe_allow_html=True)
            
            store_matrix = filtered_df.groupby(['store_name', 'category', 'floor']).agg({
                'sales_aed': 'sum',
                'transactions': 'sum',
                'store_footfall': 'sum',
                'conversion_rate': 'mean',
                'avg_basket_aed': 'mean',
                'sales_per_sqft': 'mean',
                'store_area_sqft': 'first'
            }).reset_index()
            
            store_matrix['conversion_rate'] = store_matrix['conversion_rate'] * 100
            
            # Format for display
            display_df = store_matrix.copy()
            display_df['sales_aed'] = display_df['sales_aed'].apply(lambda x: f"AED {x:,.0f}")
            display_df['avg_basket_aed'] = display_df['avg_basket_aed'].apply(lambda x: f"AED {x:,.0f}")
            display_df['sales_per_sqft'] = display_df['sales_per_sqft'].apply(lambda x: f"AED {x:,.0f}")
            display_df['conversion_rate'] = display_df['conversion_rate'].apply(lambda x: f"{x:.1f}%")
            display_df.columns = ['Store', 'Category', 'Floor', 'Total Sales', 'Transactions', 
                                 'Footfall', 'Conversion', 'Avg Basket', 'Sales/Sqft', 'Area (sqft)']
            
            st.dataframe(
                display_df.sort_values('Total Sales', ascending=False),
                use_container_width=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 4: CATEGORY INSIGHTS
    # ========================================
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Sales by Category</div>', unsafe_allow_html=True)
            
            category_sales = filtered_df.groupby('category')['sales_aed'].sum().sort_values(ascending=True)
            
            fig = go.Figure(go.Bar(
                x=category_sales.values,
                y=category_sales.index,
                orientation='h',
                marker=dict(
                    color=['#D4AF37', '#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#A8D8EA'][:len(category_sales)],
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=[format_currency(x) for x in category_sales.values],
                textposition='inside',
                textfont=dict(color='#0A1628', size=11)
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=400, xaxis_title='Total Sales (AED)', yaxis_title='')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🧺 Average Basket by Category</div>', unsafe_allow_html=True)
            
            category_basket = filtered_df.groupby('category')['avg_basket_aed'].mean().sort_values(ascending=True)
            
            fig = go.Figure(go.Bar(
                x=category_basket.values,
                y=category_basket.index,
                orientation='h',
                marker=dict(
                    color=category_basket.values,
                    colorscale='Viridis',
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=[format_currency(x) for x in category_basket.values],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=11)
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=400, xaxis_title='Average Basket (AED)', yaxis_title='')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Category Performance Radar Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🎯 Category Performance Radar</div>', unsafe_allow_html=True)
        
        category_metrics = filtered_df.groupby('category').agg({
            'sales_aed': 'sum',
            'transactions': 'sum',
            'conversion_rate': 'mean',
            'avg_basket_aed': 'mean',
            'sales_per_sqft': 'mean'
        }).reset_index()
        
        # Normalize metrics for radar chart
        for col in ['sales_aed', 'transactions', 'conversion_rate', 'avg_basket_aed', 'sales_per_sqft']:
            max_val = category_metrics[col].max()
            if max_val > 0:
                category_metrics[f'{col}_norm'] = category_metrics[col] / max_val * 100
        
        categories_list = ['Sales', 'Transactions', 'Conversion', 'Avg Basket', 'Sales/Sqft']
        
        fig = go.Figure()
        
        colors = ['#D4AF37', '#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#A8D8EA']
        
        for idx, (_, row) in enumerate(category_metrics.iterrows()):
            values = [
                row['sales_aed_norm'],
                row['transactions_norm'],
                row['conversion_rate_norm'],
                row['avg_basket_aed_norm'],
                row['sales_per_sqft_norm']
            ]
            values.append(values[0])  # Close the radar
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories_list + [categories_list[0]],
                name=row['category'],
                line=dict(color=colors[idx % len(colors)], width=2),
                fill='toself',
                fillcolor=f'rgba({int(colors[idx % len(colors)][1:3], 16)}, {int(colors[idx % len(colors)][3:5], 16)}, {int(colors[idx % len(colors)][5:7], 16)}, 0.1)'
            ))
        
        fig = apply_chart_theme(fig)
        fig.update_layout(
            height=500,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='rgba(212, 175, 55, 0.2)',
                    tickfont=dict(color='#8B9DC3')
                ),
                angularaxis=dict(
                    gridcolor='rgba(212, 175, 55, 0.2)',
                    tickfont=dict(color='#B8C5D9', size=12)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 5: DEEP DIVE ANALYSIS
    # ========================================
    with tab5:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏢 Floor-wise Performance</div>', unsafe_allow_html=True)
            
            floor_perf = filtered_df.groupby('floor').agg({
                'sales_aed': 'sum',
                'store_footfall': 'sum',
                'transactions': 'sum'
            }).reset_index()
            
            floor_order = {'LG': 0, 'G': 1, '1': 2, '2': 3, '3': 4}
            floor_perf['order'] = floor_perf['floor'].map(floor_order)
            floor_perf = floor_perf.sort_values('order')
            floor_perf['floor_label'] = floor_perf['floor'].map({
                'LG': 'Lower Ground', 'G': 'Ground', '1': 'Level 1', '2': 'Level 2', '3': 'Level 3'
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Sales (AED)',
                x=floor_perf['floor_label'],
                y=floor_perf['sales_aed'],
                marker_color='#D4AF37',
                text=[format_currency(x) for x in floor_perf['sales_aed']],
                textposition='outside'
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(height=400, xaxis_title='Floor', yaxis_title='Total Sales (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">💵 Rent vs Revenue Analysis</div>', unsafe_allow_html=True)
            
            rent_revenue = filtered_df.groupby('store_name').agg({
                'annual_base_rent_aed': 'first',
                'sales_aed': 'sum',
                'category': 'first'
            }).reset_index()
            
            # Annualize sales (assuming data is for a portion of the year)
            days_in_data = filtered_df['date'].nunique()
            rent_revenue['annualized_sales'] = rent_revenue['sales_aed'] * (365 / days_in_data)
            rent_revenue['rent_to_sales'] = (rent_revenue['annual_base_rent_aed'] / rent_revenue['annualized_sales']) * 100
            
            fig = px.scatter(
                rent_revenue,
                x='annual_base_rent_aed',
                y='annualized_sales',
                color='category',
                hover_name='store_name',
                size='rent_to_sales',
                size_max=40,
                color_discrete_sequence=['#D4AF37', '#4ECDC4', '#FF6B6B', '#95E1D3', '#F38181', '#AA96DA', '#FCBAD3', '#A8D8EA']
            )
            
            # Add break-even line (rent = 10% of sales typical retail)
            max_rent = rent_revenue['annual_base_rent_aed'].max()
            fig.add_trace(go.Scatter(
                x=[0, max_rent],
                y=[0, max_rent * 10],
                mode='lines',
                name='Break-even (10%)',
                line=dict(color='#FF6B6B', dash='dash', width=2)
            ))
            
            fig = apply_chart_theme(fig)
            fig.update_layout(
                height=400,
                xaxis_title='Annual Rent (AED)',
                yaxis_title='Annualized Sales (AED)',
                legend_title='Category'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Heatmap: Category Performance by Day
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🗓️ Category Sales Heatmap by Day of Week</div>', unsafe_allow_html=True)
        
        heatmap_data = filtered_df.pivot_table(
            values='sales_aed',
            index='category',
            columns='day_name',
            aggfunc='sum'
        )
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data[day_order]
        
        fig = go.Figure(go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=[
                [0, '#0A1628'],
                [0.25, '#1A2742'],
                [0.5, '#2D3E5F'],
                [0.75, '#D4AF37'],
                [1, '#F4E4BC']
            ],
            hovertemplate='<b>%{y}</b><br>%{x}: AED %{z:,.0f}<extra></extra>'
        ))
        
        fig = apply_chart_theme(fig)
        fig.update_layout(height=400, xaxis_title='Day of Week', yaxis_title='Category')
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Performance Insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💡 Key Insights & Recommendations</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        # Calculate insights
        best_day = filtered_df.groupby('day_name')['sales_aed'].sum().idxmax()
        best_category = filtered_df.groupby('category')['sales_aed'].sum().idxmax()
        best_floor = filtered_df.groupby('floor')['sales_aed'].sum().idxmax()
        avg_tourist_pct = filtered_df['tourist_share'].mean() * 100
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h4>🏆 Peak Performance</h4>
                <p><strong>Best Day:</strong> {best_day}</p>
                <p><strong>Top Category:</strong> {best_category}</p>
                <p><strong>Top Floor:</strong> {best_floor}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <h4>🌍 Visitor Insights</h4>
                <p><strong>Tourist Share:</strong> {avg_tourist_pct:.1f}%</p>
                <p><strong>Resident Share:</strong> {100-avg_tourist_pct:.1f}%</p>
                <p><strong>Weekend Boost:</strong> +15-20%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            top_performer = filtered_df.groupby('store_name')['sales_aed'].sum().idxmax()
            top_conversion = filtered_df.groupby('store_name')['conversion_rate'].mean().idxmax()
            st.markdown(f"""
            <div class="info-box">
                <h4>⭐ Top Performers</h4>
                <p><strong>Sales Leader:</strong> {top_performer}</p>
                <p><strong>Conversion Leader:</strong> {top_conversion}</p>
                <p><strong>Opportunity:</strong> F&B Expansion</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
    <div class="custom-footer">
        <p><span class="gold-text">🏬 Dubai Mall Analytics Dashboard</span></p>
        <p>Premium Retail Intelligence Platform | Powered by Advanced Analytics</p>
        <p style="font-size: 0.8rem; margin-top: 15px;">© 2024 Dubai Mall Management | Dashboard v2.0</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()