# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:31:47 2022

@author: osofuwa
"""

import yahoo_fin.stock_info as yf_si
import streamlit as st


def Stocks(tabs,single_ticker):
    with tabs[3]:
        col1, col2, col3= st.columns(3)
        stat_table = yf_si.get_stats(single_ticker)
        stat_table['Attribute'] = [x.rstrip('0123456789').rstrip() for x in stat_table['Attribute']]
        stat_table['Value'] = stat_table['Value'].astype(str).replace('nan','N/A')
        stat_table = stat_table.set_index('Attribute')
        with col1:
            st.subheader('Trading Information')
            st.markdown('**Stock Price History**')
            st.dataframe(stat_table.iloc[:7,:], width=400)
            st.markdown('**Validation Measures**')
            other_stat = yf_si.get_stats_valuation(single_ticker)
            other_stat = other_stat.iloc[:,:2]
            other_stat = other_stat.set_index(other_stat.columns[0])
            #other_stat = other_stat.rename(columns={1:'Value'})
            #other_stat['Value'] = other_stat['Value'].astype(str).replace('nan','N/A')
            #other_stat = other_stat.set_index(0)
            st.dataframe(other_stat, width=400)
            st.markdown('**Share Statistics**')
            st.dataframe(stat_table.iloc[7:19,:], width=400,height=457)
            st.markdown('**Divdends and Splits**')
            st.dataframe(stat_table.iloc[19:29,:], width=400,height=387)
        with col2:
            st.subheader('Financial Highlights')
            st.markdown('**Fiscal Year**')
            st.dataframe(stat_table.iloc[29:31,:], width=400)
            st.markdown('**Profotability**')
            st.dataframe(stat_table.iloc[31:33,:], width=400)
            st.markdown('**Management Effectiveness**')
            st.dataframe(stat_table.iloc[33:35,:], width=400)
            st.markdown('**Income Statement**')
            st.dataframe(stat_table.iloc[35:43,:], width=400)
            st.markdown('**Balance Sheet**')
            st.dataframe(stat_table.iloc[43:49,:], width=400)
            st.markdown('**Cash Flow**')
            st.dataframe(stat_table.iloc[49:,:], width=400)
