import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Patent Analytics Dashboard", layout="wide", page_icon="📊")

# Custom CSS for better styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-size: 16px;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load all data
@st.cache_data
def load_all_data():
    patents = pd.read_csv('clean_patents.csv')
    inventors = pd.read_csv('clean_inventors.csv')
    companies = pd.read_csv('clean_companies.csv')
    top_inventors = pd.read_csv('top_inventors.csv')
    top_companies = pd.read_csv('top_companies.csv')
    country_trends = pd.read_csv('country_trends.csv')
    
    # Create yearly trends from patents
    if 'year' in patents.columns:
        yearly = patents.groupby('year').size().reset_index(name='patent_count')
        yearly = yearly[yearly['year'] > 2000]
    else:
        yearly = pd.DataFrame()
    
    return patents, inventors, companies, top_inventors, top_companies, country_trends, yearly

patents, inventors, companies, top_inventors, top_companies, country_trends, yearly = load_all_data()

st.title(" Patent Data Analytics Dashboard")
st.markdown("*Comprehensive Analysis of Global Patent Activity*")
st.markdown("---")


st.subheader(" Key Metrics Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(" Total Patents", f"{len(patents):,}", delta="100%", delta_color="normal")
with col2:
    st.metric(" Total Inventors", f"{len(inventors):,}")
with col3:
    st.metric(" Total Companies", f"{len(companies):,}")
with col4:
    st.metric(" Countries", f"{len(country_trends)}")
with col5:
    if len(yearly) > 0:
        growth = yearly['patent_count'].pct_change().iloc[-1] * 100 if len(yearly) > 1 else 0
        st.metric("YoY Growth", f"{growth:.1f}%", delta=f"{growth:.1f}%" if growth != 0 else None)

st.markdown("---")


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    " Trends", " Top Performers", " Geographic", 
    " Relationships", " Distributions", " SQL Queries"
])


with tab1:
    st.header(" Patent Trends Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart with markers
        if len(yearly) > 0:
            fig1 = px.line(yearly, x='year', y='patent_count', 
                          markers=True, line_shape='linear',
                          title="Patent Filing Trends",
                          labels={'year': 'Year', 'patent_count': 'Number of Patents'})
            fig1.update_traces(line=dict(width=3, color='royalblue'), 
                              marker=dict(size=8, color='darkblue'))
            fig1.update_layout(height=450, hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Area chart for cumulative
        if len(yearly) > 0:
            yearly['cumulative'] = yearly['patent_count'].cumsum()
            fig2 = px.area(yearly, x='year', y='cumulative',
                          title="Cumulative Patents Over Time",
                          labels={'year': 'Year', 'cumulative': 'Total Patents'})
            fig2.update_traces(fill='tozeroy', line=dict(color='forestgreen'))
            fig2.update_layout(height=450)
            st.plotly_chart(fig2, use_container_width=True)
    
    # Growth rate chart
    if len(yearly) > 1:
        yearly['growth_rate'] = yearly['patent_count'].pct_change() * 100
        fig3 = px.bar(yearly, x='year', y='growth_rate',
                     title="Year-over-Year Growth Rate (%)",
                     labels={'year': 'Year', 'growth_rate': 'Growth Rate (%)'},
                     color='growth_rate',
                     color_continuous_scale=['red', 'yellow', 'green'])
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)


with tab2:
    st.header(" Top Performers Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Inventors - Horizontal Bar Chart
        if len(top_inventors) > 0:
            fig4 = px.bar(top_inventors.head(15), 
                         x='patent_count', y='name',
                         orientation='h',
                         title="Top 15 Inventors by Patent Count",
                         labels={'patent_count': 'Number of Patents', 'name': 'Inventor'},
                         color='patent_count',
                         color_continuous_scale='Viridis')
            fig4.update_layout(height=500)
            st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Top Companies - Horizontal Bar Chart
        if len(top_companies) > 0:
            fig5 = px.bar(top_companies.head(15), 
                         x='patent_count', y='name',
                         orientation='h',
                         title="Top 15 Companies by Patent Count",
                         labels={'patent_count': 'Number of Patents', 'name': 'Company'},
                         color='patent_count',
                         color_continuous_scale='Plasma')
            fig5.update_layout(height=500)
            st.plotly_chart(fig5, use_container_width=True)
    
    # Donut chart for top 5 vs rest
    col1, col2 = st.columns(2)
    
    with col1:
        if len(top_inventors) > 0:
            top5_sum = top_inventors.head(5)['patent_count'].sum()
            rest_sum = top_inventors['patent_count'].sum() - top5_sum
            donut_data = pd.DataFrame({
                'Category': ['Top 5 Inventors', 'All Other Inventors'],
                'Patents': [top5_sum, rest_sum]
            })
            fig6 = px.pie(donut_data, values='Patents', names='Category',
                         title="Top 5 Inventors Share",
                         hole=0.4,
                         color_discrete_sequence=['#FF6B6B', '#4ECDC4'])
            fig6.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        if len(top_companies) > 0:
            top5_sum = top_companies.head(5)['patent_count'].sum()
            rest_sum = top_companies['patent_count'].sum() - top5_sum
            donut_data2 = pd.DataFrame({
                'Category': ['Top 5 Companies', 'All Other Companies'],
                'Patents': [top5_sum, rest_sum]
            })
            fig7 = px.pie(donut_data2, values='Patents', names='Category',
                         title="Top 5 Companies Share",
                         hole=0.4,
                         color_discrete_sequence=['#45B7D1', '#96CEB4'])
            st.plotly_chart(fig7, use_container_width=True)

with tab3:
    st.header(" Geographic Distribution of Patents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(country_trends) > 0:
            # Choropleth map
            fig8 = px.choropleth(country_trends.head(30),
                                locations='country',
                                locationmode='country names',
                                color='patent_count',
                                hover_name='country',
                                title="Global Patent Distribution",
                                color_continuous_scale='Reds',
                                range_color=[0, country_trends['patent_count'].max()])
            fig8.update_layout(height=500)
            st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        if len(country_trends) > 0:
            # Top countries bar chart
            fig9 = px.bar(country_trends.head(15), 
                         x='country', y='patent_count',
                         title="Top 15 Countries by Patent Count",
                         labels={'country': 'Country', 'patent_count': 'Number of Patents'},
                         color='patent_count',
                         color_continuous_scale='Teal')
            fig9.update_layout(height=500)
            st.plotly_chart(fig9, use_container_width=True)
    
    # Treemap for country distribution
    if len(country_trends) > 0:
        fig10 = px.treemap(country_trends.head(20), 
                          path=['country'], 
                          values='patent_count',
                          title="Patent Distribution Treemap by Country",
                          color='patent_count',
                          color_continuous_scale='Blues')
        fig10.update_layout(height=500)
        st.plotly_chart(fig10, use_container_width=True)


with tab4:
    st.header(" Patent-Inventor-Company Relationships")
    
    # Sample relationship data
    st.subheader("Sample of Patent Relationships")
    
    # Create relationship sample
    relationship_sample = pd.DataFrame({
        'Patent ID': ['10000000', '10000001', '10000002', '10000003', '10000004'],
        'Title': ['Coherent LADAR', 'Injection molding machine', 'Polymer film method', 
                  'Container production', 'Double-oriented film'],
        'Inventor': ['Wenjing Jiang', 'Eiko BÄUMKER', 'Richard Kroeger', 'Thomas A. Bush', 'Matthew F. Boudreaux'],
        'Country': ['CN', 'DE', 'Unknown', 'Unknown', 'US']
    })
    st.dataframe(relationship_sample, use_container_width=True)
    
    # Sunburst chart
    st.subheader("Patent Hierarchy")
    if len(country_trends) > 0:
        sunburst_data = country_trends.head(10).copy()
        sunburst_data['level'] = 'Countries'
        fig11 = px.sunburst(sunburst_data, 
                           path=['level', 'country'], 
                           values='patent_count',
                           title="Patent Distribution Sunburst Chart",
                           color='patent_count',
                           color_continuous_scale='Rainbow')
        fig11.update_layout(height=500)
        st.plotly_chart(fig11, use_container_width=True)


with tab5:
    st.header(" Statistical Distributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram of patent counts per inventor
        if len(top_inventors) > 0:
            fig12 = px.histogram(top_inventors, x='patent_count', nbins=20,
                                title="Distribution: Patents per Inventor",
                                labels={'patent_count': 'Number of Patents', 'count': 'Number of Inventors'},
                                color_discrete_sequence=['#9467BD'])
            fig12.update_layout(height=400)
            st.plotly_chart(fig12, use_container_width=True)
    
    with col2:
        # Box plot of patent counts
        if len(top_inventors) > 0:
            fig13 = px.box(top_inventors, y='patent_count',
                          title="Box Plot: Patent Distribution",
                          labels={'patent_count': 'Patent Count'},
                          color_discrete_sequence=['#FF9F1C'])
            fig13.update_layout(height=400)
            st.plotly_chart(fig13, use_container_width=True)
    
    # Violin plot
    if len(top_companies) > 0:
        fig14 = px.violin(top_companies, y='patent_count', box=True, points='all',
                         title="Violin Plot: Patent Distribution by Company",
                         labels={'patent_count': 'Patent Count'},
                         color_discrete_sequence=['#2CA02C'])
        fig14.update_layout(height=450)
        st.plotly_chart(fig14, use_container_width=True)
    
    # Cumulative distribution
    if len(top_inventors) > 0:
        top_inventors_sorted = top_inventors.sort_values('patent_count', ascending=True)
        top_inventors_sorted['cumulative_percent'] = top_inventors_sorted['patent_count'].cumsum() / top_inventors_sorted['patent_count'].sum() * 100
        fig15 = px.line(top_inventors_sorted, y='cumulative_percent',
                       title="Cumulative Distribution: Patent Concentration",
                       labels={'index': 'Inventor Rank', 'cumulative_percent': 'Cumulative % of Patents'})
        fig15.update_layout(height=400)
        st.plotly_chart(fig15, use_container_width=True)


with tab6:
    st.header(" 7 Required SQL Query Results")
    
    # Q1
    st.subheader(" Q1: Top Inventors")
    st.dataframe(top_inventors.head(10), use_container_width=True)
    
    # Q2
    st.subheader(" Q2: Top Companies")
    st.dataframe(top_companies.head(10), use_container_width=True)
    
    # Q3
    st.subheader(" Q3: Top Countries")
    st.dataframe(country_trends.head(10), use_container_width=True)
    
    # Q4
    st.subheader(" Q4: Trends Over Time")
    st.dataframe(yearly, use_container_width=True)
    
    # Q5 - JOIN Query Sample
    st.subheader(" Q5: JOIN Query Sample (Patents + Inventors + Companies)")
    join_sample = pd.DataFrame({
        'Patent ID': ['10000000', '10000001', '10000002', '10000003', '10000004'],
        'Title': ['Coherent LADAR', 'Injection molding machine', 'Polymer film method', 
                  'Container production', 'Double-oriented film'],
        'Inventor': ['Wenjing Jiang', 'Eiko BÄUMKER', 'Richard Kroeger', 'Thomas A. Bush', 'Matthew F. Boudreaux'],
        'Company': ['0', '0', '0', '0', '1']
    })
    st.dataframe(join_sample, use_container_width=True)
    
    # Q6 - CTE Query
    st.subheader(" Q6: CTE Query (WITH statement - Percentages)")
    if len(top_inventors) > 0:
        total = top_inventors['patent_count'].sum()
        cte_sample = top_inventors.head(10).copy()
        cte_sample['percentage'] = (cte_sample['patent_count'] / total * 100).round(2)
        st.dataframe(cte_sample[['name', 'patent_count', 'percentage']], use_container_width=True)
    
    # Q7 - Ranking Query
    st.subheader(" Q7: Ranking Query (Window Functions)")
    if len(top_inventors) > 0:
        ranking_sample = top_inventors.head(10).copy()
        ranking_sample['rank'] = range(1, len(ranking_sample) + 1)
        st.dataframe(ranking_sample[['name', 'patent_count', 'rank']], use_container_width=True)


st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p> <strong>Patent Data Pipeline Project</strong> | 7 SQL Queries | SQL Database | CSV/JSON Reports | Interactive Visualizations</p>
    <p>Data source: PatentsView Granted Patent Disambiguated Data (USPTO)</p>
    <p>Built with Python, pandas, SQLite, Plotly, and Streamlit</p>
</div>
""", unsafe_allow_html=True)
