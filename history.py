# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:34:32 2022

@author: osofuwa
"""

import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st

def History(tabs,single_ticker,ticker_selected):
    with tabs[4]:
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def convert_df(df):
            return df.to_csv()
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def change_duration():
            if st.session_state["change_duration"] != "None":
                st.session_state["start_date"] = dt.date.today()-relativedelta(years=10)
                st.session_state["end_date"] = dt.date.today()
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def change_date():
            if (st.session_state["start_date"] != dt.date.today()-relativedelta(years=10)) or (st.session_state["end_date"] != dt.date.today()):
                st.session_state["change_duration"] = "None"
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def clean_columns(data_df):
            data_df = data_df.reset_index()
            data_df = data_df.sort_values(by='Date', ascending=False)
            data_df = data_df.reset_index(drop=True)
            data_df['Date'] = pd.to_datetime(data_df["Date"]).dt.strftime('%b %d, %Y')
            
            dividends = data_df.iloc[:,[0,-2]]
            dividends['Dividends'] = dividends['Dividends'].apply('{:.2f}'.format)
            dividends = dividends[dividends['Dividends']!='0.00']
            dividends = dividends.reset_index(drop=True)
            
            splits = data_df.iloc[:,[0,-1]]
            splits['Stock Splits'] = splits['Stock Splits'].apply('{:.2f}'.format)
            splits = splits[splits['Stock Splits']!='0.00']
            splits = splits.reset_index(drop=True)
            
            data_df = data_df.iloc[:,:-2]
            data_df_cols = data_df.columns[1:-1]
            data_df[data_df_cols] = data_df[data_df_cols].applymap('{:.2f}'.format)
            data_df['Volume'] = data_df['Volume'].apply('{:,}'.format)
            return data_df, dividends, splits
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)         
        def get_data(ticker_selected, duration_dict, selected_duration, interval_dict, selected_interval, start_date, end_date):
            if selected_duration != 'None':
                history = ticker_selected.history(period=duration_dict.get(selected_duration), 
                                                  interval=interval_dict.get(selected_interval))
                history = clean_columns(history)
                
            elif start_date or end_date:
                history = ticker_selected.history(start=start_date, end=end_date, interval=interval_dict.get(selected_interval))
                history = clean_columns(history)
            return history
        
        def download_data(data_df):
            csv = convert_df(data_df)
            st.download_button(
                label = "Download data as csv",
                data = csv,
                file_name= single_ticker.lower() + ' historical data.csv')  
                
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            start_date = st.date_input("Select a start date", (dt.date.today()-relativedelta(years=10)), 
                                       on_change=change_date, key="start_date")
        with col2:
            end_date = st.date_input("Select an end date", (dt.date.today()), on_change=change_date, key="end_date")
        with col3:
            duration_dict = {'None':'None', '1D':'1d', '5D':'5d', '1M':'1mo', '3M':'3mo', 
                             '6M':'6mo', 'YTD':'ytd', '1Y':'1y', '5Y':'5y', 'Max':'max'}
            selected_duration = st.selectbox("Select a time duration", list(duration_dict.keys()), 
                                             on_change=change_duration, key="change_duration")
        with col4:
            selected_stat = st.selectbox("Show", ['Historical Prices','Dividends Only','Stock Splits'])
        with col5:
            interval_dict = {'Daily':'1d', 'Weekly':'1wk', 'Monthly':'1mo'}
            selected_interval = st.selectbox("Interval", list(interval_dict.keys()), key="selected_interval")
            
        hist_data = get_data(ticker_selected, duration_dict, selected_duration, 
                             interval_dict, selected_interval, start_date, end_date)[0]
        div_data = get_data(ticker_selected, duration_dict, selected_duration, 
                            interval_dict, selected_interval, start_date, end_date)[1]
        split_data = get_data(ticker_selected, duration_dict, selected_duration, 
                              interval_dict, selected_interval, start_date, end_date)[2]
        
        if selected_stat == 'Historical Prices':
            download_data(hist_data) 
            st.write("")
            st.dataframe(hist_data, width = 800)
        elif selected_stat == 'Dividends Only':
            download_data(div_data) 
            st.write("")
            st.dataframe(div_data, width = 400)
        elif selected_stat == 'Stock Splits':
            download_data(split_data) 
            st.write("")
            st.dataframe(split_data, width = 400)