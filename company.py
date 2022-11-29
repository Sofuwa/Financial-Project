# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:08:44 2022

@author: osofuwa
"""

import numpy as np
from numerize import numerize
import yahoo_fin.stock_info as yf_si
import streamlit as st

def Company(ticker_selected, tabs):
    with tabs [0]:
        st.title('Company Information')
        st.header(ticker_selected.info['longName'])
        st.image(ticker_selected.info['logo_url'], width=100)
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.write(ticker_selected.info['address1'])
            try:
                st.write(ticker_selected.info['city']+',',ticker_selected.info['state'],' ',ticker_selected.info['zip'])
            except:
                st.write(ticker_selected.info['city'],' ',ticker_selected.info['zip'])
            st.write(ticker_selected.info['country'])
            st.write(ticker_selected.info['phone'])
            st.write(ticker_selected.info['website'])
        with col2:
            st.write('**Sector(s):**', ticker_selected.info['sector'])
            st.write('**Industry:**', ticker_selected.info['industry'])
            st.write('**Full time employees:**', str(ticker_selected.info['fullTimeEmployees']))
    
        st.write("")
        st.subheader('Description')
        st.write(ticker_selected.info['longBusinessSummary'])
        st.write("")
    
        st.subheader('Key Executives')
        company_officers = yf_si.get_company_officers('NFLX')
        company_officers = company_officers.reset_index(drop=False)
        company_officers = company_officers.iloc[:,:5]
        company_officers = company_officers.rename(columns={'name': 'Name', 'totalPay': 'Pay', 'exercisedValue':'Exercised', 'yearBorn':'Year Born', 'title':'Title'})
        company_officers = company_officers[['Name','Title','Pay','Exercised','Year Born']]
        company_officers.iloc[:,2:] = company_officers.iloc[:,2:].replace(np.nan,0)
        company_officers['Pay'] = [numerize.numerize(y) for y in company_officers['Pay']]
        company_officers['Exercised'] = [numerize.numerize(y) for y in company_officers['Exercised']]
        company_officers['Year Born'] = company_officers['Year Born'].astype("Int64").astype(str)
        company_officers.iloc[:,2:] = company_officers.iloc[:,2:].replace('0','N/A')
        company_officers = company_officers.set_index('Name')
        
        st.dataframe(company_officers, width = 800)
        st.markdown("_Pay is salary, bonuses, etc. Exercised is the value of options exercised during the fiscal year. Currency in USD._")