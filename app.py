import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv('startup_cleaned.csv')

df['date'] = df['date'].str.replace('05/072018','05/07/2018')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

st.set_page_config(layout='wide',page_title='Startup Analysis')

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())

    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    # avg ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    # total funded startups
    num_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max',str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg',str(avg_funding) + ' Cr')
    with col4:
        st.metric('Funded Startups',num_startup)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

    #temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    temp_df['date'] = pd.to_datetime(temp_df['year'].astype('str') + '-' + temp_df['month'].astype('str') + '-01')

    fig4, ax4 = plt.subplots(figsize=(6,4))
    ax4.plot(temp_df['date'],temp_df['amount'])

    ax4.xaxis.set_major_locator(mdates.YearLocator())
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xticks(rotation=0)

    st.pyplot(fig4,use_container_width=False)

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
    #biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        fig1 , ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)
    col3, col4 = st.columns(2)
    with col3:
        stages_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stages Invested In')
        fig2 , ax2 = plt.subplots()
        ax2.pie(stages_series,labels=stages_series.index,autopct="%0.01f%%")

        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Invested In')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series,labels=city_series.index,autopct="%0.1f%%")

        st.pyplot(fig3)

    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    ax4.plot(year_series.index,year_series.values)

    st.pyplot(fig4,use_container_width=False)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    
    load_overall_analysis()
elif option == 'Startup':
    company = df['startup'].unique()
    company_df = pd.DataFrame(company, columns=['startup']).sort_values('startup')
    st.sidebar.selectbox('Select Startup',company_df['startup'])
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    investor = sorted(set(df['investors'].str.split(',').sum()))
    investor_df = pd.DataFrame(investor,columns=['investors'])
    selected_investors = st.sidebar.selectbox('Select Investor',investor_df['investors'])
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investors)

