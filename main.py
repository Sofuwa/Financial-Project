# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:08:44 2022

@author: osofuwa
"""

import pandas as pd
import time
import yfinance as yf
import yahoo_fin.stock_info as yf_si
import streamlit as st
import company
import summary
import chart
import analysis
import history
import statement
import estimates
import holders
import monte_carlo
import news

#==============================================================================
# Main body
#==============================================================================
st.set_page_config(page_title="My Financial Website", page_icon='favicon.ico', layout="wide")

st.title("S&P 500 Companies financial dashboard")
with st.expander('About this app'):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("")
        st.image('yf_logo.png', width=250)
    
    with col2:
        st.write("")
    
    with col3:
        st.write("")
    st.write('This app shows the various financial information for companies listed on S&P 500 companies.')
    st.markdown('**_Data Source:_** *Yahoo Finance*')
    
ticker_list = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
single_ticker = st.selectbox(label='Choose or input a ticker',options = ticker_list)
ticker_selected = yf.Ticker(single_ticker)


with st.spinner('Fetching information...'):
    time.sleep(5)

tic1, tic2, tic3 = st.columns(3)
with tic1:
    st.write("")
    st.header(ticker_selected.info['symbol'])

with tic2:
    st.write("")

with tic3:
    st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    live_price = str(round(yf_si.get_live_price('NFLX'),1))
    st.metric(label="Live Price(USD)", value=live_price)

with col2:
    try:
        postmarket_price = str(round(yf_si.get_postmarket_price('NFLX'),1))
        st.metric(label="Post-Market Price(USD)", value=postmarket_price)
    except AssertionError:
        st.write("")
        st.write("")
        st.write('Postmarket price not currently available.')

with col3:
    st.write("")
    st.write("")
    st.write('**Market Status:**', yf_si.get_market_status())

tabs_list = ["Company Profile", "Summary", "Chart", "Statistics", "Historical Data", "Financials", "Analysis", "Holders", "Investor's Corner", "News"]    
tabs = st.tabs(tabs_list)

company.Company(single_ticker, ticker_selected, tabs)
summary.Summary(tabs, single_ticker, ticker_selected, ticker_list)
chart.Charts(tabs,ticker_list,ticker_selected)
analysis.Stocks(tabs,single_ticker)
history.History(tabs,single_ticker,ticker_selected)
statement.Statements(tabs,single_ticker,ticker_selected)
estimates.Estimates(tabs,single_ticker)
holders.Holders(tabs,ticker_selected)
monte_carlo.Montecarlo(tabs,single_ticker,ticker_selected)
news.News(tabs,ticker_selected)
