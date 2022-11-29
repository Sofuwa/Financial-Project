# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:54:33 2022

@author: osofuwa
"""

import yahoo_fin.stock_info as yf_si
import streamlit as st

def Estimates(tabs,single_ticker):
    with tabs[6]:
        st.subheader("Earnings Estimate")
        earnings_est = yf_si.get_analysts_info(single_ticker)["Earnings Estimate"]
        earn_est_cols = earnings_est.columns[1:]
        earnings_est[earn_est_cols] = earnings_est[earn_est_cols].applymap('{:.2f}'.format)
        earnings_est = earnings_est.set_index('Earnings Estimate')
        st.dataframe(earnings_est, width = 800)
        
        st.subheader("Revenue Estimate")
        revenue_est = yf_si.get_analysts_info(single_ticker)["Revenue Estimate"]
        revenue_est = revenue_est.set_index('Revenue Estimate')
        st.dataframe(revenue_est, width = 800)
        
        st.subheader("Earnings History")
        earn_hist = yf_si.get_analysts_info(single_ticker)["Earnings History"]
        earn_hist = earn_hist.set_index('Earnings History')
        st.dataframe(earn_hist, width = 800)
        
        st.subheader("EPS Trend")
        eps_trend = yf_si.get_analysts_info(single_ticker)["EPS Trend"]
        eps_trend_cols = eps_trend.columns[1:]
        eps_trend[eps_trend_cols] = eps_trend[eps_trend_cols].applymap('{:.2f}'.format)
        eps_trend = eps_trend.set_index('EPS Trend')
        st.dataframe(eps_trend, width = 800)
        
        st.subheader("EPS Revisions")
        eps_rev = yf_si.get_analysts_info(single_ticker)["EPS Revisions"]
        eps_rev_cols = eps_rev.columns[1:]
        eps_rev[eps_rev_cols] = eps_rev[eps_rev_cols].astype("Int64").astype(str)
        eps_rev[eps_rev_cols] = eps_rev[eps_rev_cols].replace('<NA>','N/A')
        eps_rev = eps_rev.set_index('EPS Revisions')
        st.dataframe(eps_rev, width = 800)
        
        st.subheader("Growth Estimates")
        growth_est = yf_si.get_analysts_info(single_ticker)["Growth Estimates"]
        growth_est_cols = growth_est.columns[1:]
        growth_est[growth_est_cols] = growth_est[growth_est_cols].astype(str)
        growth_est[growth_est_cols] = growth_est[growth_est_cols].replace('nan','N/A')
        growth_est = growth_est.set_index('Growth Estimates')
        st.dataframe(growth_est, width = 800)