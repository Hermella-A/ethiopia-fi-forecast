"""
Ethiopia Financial Inclusion Dashboard
Streamlit Application for Task 5
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
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
        color: #1a2a6c;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 4px solid #1a2a6c;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a2a6c;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 5px;
    }
    .insight-box {
        background-color: #e8f4fd;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 0.8rem;
        border-top: 1px solid #eee;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data
def load_data():
    """Load all required data."""
    try:
        df = pd.read_csv('data/processed/ethiopia_fi_enriched.csv', parse_dates=['observation_date'])
        observations = df[df['record_type'] == 'observation']
        events = df[df['record_type'] == 'event']
        impact_links = df[df['record_type'] == 'impact_link']
        targets = df[df['record_type'] == 'target']
        return df, observations, events, impact_links, targets
    except FileNotFoundError:
        # Try alternative path if running from different directory
        df = pd.read_csv('../data/processed/ethiopia_fi_enriched.csv', parse_dates=['observation_date'])
        observations = df[df['record_type'] == 'observation']
        events = df[df['record_type'] == 'event']
        impact_links = df[df['record_type'] == 'impact_link']
        targets = df[df['record_type'] == 'target']
        return df, observations, events, impact_links, targets

@st.cache_data
def load_forecasts():
    """Load forecast data."""
    try:
        forecast_df = pd.read_csv('data/processed/forecasts_2025_2027.csv')
        return forecast_df
    except FileNotFoundError:
        try:
            forecast_df = pd.read_csv('../data/processed/forecasts_2025_2027.csv')
            return forecast_df
        except FileNotFoundError:
            # Create sample forecast data if file not found
            st.warning("Forecast file not found. Using sample data for demonstration.")
            return create_sample_forecasts()

def create_sample_forecasts():
    """Create sample forecast data for demonstration."""
    data = []
    targets = ['ACCESS', 'USAGE']
    scenarios = ['Optimistic', 'Base', 'Pessimistic']
    years = [2025, 2026, 2027]
    
    # Access forecast values
    access_values = {
        'Optimistic': [55, 57, 60],
        'Base': [52, 54, 56],
        'Pessimistic': [48, 49, 51]
    }
    
    # Usage forecast values
    usage_values = {
        'Optimistic': [42, 45, 48],
        'Base': [38, 40, 42],
        'Pessimistic': [34, 35, 37]
    }
    
    for target, values_dict in [('ACCESS', access_values), ('USAGE', usage_values)]:
        for scenario in scenarios:
            for i, year in enumerate(years):
                data.append({
                    'Target': target,
                    'Scenario': scenario,
                    'Year': year,
                    'Forecast (%)': values_dict[scenario][i],
                    'Lower Bound': values_dict[scenario][i] - 3,
                    'Upper Bound': values_dict[scenario][i] + 3
                })
    
    return pd.DataFrame(data)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_values(observations):
    """Get current (most recent) values for key indicators."""
    current = {}
    
    # Account ownership
    acc = observations[observations['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date')
    if len(acc) > 0:
        current['account_ownership'] = acc.iloc[-1]['value_numeric']
        current['account_ownership_date'] = acc.iloc[-1]['observation_date']
    
    # Mobile money account
    mm = observations[observations['indicator_code'] == 'ACC_MM_ACCOUNT'].sort_values('observation_date')
    if len(mm) > 0:
        current['mm_account'] = mm.iloc[-1]['value_numeric']
    
    # Digital payments - try multiple codes
    for code in ['USG_DIGITAL_PAYMENTS', 'USG_P2P_COUNT', 'USG_TELEBIRR_USERS']:
        dp = observations[observations['indicator_code'] == code].sort_values('observation_date')
        if len(dp) > 0:
            current['digital_payments'] = dp.iloc[-1]['value_numeric']
            break
    
    return current

def calculate_growth(observations, indicator_code, years_back=2):
    """Calculate growth rate for an indicator over the last N observations."""
    data = observations[observations['indicator_code'] == indicator_code].sort_values('observation_date')
    if len(data) < 2:
        return None
    old_val = data.iloc[-2]['value_numeric']
    new_val = data.iloc[-1]['value_numeric']
    growth = ((new_val - old_val) / old_val) * 100
    return growth

# ============================================================
# PAGE FUNCTIONS
# ============================================================

def page_overview(df, observations, events, impact_links, targets):
    """Overview page with key metrics and summary."""
    
    st.markdown('<p class="main-header">📊 Overview Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ethiopia Financial Inclusion - Key Metrics and Summary</p>', unsafe_allow_html=True)
    
    # Get current values
    current = get_current_values(observations)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{current.get('account_ownership', 'N/A')}%</div>
            <div class="metric-label">Account Ownership Rate (2024)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{current.get('mm_account', 'N/A')}%</div>
            <div class="metric-label">Mobile Money Account (2024)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{current.get('digital_payments', 'N/A')}%</div>
            <div class="metric-label">Digital Payment Adoption</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate growth
        growth = calculate_growth(observations, 'ACC_OWNERSHIP')
        if growth:
            color = "green" if growth > 0 else "red"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:{color};">{growth:+.1f}%</div>
                <div class="metric-label">Growth Rate (last period)</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">N/A</div>
                <div class="metric-label">Growth Rate (last period)</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Two columns: Data quality and Event summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Data Summary")
        st.write(f"**Total Records:** {len(df)}")
        st.write(f"**Observations:** {len(observations)}")
        st.write(f"**Events:** {len(events)}")
        st.write(f"**Impact Links:** {len(impact_links)}")
        st.write(f"**Targets:** {len(targets)}")
        
        # Record types breakdown
        record_counts = df['record_type'].value_counts().reset_index()
        record_counts.columns = ['Record Type', 'Count']
        st.dataframe(record_counts, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📌 Key Events")
        events_sorted = events.sort_values('observation_date')
        # Show last 5 events
        for _, row in events_sorted.tail(5).iterrows():
            st.write(f"**{row['observation_date'].strftime('%Y-%m-%d')}** — {row['indicator']}")
            st.caption(f"Category: {row['category']}")
    
    st.divider()
    
    # Insights section
    st.subheader("💡 Key Insights")
    
    insights = [
        "Account ownership has grown from 14% (2011) to 49% (2024), but growth slowed to +3pp between 2021-2024.",
        "Mobile money accounts reached 9.45% in 2024, up from 4.7% in 2021.",
        "Only ~0.5% of adults are mobile money-only users, indicating bank accounts remain primary.",
        "Digital payment adoption lags behind account ownership, suggesting a usage gap."
    ]
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">💡 {insight}</div>', unsafe_allow_html=True)

def page_trends(observations, events):
    """Trends page with interactive time series plots."""
    
    st.markdown('<p class="main-header">📈 Trends Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore historical trends in financial inclusion indicators</p>', unsafe_allow_html=True)
    
    # Get available indicators
    indicators = observations['indicator_code'].unique()
    indicator_names = observations.groupby('indicator_code')['indicator'].first().to_dict()
    
    # Sidebar filters
    st.sidebar.subheader("🔍 Filters")
    
    selected_indicators = st.sidebar.multiselect(
        "Select Indicators to Display",
        options=indicators,
        default=indicators[:3] if len(indicators) >= 3 else indicators,
        format_func=lambda x: indicator_names.get(x, x)
    )
    
    # Date range
    min_date = observations['observation_date'].min()
    max_date = observations['observation_date'].max()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Show events overlay
    show_events = st.sidebar.checkbox("Show Events", value=True)
    
    # Filter data by date
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = observations[
            (observations['observation_date'] >= pd.to_datetime(start_date)) &
            (observations['observation_date'] <= pd.to_datetime(end_date))
        ]
    else:
        filtered_data = observations
    
    # Create plot
    if selected_indicators:
        fig = go.Figure()
        
        colors = ['#1a2a6c', '#b21f1f', '#fdbb2d', '#2e7d32', '#9c27b0', '#1976d2']
        
        for i, indicator in enumerate(selected_indicators):
            data = filtered_data[filtered_data['indicator_code'] == indicator].sort_values('observation_date')
            if len(data) > 0:
                color = colors[i % len(colors)]
                fig.add_trace(go.Scatter(
                    x=data['observation_date'],
                    y=data['value_numeric'],
                    mode='lines+markers',
                    name=indicator_names.get(indicator, indicator),
                    line=dict(color=color, width=2),
                    marker=dict(size=8, color=color)
                ))
        
        # Add events as vertical lines
        if show_events:
            events_filtered = events[
                (events['observation_date'] >= pd.to_datetime(start_date)) &
                (events['observation_date'] <= pd.to_datetime(end_date))
            ] if len(date_range) == 2 else events
            
            for _, event in events_filtered.iterrows():
                fig.add_vline(
                    x=event['observation_date'],
                    line_dash="dash",
                    line_color="red",
                    opacity=0.5,
                    annotation_text=event['indicator'][:20],
                    annotation_position="top right",
                    annotation_font_size=8
                )
        
        fig.update_layout(
            title="Financial Inclusion Indicators Over Time",
            xaxis_title="Date",
            yaxis_title="Value (%)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        with st.expander("📋 View Data Table"):
            display_data = filtered_data[filtered_data['indicator_code'].isin(selected_indicators)]
            display_data = display_data[['observation_date', 'indicator_code', 'value_numeric', 'confidence']]
            display_data = display_data.rename(columns={
                'observation_date': 'Date',
                'indicator_code': 'Indicator',
                'value_numeric': 'Value (%)',
                'confidence': 'Confidence'
            })
            st.dataframe(display_data, use_container_width=True, hide_index=True)
            
            # Download button
            csv = display_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Data as CSV",
                data=csv,
                file_name="financial_inclusion_trends.csv",
                mime="text/csv"
            )
    else:
        st.warning("Please select at least one indicator to display.")

def page_forecasts(forecast_df):
    """Forecasts page with visualizations and projections."""
    
    st.markdown('<p class="main-header">🔮 Forecasts 2025-2027</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Projections for Account Ownership and Digital Payment Usage</p>', unsafe_allow_html=True)
    
    if forecast_df is None or len(forecast_df) == 0:
        st.warning("No forecast data available. Please run the forecasting model first.")
        return
    
    # Sidebar filters
    st.sidebar.subheader("📊 Forecast Controls")
    
    target_options = forecast_df['Target'].unique()
    selected_target = st.sidebar.selectbox("Select Target", target_options)
    
    scenario_options = forecast_df['Scenario'].unique()
    selected_scenarios = st.sidebar.multiselect(
        "Select Scenarios",
        scenario_options,
        default=scenario_options
    )
    
    # Filter data
    filtered_forecast = forecast_df[
        (forecast_df['Target'] == selected_target) &
        (forecast_df['Scenario'].isin(selected_scenarios))
    ]
    
    if len(filtered_forecast) == 0:
        st.warning("No data for selected filters.")
        return
    
    # Forecast chart
    fig = go.Figure()
    
    colors = {'Optimistic': '#2e7d32', 'Base': '#1a2a6c', 'Pessimistic': '#b21f1f'}
    
    for scenario in selected_scenarios:
        data = filtered_forecast[filtered_forecast['Scenario'] == scenario]
        data = data.sort_values('Year')
        
        color = colors.get(scenario, '#666')
        
        fig.add_trace(go.Scatter(
            x=data['Year'],
            y=data['Forecast (%)'],
            mode='lines+markers',
            name=f"{scenario}",
            line=dict(color=color, width=3),
            marker=dict(size=10, color=color)
        ))
        
        # Add confidence intervals
        fig.add_trace(go.Scatter(
            x=data['Year'].tolist() + data['Year'].tolist()[::-1],
            y=data['Upper Bound'].tolist() + data['Lower Bound'].tolist()[::-1],
            fill='toself',
            fillcolor=color,
            opacity=0.2,
            line=dict(width=0),
            name=f"{scenario} (CI)",
            hoverinfo='skip',
            showlegend=False
        ))
    
    fig.update_layout(
        title=f"{selected_target} Forecast (2025-2027)",
        xaxis_title="Year",
        yaxis_title="Percentage of Adults (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast table
    st.subheader("📋 Forecast Table")
    
    pivot_table = filtered_forecast.pivot_table(
        index=['Scenario'],
        columns='Year',
        values='Forecast (%)'
    ).round(1)
    
    st.dataframe(pivot_table, use_container_width=True)
    
    # Download forecast data
    csv = filtered_forecast.to_csv(index=False)
    st.download_button(
        label="📥 Download Forecast as CSV",
        data=csv,
        file_name=f"forecast_{selected_target}_2025_2027.csv",
        mime="text/csv"
    )
    
    # Key milestones
    st.subheader("🎯 Key Projected Milestones")
    
    for scenario in selected_scenarios:
        data = filtered_forecast[filtered_forecast['Scenario'] == scenario].sort_values('Year')
        if len(data) > 0:
            st.markdown(f"**{scenario} Scenario:**")
            for _, row in data.iterrows():
                st.write(f"  • {row['Year']}: {row['Forecast (%)']:.1f}% (Range: {row['Lower Bound']:.1f}% - {row['Upper Bound']:.1f}%)")

def page_projections(observations, forecast_df):
    """Inclusion Projections page with scenario selector and target visualization."""
    
    st.markdown('<p class="main-header">🎯 Inclusion Projections</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Progress toward 60% target and scenario analysis</p>', unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.subheader("🎯 Projection Controls")
    
    target = st.sidebar.selectbox(
        "Select Target",
        ['Account Ownership', 'Digital Payment Usage']
    )
    
    scenario = st.sidebar.selectbox(
        "Select Scenario",
        ['Optimistic', 'Base', 'Pessimistic']
    )
    
    # Get historical data
    if target == 'Account Ownership':
        indicator_code = 'ACC_OWNERSHIP'
    else:
        indicator_code = 'USG_DIGITAL_PAYMENTS'
    
    historical = observations[observations['indicator_code'] == indicator_code].sort_values('observation_date')
    
    # Get forecast data
    if forecast_df is not None and len(forecast_df) > 0:
        forecast_target = 'ACCESS' if target == 'Account Ownership' else 'USAGE'
        forecast_data = forecast_df[
            (forecast_df['Target'] == forecast_target) &
            (forecast_df['Scenario'] == scenario)
        ].sort_values('Year')
    else:
        forecast_data = pd.DataFrame()
    
    # Create projection chart
    fig = go.Figure()
    
    # Historical data
    if len(historical) > 0:
        fig.add_trace(go.Scatter(
            x=historical['observation_date'],
            y=historical['value_numeric'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#1a2a6c', width=3),
            marker=dict(size=10, color='#1a2a6c')
        ))
    
    # Forecast data
    if len(forecast_data) > 0:
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(forecast_data['Year'].astype(str) + '-07-01'),
            y=forecast_data['Forecast (%)'],
            mode='lines+markers',
            name=f'Forecast ({scenario})',
            line=dict(color='#fdbb2d', width=3, dash='dash'),
            marker=dict(size=12, color='#fdbb2d')
        ))
        
        # Confidence intervals
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(forecast_data['Year'].astype(str) + '-07-01').tolist() + 
              pd.to_datetime(forecast_data['Year'].astype(str) + '-07-01').tolist()[::-1],
            y=forecast_data['Upper Bound'].tolist() + forecast_data['Lower Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='#fdbb2d',
            opacity=0.2,
            line=dict(width=0),
            name='Confidence Interval',
            hoverinfo='skip'
        ))
    
    # 60% target line
    fig.add_hline(
        y=60,
        line_dash="dot",
        line_color="green",
        line_width=2,
        annotation_text="60% Target (NFIS-II)",
        annotation_position="bottom right"
    )
    
    fig.update_layout(
        title=f"{target} - Historical and Projected ({scenario} Scenario)",
        xaxis_title="Year",
        yaxis_title="Percentage of Adults (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress toward target
    st.subheader("📊 Progress Toward 60% Target")
    
    if len(forecast_data) > 0:
        last_historical = historical.iloc[-1]['value_numeric'] if len(historical) > 0 else 0
        target_2027 = forecast_data[forecast_data['Year'] == 2027]['Forecast (%)'].values[0] if 2027 in forecast_data['Year'].values else None
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current (2024)", f"{last_historical:.1f}%")
        
        with col2:
            if target_2027:
                st.metric("Projected 2027", f"{target_2027:.1f}%", 
                         delta=f"{target_2027 - last_historical:.1f}pp" if last_historical else None)
            else:
                st.metric("Projected 2027", "N/A")
        
        with col3:
            if target_2027:
                gap = 60 - target_2027
                st.metric("Gap to 60% Target", f"{gap:.1f}pp" if gap > 0 else "Target Met! 🎉")
            else:
                st.metric("Gap to 60% Target", "N/A")
    
    # Policy recommendations
    st.subheader("💡 Policy Recommendations")
    
    recommendations = [
        "**Accelerate Digital ID Rollout:** Expanding Fayda digital ID coverage can enable simplified KYC and boost account ownership.",
        "**Enhance Agent Networks:** Increasing agent density (currently 45 per 100k adults) can improve access in rural areas.",
        "**Promote Digital Payment Use Cases:** Moving beyond P2P transfers to merchant payments, bill pay, and wage disbursements.",
        "**Address Gender Gap:** Targeted programs to increase women's financial inclusion can close the gender gap.",
        "**Interoperability Expansion:** Full interoperability between mobile money providers can drive usage."
    ]
    
    for rec in recommendations:
        st.markdown(f'<div class="insight-box">💡 {rec}</div>', unsafe_allow_html=True)

# ============================================================
# MAIN APP
# ============================================================

def main():
    """Main application entry point."""
    
    # Load data
    try:
        df, observations, events, impact_links, targets = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
    
    # Load forecasts
    forecast_df = load_forecasts()
    
    # Sidebar navigation
    st.sidebar.image("https://img.icons8.com/color/96/000000/ethiopia.png", width=80)
    st.sidebar.title("Navigation")
    
    pages = {
        "📊 Overview": page_overview,
        "📈 Trends": page_trends,
        "🔮 Forecasts": page_forecasts,
        "🎯 Projections": page_projections
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    # Render selected page
    if selection == "📊 Overview":
        pages[selection](df, observations, events, impact_links, targets)
    elif selection == "📈 Trends":
        pages[selection](observations, events)
    elif selection == "🔮 Forecasts":
        pages[selection](forecast_df)
    elif selection == "🎯 Projections":
        pages[selection](observations, forecast_df)
    
    # Footer
    st.markdown('<div class="footer">Ethiopia Financial Inclusion Dashboard | Week 11 Challenge | Birhan Energies</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 