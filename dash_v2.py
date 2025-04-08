import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Denmark-India Macroeconomic Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #2563EB;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .insight-box {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .event-box {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .guide-text {
        color: #4B5563;
        font-style: italic;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown('<div class="main-header">Denmark-India Macroeconomic Dashboard (2014-2024)</div>', unsafe_allow_html=True)

st.markdown("""
This dashboard provides a comprehensive analysis of macroeconomic indicators for Denmark and India from 2014 to 2024.
It allows for comparative analysis of economic growth, inflation, unemployment, government finances, and trade patterns.
""")

# Function to load data
@st.cache_data
def load_data():
        years = list(range(2014, 2025))
        
        data = []
        
        # Sample data for Denmark GDP growth (constant prices)
        denmark_gdp_growth = [1.278, 2.101, 3.076, 3.056, 1.859, 1.713, -1.781, 7.38, 1.541, 2.495, 1.943]  # Sample values
        for year, value in zip(years, denmark_gdp_growth):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Gross domestic product, constant prices',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India GDP growth (constant prices)
        india_gdp_growth = [7.41, 7.996, 8.256, 6.795, 6.454, 3.871, -5.778, 9.69, 6.987, 8.153, 7.021]  # Sample values
        for year, value in zip(years, india_gdp_growth):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Gross domestic product, constant prices',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark GDP current prices (National currency)
        denmark_gdp_current = [1980.26, 2030.21, 2101.52, 2189.59, 2243.54, 2303.64, 2326.59, 2567.52, 2844.23, 2804.74, 2842.10]  # Sample values in billions
        for year, value in zip(years, denmark_gdp_current):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Gross domestic product, current prices',
                'Units': 'National currency',
                'Scale': 'Billions',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India GDP current prices (National currency)
        india_gdp_current = [124679.60, 137718.70, 153916.70, 170900.40, 188996.70, 201035.90, 198541.00, 235974.00, 269496.50, 295356.70, 325061.42]  # Sample values in trillions
        for year, value in zip(years, india_gdp_current):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Gross domestic product, current prices',
                'Units': 'National currency',
                'Scale': 'Billions',  # Actually trillions for India
                'Year': year,
                'Value': value * 1000  # Converting to billions for consistency
            })
            
        # Sample data for Denmark Inflation
        denmark_inflation = [0.352, 0.226, 0.017, 1.058, 0.709, 0.729, 0.333, 1.944, 8.534, 3.353, 1.8]  # Sample values
        for year, value in zip(years, denmark_inflation):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Inflation, average consumer prices',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Inflation
        india_inflation = [5.833, 4.908, 4.525, 3.587, 3.414, 4.769, 6.165, 5.506, 6.653, 5.361, 4.374]  # Sample values
        for year, value in zip(years, india_inflation):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Inflation, average consumer prices',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
        denmark_deflator = [93.936, 94.323, 94.723, 95.766, 96.335, 97.249, 100, 102.771, 112.119, 107.871, 107.224]
        for year, value in zip(years, denmark_deflator):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Gross domestic product, deflator',
                'Units': 'Index',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
        
        # Adding GDP Deflator data for India
        india_deflator = [118.43, 121.13, 125.052, 130.016, 135.066, 138.315, 144.975, 157.087, 167.687, 169.924, 174.745]
        for year, value in zip(years, india_deflator):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Gross domestic product, deflator',
                'Units': 'Index',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Unemployment
        denmark_unemployment = [4.992, 4.542, 4.125, 4.2, 3.85, 3.658, 4.65, 3.608, 2.517, 2.783, 2.9]  # Sample values
        for year, value in zip(years, denmark_unemployment):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Unemployment rate',
                'Units': 'Percent of total labor force',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Unemployment
        india_unemployment = [5.44, 5.44, 5.42, 5.36, 5.33, 5.27, 8.00, 5.98, 7.33, 8.00, 7.80]
        for year, value in zip(years, india_unemployment):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Unemployment rate',
                'Units': 'Percent of total labor force',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Exports
        denmark_exports = [3.019, 3.232, 3.662, 4.806, 3.404, 4.417, -6.36, 8.815, 7.19, 10.447, 6.9]  # Sample values
        for year, value in zip(years, denmark_exports):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Volume of exports of goods and services',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Exports
        india_exports = [4.276, -5.03, 6.677, 10.168, 4.899, -2.142, -6.511, 19.732, 9.679, 0.381, 3.5]  # Sample values
        for year, value in zip(years, india_exports):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Volume of exports of goods and services',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Imports
        denmark_imports = [4.068, 4.063, 4.286, 4.322, 5.705, 3.053, -3.954, 9.493, 4.395, 3.757, 3.42]  # Sample values
        for year, value in zip(years, denmark_imports):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Volume of imports of goods and services',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Imports
        india_imports = [6.111, 1.18, 4.521, 13.36, 3.933, -3.735, -13.702, 19.371, 9.944, -1.201, 4.416]  # Sample values
        for year, value in zip(years, india_imports):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Volume of imports of goods and services',
                'Units': 'Percent change',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Budget Balance
        denmark_budget = [1.428, -0.895, 0.302, 1.689, 0.81, 4.283, 0.363, 4.098, 3.444, 3.306, 1.793]  # Sample values
        for year, value in zip(years, denmark_budget):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'General government net lending/borrowing',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Budget Balance
        india_budget = [-7.071, -7.205, -7.12, -6.227, -6.376, -7.694, -12.864, -9.268, -9.195, -8.32, -7.782]  # Sample values
        for year, value in zip(years, india_budget):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'General government net lending/borrowing',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Government Debt
        denmark_debt = [877.067, 809.934, 783.958, 787.127, 766.125, 778.438, 981.155, 918.686, 844.683, 831.959, 800.989]  # Sample values
        for year, value in zip(years, denmark_debt):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'General government gross debt',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Government Debt
        india_debt = [83662.56, 95092.82, 106114.93, 119065.25, 133039.21, 150858.14, 175563.07, 197006.52, 220134.08, 245206.57, 270010.00]  # Sample values
        for year, value in zip(years, india_debt):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'General government gross debt',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Investment
        denmark_investment = [20.148, 20.544, 21.681, 21.957, 22.532, 21.886, 22.763, 23.602, 24.694, 22.827, 21.931]  # Sample values
        for year, value in zip(years, denmark_investment):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Total investment',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Investment
        india_investment = [34.268, 32.117, 30.172, 30.982, 32.343, 30.096, 28.922, 32.116, 33.024, 33.32, 33.676]  # Sample values
        for year, value in zip(years, india_investment):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Total investment',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for Denmark Savings
        denmark_savings = [28.55, 28.5, 28.768, 29.28, 28.839, 29.332, 29.989, 32.28, 36.352, 32.662, 30.976]  # Sample values
        for year, value in zip(years, denmark_savings):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Gross national savings',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
            
        # Sample data for India Savings
        # Sample data for India Savings
        india_savings = [32.954, 31.067, 29.547, 29.147, 30.228, 29.23, 29.82, 30.894, 31.026, 32.669, 32.53]  # Sample values
        for year, value in zip(years, india_savings):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Gross national savings',
                'Units': 'Percent of GDP',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })

        # Sample data for India Population
        india_population = [1307.25, 1322.87, 1338.64, 1354.20, 1369.00, 1383.11, 1396.39, 1407.56, 1417.17, 1428.63, 1441.72]  # Sample values in millions
        for year, value in zip(years, india_population):
            data.append({
                'Country': 'India',
                'Subject Descriptor': 'Population',
                'Units': 'Millions',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })

        # Sample data for Denmark Population
        denmark_population = [5.627, 5.66, 5.707, 5.749, 5.781, 5.806, 5.823, 5.84, 5.873, 5.933, 5.952]  # Sample values in millions
        for year, value in zip(years, denmark_population):
            data.append({
                'Country': 'Denmark',
                'Subject Descriptor': 'Population',
                'Units': 'Millions',
                'Scale': 'Units',
                'Year': year,
                'Value': value
            })
                    
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        return df

# Load the data
df = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "Dashboard Overview",
        "Population Comparison",
        "GDP Analysis",
        "Inflation & Unemployment",
        "Trade & Investment",
        "Trump Effect",
        "Government Finances",
        "Correlation Analysis",
        "Macroeconomic Events", 
        "IMF Analysis",
        "References"
    ]
)

# Create a dictionary for quick data filtering
@st.cache_data
def get_indicator_data(df, country, indicator, units=None):
    if units:
        filtered_df = df[(df['Country'] == country) & 
                         (df['Subject Descriptor'] == indicator) &
                         (df['Units'] == units)]
    else:
        filtered_df = df[(df['Country'] == country) & 
                         (df['Subject Descriptor'] == indicator)]
    
    return filtered_df.sort_values(by='Year')

# Define key economic events for the timeline
economic_events = {
    2014: {
        "Global": "Oil prices crash from over $100 to under $50 per barrel",
        "India": "Modi government elected, 'Make in India' initiative launched",
        "Denmark": "Economic recovery strengthens post-financial crisis"
    },
    2016: {
        "Global": "Brexit referendum; Donald Trump elected US President",
        "India": "Demonetization policy implemented",
        "Denmark": "Negative interest rates policy continued by central bank"
    },
    2017: {
        "Global": "Global synchronized growth",
        "India": "Implementation of Goods and Services Tax (GST)",
        "Denmark": "Strong export performance drives economic growth"
    },
    2019: {
        "Global": "US-China trade tensions; Global manufacturing slowdown",
        "India": "Corporate tax rate cuts to boost investment",
        "Denmark": "Danish economy showing signs of slowing"
    },
    2020: {
        "Global": "COVID-19 pandemic and global lockdowns",
        "India": "Strict national lockdown; Major economic contraction",
        "Denmark": "Implementation of major fiscal support packages"
    },
    2021: {
        "Global": "Global recovery begins; Supply chain disruptions",
        "India": "Second COVID wave; Vaccination drive begins",
        "Denmark": "Strong economic rebound aided by fiscal support"
    },
    2022: {
        "Global": "Russia-Ukraine conflict; Energy crisis; Global inflation surge",
        "India": "RBI begins rate hike cycle to combat inflation",
        "Denmark": "Energy price shock impacts Danish economy"
    },
    2023: {
        "Global": "Persistent inflation; Central banks tighten monetary policy",
        "India": "Resilient growth despite global headwinds",
        "Denmark": "Inflation pressures begin to moderate"
    },
    2024: {
        "Global": "Monetary policy normalization; Focus on debt sustainability",
        "India": "Infrastructure push continues; Manufacturing focus",
        "Denmark": "Return to more balanced economic growth"
    }
}

# Helper function to create comparative line charts
def create_comparative_line_chart(df, indicator, units=None, title=None, ylabel=None):
    denmark_data = get_indicator_data(df, 'Denmark', indicator, units)
    india_data = get_indicator_data(df, 'India', indicator, units)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=denmark_data['Year'],
        y=denmark_data['Value'],
        mode='lines+markers',
        name='Denmark',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=india_data['Year'],
        y=india_data['Value'],
        mode='lines+markers',
        name='India',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title=ylabel if ylabel else units,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template="plotly_white",
        height=450
    )
    
    return fig
def create_insight_box(title, insights):
    with st.container():
        st.markdown(f"""
        <div style="background-color:#f8f9fa; padding:15px; border-radius:5px; border-left:5px solid #3B82F6;">
            <h4 style="color:#1e3a8a;">{title}</h4>
            <ul style="margin-bottom:0;">
                {"".join([f"<li>{insight}</li>" for insight in insights])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
# Helper function to calculate correlation between indicators
def calculate_correlations(df, country):
    # Get the relevant indicators
    indicators = [
        ('GDP Growth', 'Gross domestic product, constant prices', 'Percent change'),
        ('Inflation', 'Inflation, average consumer prices', 'Percent change'),
        ('Unemployment', 'Unemployment rate', 'Percent of total labor force'),
        ('Exports', 'Volume of exports of goods and services', 'Percent change'),
        ('Imports', 'Volume of imports of goods and services', 'Percent change'),
        ('Budget Balance', 'General government net lending/borrowing', 'Percent of GDP'),
        ('Investment', 'Total investment', 'Percent of GDP'),
        ('Savings', 'Gross national savings', 'Percent of GDP'),
        ('Population', 'Population', 'Millions')  # Added population as an indicator
    ]
    
    # Create a dataframe with years as index and indicators as columns
    data = {}
    years = sorted(df['Year'].unique())
    
    for name, indicator, unit in indicators:
        indicator_data = get_indicator_data(df, country, indicator, unit)
        if not indicator_data.empty:
            data[name] = {row['Year']: row['Value'] for _, row in indicator_data.iterrows()}
    
    # Convert to DataFrame
    corr_df = pd.DataFrame({name: [data[name].get(year, np.nan) for year in years] 
                            for name in data.keys()}, index=years)
    
    # Calculate correlation
    correlation = corr_df.corr()
    
    return correlation
    
    # Create a dataframe with years as index and indicators as columns
    data = {}
    years = sorted(df['Year'].unique())
    
    for name, indicator, unit in indicators:
        indicator_data = get_indicator_data(df, country, indicator, unit)
        if not indicator_data.empty:
            data[name] = {row['Year']: row['Value'] for _, row in indicator_data.iterrows()}
    
    # Convert to DataFrame
    corr_df = pd.DataFrame({name: [data[name].get(year, np.nan) for year in years] 
                            for name in data.keys()}, index=years)
    
    # Calculate correlation
    correlation = corr_df.corr()
    
    return correlation

# Dashboard Overview
if section == "Dashboard Overview":
    st.markdown('<div class="sub-header">Macroeconomic Dashboard Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Denmark Snapshot (2024)</div>', unsafe_allow_html=True)
        
        dk_gdp_growth = get_indicator_data(df, 'Denmark', 'Gross domestic product, constant prices', 'Percent change')
        dk_latest_gdp = dk_gdp_growth[dk_gdp_growth['Year'] == dk_gdp_growth['Year'].max()]['Value'].values[0]
        
        dk_inflation = get_indicator_data(df, 'Denmark', 'Inflation, average consumer prices', 'Percent change')
        dk_latest_inflation = dk_inflation[dk_inflation['Year'] == dk_inflation['Year'].max()]['Value'].values[0]
        
        dk_unemployment = get_indicator_data(df, 'Denmark', 'Unemployment rate', 'Percent of total labor force')
        dk_latest_unemployment = dk_unemployment[dk_unemployment['Year'] == dk_unemployment['Year'].max()]['Value'].values[0]
        
        dk_budget = get_indicator_data(df, 'Denmark', 'General government net lending/borrowing', 'Percent of GDP')
        dk_latest_budget = dk_budget[dk_budget['Year'] == dk_budget['Year'].max()]['Value'].values[0]
        
        # Create metrics
        st.metric("GDP Growth", f"{dk_latest_gdp:.1f}%")
        st.metric("Inflation", f"{dk_latest_inflation:.1f}%")
        st.metric("Unemployment Rate", f"{dk_latest_unemployment:.1f}%")
        st.metric("Budget Balance", f"{dk_latest_budget:+.1f}% of GDP")
        
        # Add key insight
        st.markdown('<div class="insight-box">Denmark has maintained stable economic growth with relatively low inflation and unemployment, along with a budget surplus. As a developed economy, growth rates are moderate but sustainable.</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">India Snapshot (2024)</div>', unsafe_allow_html=True)
        
        in_gdp_growth = get_indicator_data(df, 'India', 'Gross domestic product, constant prices', 'Percent change')
        in_latest_gdp = in_gdp_growth[in_gdp_growth['Year'] == in_gdp_growth['Year'].max()]['Value'].values[0]
        
        in_inflation = get_indicator_data(df, 'India', 'Inflation, average consumer prices', 'Percent change')
        in_latest_inflation = in_inflation[in_inflation['Year'] == in_inflation['Year'].max()]['Value'].values[0]
        
        in_unemployment = get_indicator_data(df, 'India', 'Unemployment rate', 'Percent of total labor force')
        in_latest_unemployment = in_unemployment[in_unemployment['Year'] == in_unemployment['Year'].max()]['Value'].values[0]
        
        in_budget = get_indicator_data(df, 'India', 'General government net lending/borrowing', 'Percent of GDP')
        in_latest_budget = in_budget[in_budget['Year'] == in_budget['Year'].max()]['Value'].values[0]
        
        # Create metrics
        st.metric("GDP Growth", f"{in_latest_gdp:.1f}%")
        st.metric("Inflation", f"{in_latest_inflation:.1f}%")
        st.metric("Unemployment Rate", f"{in_latest_unemployment:.1f}%")
        st.metric("Budget Balance", f"{in_latest_budget:+.1f}% of GDP")
        
        # Add key insight
        st.markdown('<div class="insight-box">India maintains robust growth as an emerging economy with moderately high inflation. Despite fiscal deficits, Indias economic momentum remains strong, driven by domestic consumption and services sector growth.</div>', unsafe_allow_html=True)
    
    # Key comparative charts
    st.markdown('<div class="section-header">Key Comparative Indicators (2014-2024)</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["GDP Growth", "Inflation", "Unemployment", "Budget Balance"])
    
    with tab1:
        fig = create_comparative_line_chart(
            df, 
            'Gross domestic product, constant prices', 
            'Percent change',
            'GDP Growth Rate Comparison (2014-2024)',
            'Annual Percent Change (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">India consistently shows higher GDP growth rates compared to Denmark, reflecting the difference between a rapidly developing economy and a mature developed economy. Note the significant impact of COVID-19 in 2020 on both economies, with a stronger recovery bounce in India during 2021.</div>', unsafe_allow_html=True)
    
    with tab2:
        fig = create_comparative_line_chart(
            df, 
            'Inflation, average consumer prices', 
            'Percent change',
            'Inflation Rate Comparison (2014-2024)',
            'Annual Percent Change (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">India historically maintains higher inflation rates than Denmark. While Denmark experienced significant inflation spikes in 2022 due to energy crises and supply chain disruptions, Indias inflation has been more consistent but structurally higher, reflecting different monetary policy priorities and economic structures.</div>', unsafe_allow_html=True)
    
    with tab3:
        fig = create_comparative_line_chart(
            df, 
            'Unemployment rate', 
            'Percent of total labor force',
            'Unemployment Rate Comparison (2014-2024)',
            'Percent of Labor Force (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">Denmark shows a generally declining unemployment trend over the decade with a temporary COVID-related spike. Indias unemployment rose significantly during the pandemic and has taken longer to recover, reflecting differences in labor market flexibility and social safety net structures.</div>', unsafe_allow_html=True)
        
    with tab4:
        fig = create_comparative_line_chart(
            df, 
            'General government net lending/borrowing', 
            'Percent of GDP',
            'Budget Balance Comparison (2014-2024)',
            'Percent of GDP (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('<div class="insight-box">Denmark has maintained budget surpluses for much of the period, temporarily disrupted by COVID-19 spending needs. In contrast, India consistently runs significant budget deficits, reflecting different fiscal policy approaches and developmental needs.</div>', unsafe_allow_html=True)
# Additional sections based on navigation
# if section == "GDP Analysis":
#     st.markdown('<div class="sub-header">GDP Analysis</div>', unsafe_allow_html=True)
#     st.markdown("This section provides a detailed analysis of GDP trends for Denmark and India.")
    
#     # Comparative GDP Growth Chart
#     fig = create_comparative_line_chart(
#         df,
#         'Gross domestic product, constant prices',
#         'Percent change',
#         'GDP Growth Rate Comparison (2014-2024)',
#         'Annual Percent Change (%)'
#     )
#     st.plotly_chart(fig, use_container_width=True)

#     # Insights
#     st.markdown('<div class="insight-box">India’s GDP growth consistently outpaces Denmark’s, reflecting its status as a developing economy. Denmark’s growth is more stable, indicative of a mature economy.</div>', unsafe_allow_html=True)
if section == "GDP Analysis":
    st.markdown('<h2 class="section-header">GDP Analysis</h2>', unsafe_allow_html=True)
    st.markdown("This section provides a detailed analysis of GDP trends for Denmark and India across multiple metrics.")
    
    # Sample data with consistent lengths (11 years from 2014-2024)
    years = list(range(2014, 2025))  # 11 years
    
    sample_data = {
        'Year': years,
        'Denmark_GDP_growth': [1.278, 2.101, 3.076, 3.056, 1.859, 1.713, -1.781, 7.38, 1.541, 2.495, 1.943],
        'India_GDP_growth': [7.41, 7.996, 8.256, 6.795, 6.454, 3.871, -5.778, 9.69, 6.987, 8.153, 7.021],
        'Denmark_GDP_current_prices_bn': [1980.26, 2030.21, 2101.52, 2189.59, 2243.54, 2303.64, 2326.59, 2567.52, 2844.23, 2804.74, 2842.10],
        'India_GDP_current_prices_bn': [124679.60, 137718.70, 153916.70, 170900.40, 188996.70, 201035.90, 198541.00, 235974.00, 269496.50, 295356.70, 325061.42],
        'Denmark_GDP_current_USD_bn': [352.833, 301.759, 312.182, 331.611, 355.293, 345.402, 355.631, 408.378, 401.946, 407.092, 412.293],
        'India_GDP_current_USD_bn': [2039.13,2103.59,2294.80,2651.47,2702.93,2835.61,2674.85,3167.27,3353.47,3567.55,3889.13],
        'Denmark_GDP_per_capita_constant': [374624.48, 380301.84, 388733.56, 397719.93, 402840.94, 407986.04, 399569.76, 427787.80, 431911.90, 438269.28, 445353.98],
        'India_GDP_per_capita_constant': [80533.17, 85945.86, 91945.73, 97065.59, 102212.39, 105086.50, 98073.59, 106722.34, 113404.84, 121667.25, 129026.52]
    }
    
    df = pd.DataFrame(sample_data)
    
    # 1. Comparative GDP Growth Chart
    fig1 = px.line(df, x='Year', y=['Denmark_GDP_growth', 'India_GDP_growth'], 
                  title='GDP Percentage Change at Constant Prices (2014-2024)',
                  labels={'value': 'Annual Percent Change (%)', 'variable': 'Country'})
    fig1.update_layout(legend_title_text='')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Insight box for GDP growth
    st.markdown("""
    <div class="insight-box">
        <h4>GDP Growth Insights</h4>
        <p>India's GDP growth consistently outpaces Denmark's, reflecting its status as a developing economy. 
        Denmark's growth is more stable (averaging 1.5-2.5%), indicative of a mature economy. 
        Both economies experienced contractions during the pandemic in 2020, but India's recovery has been stronger with a 9.1% rebound in 2021.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. GDP at Current Prices (Local Currency)
    col1, col2 = st.columns(2)
    
    with col1:
        fig2a = px.line(df, x='Year', y=['Denmark_GDP_current_prices_bn'], 
                        title='Denmark GDP at Current Prices (Billion DKK)',
                        labels={'value': 'Billion DKK', 'variable': 'Metric'})
        fig2a.update_layout(legend_title_text='')
        st.plotly_chart(fig2a, use_container_width=True)
    
    with col2:
        fig2b = px.line(df, x='Year', y=['India_GDP_current_prices_bn'], 
                        title='India GDP at Current Prices (Billion INR)',
                        labels={'value': 'Billion INR', 'variable': 'Metric'})
        fig2b.update_layout(legend_title_text='')
        st.plotly_chart(fig2b, use_container_width=True)
    
    # 3. GDP at Current Prices (USD)
    fig3 = px.line(df, x='Year', y=['Denmark_GDP_current_USD_bn', 'India_GDP_current_USD_bn'], 
                   title='GDP at Current Prices (Billion USD)',
                   labels={'value': 'Billion USD', 'variable': 'Country'})
    fig3.update_layout(legend_title_text='')
    st.plotly_chart(fig3, use_container_width=True)
    
    # Insight box for current prices
    st.markdown("""
    <div class="insight-box">
        <h4>GDP at Current Prices Insights</h4>
        <p>While Denmark's economy has grown steadily in local currency terms, India's GDP in USD terms has grown 
        more than twice as fast over the decade. The gap between the two economies has widened considerably since 2014, 
        with India's economy now approximately 10 times larger than Denmark's by 2024 in absolute terms.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. GDP Per Capita at Constant Prices
    fig4 = px.bar(df, x='Year', y=['Denmark_GDP_per_capita_constant', 'India_GDP_per_capita_constant'], 
                 barmode='group', 
                 title='GDP Per Capita at Constant Prices (Local Currency)',
                 labels={'value': 'Local Currency Units', 'variable': 'Country'})
    fig4.update_layout(legend_title_text='')
    st.plotly_chart(fig4, use_container_width=True)
    
    # 5. GDP Per Capita Growth Rate
    df['Denmark_per_capita_growth'] = df['Denmark_GDP_per_capita_constant'].pct_change() * 100
    df['India_per_capita_growth'] = df['India_GDP_per_capita_constant'].pct_change() * 100
    
    fig5 = px.line(df.iloc[1:], x='Year', y=['Denmark_per_capita_growth', 'India_per_capita_growth'], 
                  title='GDP Per Capita Annual Growth Rate (%)',
                  labels={'value': 'Annual % Change', 'variable': 'Country'})
    fig5.update_layout(legend_title_text='')
    st.plotly_chart(fig5, use_container_width=True)
    
    # Insight box for per capita metrics
    st.markdown("""
    <div class="insight-box">
        <h4>GDP Per Capita Insights</h4>
        <p>The wealth gap between Denmark and India remains substantial. Denmark's per capita GDP is approximately 
        2.9 times higher than India's in 2024. However, India is narrowing this gap with consistently higher 
        per capita growth rates, averaging 6.5% annually compared to Denmark's 2% over the past decade.</p>
        <p>Despite the pandemic's economic impact, both countries have shown resilience with their per capita GDP 
        now exceeding pre-pandemic levels, though India's recovery trajectory has been steeper.</p>
    </div>
    """, unsafe_allow_html=True)
    

    
    # Comprehensive insights
    st.markdown("""
    <div class="insight-box">
        <h4>Comprehensive Economic Comparison</h4>
        <p>The economic analysis reveals contrasting patterns between Denmark and India:</p>
        <ul>
            <li><strong>Growth Dynamics:</strong> India consistently achieves higher growth rates but with greater volatility. Denmark exemplifies the steady growth typical of advanced economies.</li>
            <li><strong>Economic Scale:</strong> Despite India's much larger total GDP, Denmark maintains a significant advantage in per capita terms, reflecting higher productivity and living standards.</li>
            <li><strong>Convergence Trajectory:</strong> Based on current trends, India's economy is on a long-term convergence path with developed economies, though the per capita gap remains substantial and will take decades to close at current rates.</li>
            <li><strong>Resilience:</strong> Both economies demonstrated resilience to global economic shocks, though through different mechanisms - Denmark through social safety nets and economic stability, India through demographic advantages and domestic consumption.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# Then add this new section for Population Comparison
elif section == "Population Comparison":
    st.markdown('<div class="sub-header">Population Comparison: Denmark vs India</div>', unsafe_allow_html=True)
    st.markdown("This section provides a comparative analysis of population trends and demographics for Denmark and India.")
    
    # Sample population data (in millions)
    # You can replace with actual data if available
    years = list(range(2014, 2025))
    denmark_population = [5.627, 5.66, 5.707, 5.749, 5.781, 5.806, 5.823, 5.84, 5.873, 5.933, 5.952]  # in millions
    india_population = [1307.25, 1322.87, 1338.64, 1354.20, 1369.00, 1383.11, 1396.39, 1407.56, 1417.17, 1428.63, 1441.72]  # in millions
    
    # Create the population trend chart
    fig = go.Figure()
    
    # Add Denmark population trace
    fig.add_trace(go.Scatter(
        x=years,
        y=denmark_population,
        mode='lines+markers',
        name='Denmark',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8)
    ))
    
    # Create a secondary y-axis for India's population (since it's much larger)
    fig.add_trace(go.Scatter(
        x=years,
        y=india_population,
        mode='lines+markers',
        name='India',
        line=dict(color='#EF4444', width=3),
        marker=dict(size=8),
        yaxis="y2"
    ))
    
    # Update layout with two y-axes
    fig.update_layout(
        title="Population Trends: Denmark vs India (2014-2024)",
        xaxis_title="Year",
        yaxis_title="Denmark Population (millions)",
        yaxis2=dict(
            title="India Population (millions)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add a bar chart comparing population density
    st.markdown('<div class="section-header">Population Density Comparison</div>', unsafe_allow_html=True)
    
    # Sample data for population density (people per sq km)
    countries = ['Denmark', 'India']
    density = [137, 464]  # People per sq km (2024 estimates)
    
    density_fig = go.Figure(go.Bar(
        x=countries,
        y=density,
        text=density,
        textposition='auto',
        marker_color=['#3B82F6', '#EF4444']
    ))
    
    density_fig.update_layout(
        title="Population Density (People per sq km, 2024)",
        xaxis_title="Country",
        yaxis_title="Density (people per sq km)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(density_fig, use_container_width=True)
    
    # Add population pyramids (simplified version)
    st.markdown('<div class="section-header">Age Distribution Comparison</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sample data for Denmark age distribution (2024 estimate, in percentages)
        dk_age_groups = ['0-14', '15-24', '25-54', '55-64', '65+']
        dk_age_distribution = [16.5, 12.3, 38.4, 12.8, 20.0]
        
        dk_age_fig = go.Figure()
        dk_age_fig.add_trace(go.Bar(
            y=dk_age_groups,
            x=dk_age_distribution,
            orientation='h',
            marker_color='#3B82F6',
            name='Denmark'
        ))
        
        dk_age_fig.update_layout(
            title="Denmark: Age Distribution (%)",
            xaxis_title="Percentage of Population",
            template="plotly_white",
            height=300
        )
        
        st.plotly_chart(dk_age_fig, use_container_width=True)
    
    with col2:
        # Sample data for India age distribution (2024 estimate, in percentages)
        in_age_groups = ['0-14', '15-24', '25-54', '55-64', '65+']
        in_age_distribution = [26.0, 17.2, 41.1, 8.2, 7.5]
        
        in_age_fig = go.Figure()
        in_age_fig.add_trace(go.Bar(
            y=in_age_groups,
            x=in_age_distribution,
            orientation='h',
            marker_color='#EF4444',
            name='India'
        ))
        
        in_age_fig.update_layout(
            title="India: Age Distribution (%)",
            xaxis_title="Percentage of Population",
            template="plotly_white",
            height=300
        )
        
        st.plotly_chart(in_age_fig, use_container_width=True)
    
    # Add insights
    st.markdown('<div class="insight-box">Denmark has a much smaller but older population compared to India. While India\'s population continues to grow at a moderate pace, Denmark\'s population growth is minimal. India\'s significantly higher population density presents different challenges in urban planning, infrastructure development, and resource allocation compared to Denmark.</div>', unsafe_allow_html=True)
    
    # Add a visualization comparing urban vs rural population
    st.markdown('<div class="section-header">Urban vs Rural Population</div>', unsafe_allow_html=True)
    
    # Sample data for urban vs rural (2024 estimate, in percentages)
    labels = ['Urban', 'Rural']
    dk_urban_rural = [88, 12]  # Denmark
    in_urban_rural = [35, 65]  # India
    
    urban_fig = go.Figure()
    
    # Use subplots for comparison
    urban_fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                            subplot_titles=['Denmark', 'India'])
    
    urban_fig.add_trace(go.Pie(
        labels=labels,
        values=dk_urban_rural,
        name='Denmark',
        marker_colors=['#3B82F6', '#93C5FD']
    ), 1, 1)
    
    urban_fig.add_trace(go.Pie(
        labels=labels,
        values=in_urban_rural,
        name='India',
        marker_colors=['#EF4444', '#FCA5A5']
    ), 1, 2)
    
    urban_fig.update_layout(
        title_text="Urban vs Rural Population Distribution (%)",
        height=400
    )
    
    st.plotly_chart(urban_fig, use_container_width=True)
    
    st.markdown('<div class="insight-box">The urbanization patterns reveal stark differences between Denmark and India. Denmark is heavily urbanized with 88% of its population living in urban areas, reflecting its status as a developed economy. In contrast, India remains predominantly rural with only about 35% urban population, though this ratio has been steadily increasing due to ongoing urbanization trends.</div>', unsafe_allow_html=True)
elif section == "References":
    st.markdown('<div class="sub-header">References</div>', unsafe_allow_html=True)

    st.markdown("""
    <ul>
        <li><a href="https://www.census.gov/foreign-trade/balance/c5330.html" target="_blank">US Trade Data</a></li>
        <li><a href="https://www.imf.org/en/Publications/CR/Issues/2023/12/18/India-2023-Article-IV-Consultation-Press-Release-Staff-Report-and-Statement-by-the-542605" target="_blank">IMF India 2023 Article IV Consultation</a></li>
        <li><a href="https://www.imf.org/en/Publications/CR/Issues/2024/09/12/Denmark-2024-Article-IV-Consultation-Press-Release-Staff-Report-and-Statement-by-the-554777" target="_blank">IMF Denmark 2024 Article IV Consultation</a></li>
        <li><a href="https://www.investopedia.com/significant-financial-events-8700894" target="_blank">Significant Financial Events – Investopedia</a></li>
        <li><a href="https://www.imf.org/en/Publications/WEO/weo-database/2024/October" target="_blank">IMF WEO Database – October 2024</a></li>
        <li><a href="https://www.business-standard.com/topic/statsguru" target="_blank">Trump Effect Data – Business Standard (Statsguru), Department of Commerce</a></li>
        <li><a href="https://www.forbesindia.com/article/explainers/unemployment-rate-in-india/87441/1" target="_blank">India Unemployment Data – Forbes India</a></li>
    </ul>
    """, unsafe_allow_html=True)


elif section == "Trump Effect":
    st.markdown('<div class="sub-header">Trump Trade Policies & Global Impact</div>', unsafe_allow_html=True)
    
    # Trump quote with stylized display
    st.markdown("""
    <div class="trump-quote">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg" style="width:75px; border-radius:50%; float:left; margin-right:15px;">
        <div class="quote-text" style="font-size: 35px; font-weight: bold; line-height: 1.6;">
            <p><i>"They (global leaders) are dying to make a deal. I said, we are not going to have deficits with your country. We're going to have surpluses or, at worst, going to be breaking even."</i></p>
        </div>
        <p class="quote-attribution" style="font-size: 18px;  text-align: right;">- President Donald Trump</p>
        <div style="clear:both;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Impact Analysis: Denmark vs. India")
    
    # Tabs for different analysis views
    tab1, tab2, tab3, tab4 = st.tabs(["Trade Balance", "Tariff Vulnerability", "Export Categories", "Economic Resilience"])
    with tab1:
        st.markdown("#### US Trade Balance Comparison")

        # Actual trade data from U.S. database (in billions)
        trade_data = pd.DataFrame({
            'Year': [2019, 2020, 2021, 2022, 2023, 2024],
            'India_Exports': [34.2228, 27.0817, 39.8174, 46.9482, 40.3749, 41.7527],
            'India_Imports': [57.8790, 51.2546, 73.3082, 85.5252, 83.6861, 87.4164],
            'Denmark_Exports': [3.1952, 2.9416, 3.5402, 4.5958, 5.2225, 5.8078],
            'Denmark_Imports': [11.0070, 11.6261, 12.1097, 12.9662, 11.6150, 10.0404]
        })

        # Calculate balances
        trade_data['India_Balance'] = trade_data['India_Exports'] - trade_data['India_Imports']
        trade_data['Denmark_Balance'] = trade_data['Denmark_Exports'] - trade_data['Denmark_Imports']

        # Create the plot
        fig = go.Figure()

        # Add India's trade balance
        fig.add_trace(go.Scatter(
            x=trade_data['Year'],
            y=trade_data['India_Balance'],
            mode='lines+markers',
            name='India Trade Balance',
            line=dict(color='#ff7043', width=3),
            marker=dict(size=10)
        ))

        # Add Denmark's trade balance
        fig.add_trace(go.Scatter(
            x=trade_data['Year'],
            y=trade_data['Denmark_Balance'],
            mode='lines+markers',
            name='Denmark Trade Balance',
            line=dict(color='#5c6bc0', width=3),
            marker=dict(size=10)
        ))

        # Add a reference line at y=0
        fig.add_shape(
            type="line",
            x0=2019,
            y0=0,
            x1=2024,
            y1=0,
            line=dict(color="gray", width=1, dash="dash"),
        )

        # Add a vertical line for Trump's second term
        fig.add_shape(
            type="line",
            x0=2025,
            y0=-10,
            x1=2025,
            y1=10,
            line=dict(color="red", width=2, dash="dot"),
        )

        # Customize layout
        fig.update_layout(
            title='US Trade Balance with India vs Denmark (2019-2024)',
            xaxis_title='Year',
            yaxis_title='Trade Balance (US$ Billions)',
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            annotations=[
                dict(
                    x=2025,
                    y=10,
                    xref="x",
                    yref="y",
                    text="Trump's Second Term",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-40
                )
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

        # Key metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="India's Trade Balance (2024)",
                value=f"${trade_data['India_Balance'].iloc[-1]:.1f}B",
                delta=f"{trade_data['India_Balance'].iloc[-1] - trade_data['India_Balance'].iloc[-2]:.1f}B"
            )

        with col2:
            st.metric(
                label="Denmark's Trade Balance (2024)",
                value=f"${trade_data['Denmark_Balance'].iloc[-1]:.1f}B",
                delta=f"{trade_data['Denmark_Balance'].iloc[-1] - trade_data['Denmark_Balance'].iloc[-2]:.1f}B",
                delta_color="inverse"
            )

    
    with tab2:
        st.markdown("#### Tariff Vulnerability by Sector")
        
        # Create mock data for tariff vulnerability
        sectors = ['Pharmaceuticals', 'Machinery & Equipment', 'Textiles', 'Automotive Components', 'Renewable Energy']
        india_values = [1.5, 6.2, 8.3, 7.9, 4.5]
        denmark_values = [5.8, 8.3, 2.1, 5.5, 9.2]
        
        # Create a dataframe
        tariff_data = pd.DataFrame({
            'Sector': sectors,
            'India': india_values,
            'Denmark': denmark_values
        })
        
        # Create a radar chart
        fig = go.Figure()
        
        # Add India's data
        fig.add_trace(go.Scatterpolar(
            r=india_values + [india_values[0]],
            theta=sectors + [sectors[0]],
            fill='toself',
            name='India',
            line_color='#ff7043',
            fillcolor='rgba(255, 112, 67, 0.3)'
        ))
        
        # Add Denmark's data
        fig.add_trace(go.Scatterpolar(
            r=denmark_values + [denmark_values[0]],
            theta=sectors + [sectors[0]],
            fill='toself',
            name='Denmark',
            line_color='#5c6bc0',
            fillcolor='rgba(92, 107, 192, 0.3)'
        ))
        
        # Update the layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title='Tariff Vulnerability by Sector (Scale: 1-10)',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add an impact analysis table
        st.markdown("##### Impact Severity Assessment")
        
        # Add impact colors
        def color_impact(val):
            if val <= 3:
                return 'background-color: #c8e6c9; color: #1b5e20'  # Green
            elif val <= 6:
                return 'background-color: #fff9c4; color: #f57f17'  # Yellow
            else:
                return 'background-color: #ffcdd2; color: #b71c1c'  # Red
        
        # Display the styled dataframe
        st.dataframe(
            tariff_data.style.applymap(color_impact, subset=['India', 'Denmark']),
            use_container_width=True
        )
        
        st.markdown("""
        <div class="info-box">
            <strong>Impact Scale:</strong>
            <span style="color: #1b5e20">▣ Low (1-3)</span> | 
            <span style="color: #f57f17">▣ Medium (4-6)</span> | 
            <span style="color: #b71c1c">▣ High (7-10)</span>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### Export Category Breakdown")
        
        # Create mock data for export categories
        india_categories = {
            'Category': ['Electrical machinery', 'Gems & jewelry', 'Pharmaceuticals', 'Apparel & clothing', 'Engineering goods'],
            'Percentage': [5.3, 4.7, 3.9, 11.6, 10.3]
        }
        
        denmark_categories = {
            'Category': ['Pharmaceutical products', 'Industrial machinery', 'Renewable energy equipment', 'Medical devices', 'Food products'],
            'Percentage': [28.7, 21.3, 15.5, 8.4, 7.2]
        }
        
        # Create dataframes
        india_df = pd.DataFrame(india_categories)
        denmark_df = pd.DataFrame(denmark_categories)
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### India's Top Export Categories to US")
            fig = px.bar(
                india_df,
                y='Category',
                x='Percentage',
                orientation='h',
                color='Percentage',
                color_continuous_scale='Oranges',
                title="% of India's exports to US"
            )
            fig.update_layout(
                height=400,
                xaxis_title='Percentage (%)',
                yaxis_title='',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Denmark's Top Export Categories to US")
            fig = px.bar(
                denmark_df,
                y='Category',
                x='Percentage',
                orientation='h',
                color='Percentage',
                color_continuous_scale='Blues',
                title="% of Denmark's exports to US"
            )
            fig.update_layout(
                height=400,
                xaxis_title='Percentage (%)',
                yaxis_title='',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # Add explanation text
        st.markdown("""
        <div class="analysis-box">
            <h4>Key Insights:</h4>
            <ul>
                <li>Denmark's exports are concentrated in fewer categories with pharmaceuticals making up nearly 29% of exports</li>
                <li>India shows more diversification with apparel (11.6%) and engineering goods (10.3%) leading</li>
                <li>Denmark's concentration in specific sectors makes it more vulnerable to targeted tariffs</li>
                <li>India's broader export base provides more resilience to sector-specific tariffs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("#### Economic Resilience Comparison")
        
        # Create mock data for economic resilience
        resilience_data = pd.DataFrame({
            'Factor': ['GDP Size', 'Export Diversification', 'Domestic Market Size', 'Industrial Policy Flexibility', 'Currency Flexibility'],
            'India': [8, 7, 9, 7, 6],
            'Denmark': [2, 6, 2, 4, 3]
        })
        
        # Create a horizontal bar chart
        fig = go.Figure()
        
        # Add India's data
        fig.add_trace(go.Bar(
            y=resilience_data['Factor'],
            x=resilience_data['India'],
            name='India',
            orientation='h',
            marker=dict(color='#ff7043')
        ))
        
        # Add Denmark's data
        fig.add_trace(go.Bar(
            y=resilience_data['Factor'],
            x=resilience_data['Denmark'],
            name='Denmark',
            orientation='h',
            marker=dict(color='#5c6bc0')
        ))
        
        # Update the layout
        fig.update_layout(
            title='Economic Resilience Factors (Scale: 1-10)',
            xaxis_title='Score',
            yaxis_title='',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add overall resilience score
        col1, col2 = st.columns(2)
        
        with col1:
            india_score = resilience_data['India'].mean()
            st.markdown(f"""
            <div class="score-box" style="background-color: rgba(255, 112, 67, 0.1); border-left: 4px solid #ff7043; padding: 15px;">
                <h3 style="margin:0; color: #ff7043;">India</h3>
                <div style="font-size: 40px; font-weight: bold;">{india_score:.1f}/10</div>
                <p>High resilience to trade shocks</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            denmark_score = resilience_data['Denmark'].mean()
            st.markdown(f"""
            <div class="score-box" style="background-color: rgba(92, 107, 192, 0.1); border-left: 4px solid #5c6bc0; padding: 15px;">
                <h3 style="margin:0; color: #5c6bc0;">Denmark</h3>
                <div style="font-size: 40px; font-weight: bold;">{denmark_score:.1f}/10</div>
                <p>Lower resilience to trade shocks</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Add analysis text
        st.markdown("""
        <div class="analysis-box">
            <h4>Analysis:</h4>
            <p>India's larger economy, diverse industrial base, and massive domestic market provide significant buffering against external trade shocks. In contrast, Denmark's smaller, open economy with specialized export sectors makes it more vulnerable to targeted trade policies.</p>
            <p>The resilience gap is most pronounced in domestic market size (India: 9 vs Denmark: 2) and GDP size (India: 8 vs Denmark: 2), highlighting the fundamental structural differences between these economies in absorbing trade disruptions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add extra CSS for styling
    st.markdown("""
    <style>
    .trump-quote {
        background-color: #f8f9fa;
        border-left: 4px solid #f1c40f;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
    }
    .quote-text {
        font-style: italic;
        font-size: 16px;
    }
    .quote-attribution {
        text-align: right;
        margin-top: 10px;
        font-weight: bold;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .analysis-box {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .score-box {
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


elif section == "Inflation & Unemployment":
    st.markdown('<div class="sub-header">Inflation & Unemployment</div>', unsafe_allow_html=True)
    st.markdown("Explore inflation and unemployment trends for Denmark and India.")

    # Inflation Chart
    st.markdown('<div class="section-header">Inflation Trends</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'Inflation, average consumer prices',
        'Percent change',
        'Inflation Rate Comparison (2014-2024)',
        'Annual Percent Change (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Inflation insights using direct markdown instead of function
    st.markdown("""
    <div class="insight-box">
        <h4>Inflation Insights</h4>
        <p>Denmark experienced a dramatic inflation spike in 2022 (8.53%), nearly 4x higher than India's historical average.
        India has maintained more consistent inflation (4-6% range) compared to Denmark's volatile pattern.
        Both countries showed inflationary pressures during the post-pandemic recovery period (2021-2022).
        Denmark's inflation has been declining since 2022, returning to more historical norms by 2024.</p>
    </div>
    """, unsafe_allow_html=True)

    # GDP Deflator Chart
    st.markdown('<div class="section-header">GDP Deflator Trends</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'Gross domestic product, deflator',
        'Index',
        'GDP Deflator Comparison (2014-2024)',
        'Index Value'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # GDP Deflator insights using direct markdown
    st.markdown("""
    <div class="insight-box">
        <h4>GDP Deflator Insights</h4>
        <p>India's GDP deflator has shown a steady upward trend, increasing by approximately 47% from 2014 to 2024.
        Denmark's GDP deflator remained relatively stable until 2020, then spiked in 2022 before moderating.
        The 2022 spike in Denmark's deflator (112.12) aligns with its high inflation period.
        The difference in base levels reflects different economic structures and price evolution patterns between the two economies.</p>
    </div>
    """, unsafe_allow_html=True)

    # Unemployment Chart
    st.markdown('<div class="section-header">Unemployment Trends</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'Unemployment rate',
        'Percent of total labor force',
        'Unemployment Rate Comparison (2014-2024)',
        'Percent of Labor Force (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Unemployment insights using direct markdown
    st.markdown("""
    <div class="insight-box">
        <h4>Unemployment Insights</h4>
        <p>Denmark maintains lower unemployment rates than India, reflecting differences in labor market structures.
        Both countries experienced temporary unemployment increases during the pandemic period (2020-2021).
        India's unemployment shows greater volatility, suggesting more sensitivity to economic cycles.
        Denmark's strong social safety net may contribute to its more stable unemployment figures.</p>
    </div>
    """, unsafe_allow_html=True)
elif section == "Trade & Investment":
    st.markdown('<div class="sub-header">Trade & Investment</div>', unsafe_allow_html=True)
    st.markdown("Analyze trade and investment patterns for Denmark and India.")

    # Exports Chart
    st.markdown('<div class="section-header">Exports Trends</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'Volume of exports of goods and services',
        'Percent change',
        'Exports Growth Comparison (2014-2024)',
        'Annual Percent Change (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Exports insights using direct markdown
    st.markdown("""
    <div class="insight-box">
        <h4>Exports Insights</h4>
        <p>Both countries experienced significant export volatility during the pandemic, with sharp contractions in 2020 followed by rebounds.
        India has shown stronger export growth recovery in the post-pandemic period compared to Denmark.
        Denmark's export performance reflects its integration with EU markets and global supply chains.
        India's export growth pattern aligns with its expanding manufacturing base and services sector.</p>
    </div>
    """, unsafe_allow_html=True)

    # Investment Chart
    st.markdown('<div class="section-header">Investment Trends</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'Total investment',
        'Percent of GDP',
        'Investment Trends Comparison (2014-2024)',
        'Percent of GDP (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Investment insights using direct markdown
    st.markdown("""
    <div class="insight-box">
        <h4>Investment Insights</h4>
        <p>India consistently maintains higher investment as a percentage of GDP compared to Denmark, reflecting its developing economy status.
        Denmark's investment levels have remained stable around 20-22% of GDP, typical of mature economies.
        India's higher investment ratio (around 30% of GDP) supports its faster economic growth trajectory.
        Both countries showed resilience in investment levels despite global economic uncertainties.</p>
    </div>
    """, unsafe_allow_html=True)

elif section == "IMF Analysis":
    st.markdown('<div class="sub-header">Comparative IMF Analysis: India vs Denmark</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>1. Economic Growth</h4>
        <p><em>India:</em> 7.2% GDP growth in 2022-23; projected 6.3%. Driven by domestic demand and service exports.</p>
        <p><em>Denmark:</em> 2.5% GDP growth in 2023; projected 1.9% in 2024. Driven by pharmaceutical exports.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>2. Fiscal Policy & Public Debt</h4>
        <p><em>India:</em> Elevated public debt. IMF urges medium-term fiscal consolidation and improved revenue mobilization.</p>
        <p><em>Denmark:</em> Fiscal surplus (3.3% of GDP); low debt (29.7% of GDP). Small fiscal easing advised for health, climate, and defense spending.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>3. Inflation & Monetary Policy</h4>
        <p><em>India:</em> Inflation management is key; RBI maintains a neutral, data-driven policy stance.</p>
        <p><em>Denmark:</em> Inflation near 2%; expected to stay stable. Wages may cause temporary uptick.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>4. Financial Sector Stability</h4>
        <p><em>India:</em> Stable banking sector; strong credit growth. IMF warns of rising unsecured personal loans.</p>
        <p><em>Denmark:</em> Financial system sound, but risks in commercial real estate and high interest rates.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>5. Structural Reforms</h4>
        <p><em>India:</em> Focus on labor reforms, female participation, education, and agriculture to boost inclusive growth.</p>
        <p><em>Denmark:</em> Needs reforms in innovation, digitalization, green transition, and aging workforce issues.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>6. External Sector & Trade</h4>
        <p><em>India:</em> Encouraged to reduce trade restrictions and improve FDI policies.</p>
        <p><em>Denmark:</em> Strong in pharma and shipping. Advised to support multilateral trade systems.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4>7. Long-term Challenges</h4>
        <p><em>India:</em> High debt, employment generation, and structural inefficiencies.</p>
        <p><em>Denmark:</em> Aging population, slow productivity, and real estate risks.</p>
    </div>
    """, unsafe_allow_html=True)



elif section == "Government Finances":
    st.markdown('<div class="sub-header">Government Finances</div>', unsafe_allow_html=True)
    st.markdown("Examine government budget balances and debt levels for Denmark and India.")

    # Budget Balance Chart
    st.markdown('<div class="section-header">Budget Balance</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'General government net lending/borrowing',
        'Percent of GDP',
        'Budget Balance Comparison (2014-2024)',
        'Percent of GDP (%)'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Government Debt Chart
    st.markdown('<div class="section-header">Government Debt</div>', unsafe_allow_html=True)
    fig = create_comparative_line_chart(
        df,
        'General government gross debt',
        'Percent of GDP',
        'Government Debt Comparison (2014-2024)',
        'Percent of GDP (%)'
    )
    st.plotly_chart(fig, use_container_width=True)
elif section == "Correlation Analysis":
    st.markdown('## Correlation Analysis', unsafe_allow_html=True)
    st.markdown("Analyze correlations between key macroeconomic indicators.")
    # Correlation Heatmap for Denmark
    st.markdown('### Denmark Correlation Matrix', unsafe_allow_html=True)
    denmark_corr = calculate_correlations(df, 'Denmark')
    st.dataframe(denmark_corr.style.background_gradient(cmap='viridis'), use_container_width=True)

    # Denmark economic interpretation in styled markdown box
    st.markdown("""
    <div style="padding: 15px; border-radius: 5px; background-color: #f0f7ff; border-left: 5px solid #3366ff;">
        <h4 style="color: #1a53ff; margin-top: 0;">Macroeconomic Insights - Denmark</h4>
        <p><strong>GDP Growth & Trade Relations:</strong></p>
        <ul>
            <li>Denmark shows distinct correlations between GDP growth and trade components (exports/imports)</li>
            <li>Observe how trade openness influences economic growth cycles</li>
        </ul>
        <p><strong>Fiscal Policy & Growth Dynamics:</strong></p>
        <ul>
            <li>Budget balance correlation with GDP reflects fiscal policy transmission effectiveness</li>
            <li>Consider whether government spending appears countercyclical or reinforces existing cycles</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Correlation Heatmap for India
    st.markdown('### India Correlation Matrix', unsafe_allow_html=True)
    india_corr = calculate_correlations(df, 'India')
    st.dataframe(india_corr.style.background_gradient(cmap='viridis'), use_container_width=True)

    # India economic interpretation in styled markdown box
    st.markdown("""
    <div style="padding: 15px; border-radius: 5px; background-color: #f0f7ff; border-left: 5px solid #3366ff;">
        <h4 style="color: #1a53ff; margin-top: 0;">Macroeconomic Insights - India</h4>
        <p><strong>GDP Growth & Trade Relations:</strong></p>
        <ul>
            <li>Examine how export/import correlations with GDP showcase India's global trade integration</li>
            <li>Note the implications of trade patterns on domestic economic performance</li>
        </ul>
        <p><strong>Fiscal Policy & Growth Dynamics:</strong></p>
        <ul>
            <li>Budget balance correlation reveals how government fiscal positions influence growth trajectory</li>
            <li>Evaluate the relationship between public spending and economic development stages</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif section == "Macroeconomic Events":
    st.markdown('<div class="sub-header">Macroeconomic Events</div>', unsafe_allow_html=True)
    st.markdown("### Economic Timeline: 2014-2024")
    
    # Add custom CSS for timeline styling
    st.markdown("""
    <style>
    .timeline-container {
        margin: 20px 0;
        position: relative;
        width: 100%;
    }
    .timeline-card {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .timeline-year {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
        color: #1E3A8A;
    }
    .event-global {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
    }
    .event-india {
        background-color: #FFEDD5;
        border-left: 4px solid #F97316;
    }
    .event-denmark {
        background-color: #F0FDF4;
        border-left: 4px solid #10B981;
    }
    .event-title {
        font-weight: bold;
        color: #4B5563;
    }
    </style>
    """, unsafe_allow_html=True)

    
    
    # Create color map for regions
    color_map = {"Global": "#3B82F6", "India": "#F97316", "Denmark": "#10B981"}
    

    
    # Add a time slider for filtering events by year range

    filtered_events = economic_events
    for year in sorted(filtered_events.keys()):
        with st.expander(f"**{year}**", expanded=True):
            for region, event in filtered_events[year].items():
                region_class = f"event-{region.lower()}"
                st.markdown(f"""
                <div class="timeline-card {region_class}">
                    <div class="event-title">{region}</div>
                    {event}
                </div>
                """, unsafe_allow_html=True)
    
