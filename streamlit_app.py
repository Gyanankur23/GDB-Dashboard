"""
GDP Dashboard - A Streamlit app showing GDP of different countries.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="GDP Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Title
st.title("🌍 World GDP Dashboard")
st.markdown("Explore GDP data for countries around the world.")

# Load sample GDP data
@st.cache_data
def load_data():
    """Load sample GDP data."""
    data = {
        'Country': ['United States', 'China', 'Japan', 'Germany', 'India', 
                    'United Kingdom', 'France', 'Italy', 'Brazil', 'Canada',
                    'Russia', 'South Korea', 'Spain', 'Australia', 'Mexico'],
        'GDP (Trillion USD)': [26.95, 17.70, 4.23, 4.43, 3.73,
                               3.33, 3.05, 2.25, 2.13, 2.12,
                               1.86, 1.71, 1.58, 1.55, 1.81],
        'GDP Per Capita (USD)': [80835, 12541, 33815, 52824, 2612,
                                 48912, 44508, 38146, 10079, 54966,
                                 12993, 33192, 33091, 59934, 13980],
        'Continent': ['North America', 'Asia', 'Asia', 'Europe', 'Asia',
                      'Europe', 'Europe', 'Europe', 'South America', 'North America',
                      'Europe', 'Asia', 'Europe', 'Oceania', 'North America'],
        'Growth Rate (%)': [2.5, 5.2, 1.9, 1.8, 6.3,
                           3.6, 2.6, 3.7, 2.9, 3.4,
                           3.0, 3.1, 4.2, 3.6, 3.2]
    }
    return pd.DataFrame(data)

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("📊 Filters")

# Continent filter
continents = ['All'] + sorted(df['Continent'].unique().tolist())
selected_continent = st.sidebar.selectbox("Select Continent:", continents)

# Filter data
if selected_continent != 'All':
    df_filtered = df[df['Continent'] == selected_continent]
else:
    df_filtered = df

# Top N slider
top_n = st.sidebar.slider("Top N Countries:", 3, 15, 10)

# Sort by GDP
df_filtered = df_filtered.nlargest(top_n, 'GDP (Trillion USD)')

# Main content - Metrics
st.subheader("📈 Key Metrics")

# Display metrics
metrics = st.columns(4)
metrics[0].metric("Total Countries", len(df_filtered))
metrics[1].metric("Total GDP", f"${df_filtered['GDP (Trillion USD)'].sum():.2f}T")
metrics[2].metric("Avg GDP Per Capita", f"${df_filtered['GDP Per Capita (USD)'].mean():,.0f}")
metrics[3].metric("Avg Growth Rate", f"{df_filtered['Growth Rate (%)'].mean():.1f}%")

st.divider()

# Charts
st.subheader("📊 Visualizations")

# Create columns for charts
chart_col1, chart_col2 = st.columns(2)

# Bar chart - GDP by Country
with chart_col1:
    fig = px.bar(
        df_filtered,
        x='Country',
        y='GDP (Trillion USD)',
        title=f'GDP by Country ({selected_continent})',
        color='GDP (Trillion USD)',
        color_continuous_scale='Blues'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Pie chart - GDP distribution by continent
with chart_col2:
    if selected_continent == 'All':
        continent_gdp = df.groupby('Continent')['GDP (Trillion USD)'].sum().reset_index()
        fig2 = px.pie(
            continent_gdp,
            values='GDP (Trillion USD)',
            names='Continent',
            title='GDP Distribution by Continent',
            hole=0.3
        )
    else:
        fig2 = px.bar(
            df_filtered,
            x='Country',
            y='Growth Rate (%)',
            title='Growth Rate by Country',
            color='Growth Rate (%)',
            color_continuous_scale='Greens'
        )
        fig2.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig2, use_container_width=True)

# Scatter plot
st.subheader("🔍 GDP vs GDP Per Capita")
fig3 = px.scatter(
    df_filtered,
    x='GDP Per Capita (USD)',
    y='GDP (Trillion USD)',
    size='Growth Rate (%)',
    color='Continent',
    hover_name='Country',
    title='GDP vs GDP Per Capita (bubble size = Growth Rate)',
    size_max=40
)
st.plotly_chart(fig3, use_container_width=True)

# Data table
st.subheader("📋 Data Table")
st.dataframe(
    df_filtered.sort_values('GDP (Trillion USD)', ascending=False),
    use_container_width=True,
    hide_index=True
)

# Download button
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name=f'gdp_data_{selected_continent.lower().replace(" ", "_")}.csv',
    mime='text/csv'
)

# Footer
st.divider()
st.markdown("Built with ❤️ using Streamlit, Plotly & Pandas")
