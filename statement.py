# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:36:32 2022

@author: osofuwa
"""

import streamlit as st

def Statements(tabs,single_ticker,ticker_selected):
    with tabs[5]:
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def convert_stmt(df):
            return df.to_csv()
        
        def download_stmt(stmt_df, stmt, timeframe):
            timef = timeframe.lower()[0]
            stmt_type = stmt.split()[0][:3] + '_' + stmt.split()[1][:2]
            file_name_end = '.' + stmt_type + '.' + timef +  '.csv'
            csv = convert_stmt(stmt_df)
            st.download_button(
                label = "Download data as csv",
                data = csv,
                file_name= single_ticker.lower() + file_name_end.lower()) 
         
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def clean_stmt(stm_df):
            stm_df.columns = stm_df.columns.astype("str").str.replace('-','/')
            stm_df = stm_df.fillna(0)
            for i in range(len(stm_df.columns)):
                colname =stm_df.columns[i]
                stm_df[colname]= [int(float(i)) for i in stm_df[colname]]
            stm_df.iloc[:,:] = stm_df.iloc[:,:].applymap('{:,}'.format)
            stm_df.iloc[:,:] = stm_df.iloc[:,:].astype(str).replace('0','N/A')
            return stm_df
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)      
        def get_stmt(ticker_select, select_fin, select_fin_time, single_tick = 'None'):
            
            if select_fin == 'Balance Sheet':
                if select_fin_time == 'Annual':
                    st.header(single_tick + "'s " + select_fin_time + ' Balance Sheet')
                    stmt_data = ticker_select.balance_sheet
                    stmt_data = clean_stmt(stmt_data)
                else:
                    st.header(single_tick + "'s " + select_fin_time + ' Balance Sheet')
                    stmt_data = ticker_select.quarterly_balance_sheet
                    stmt_data = clean_stmt(stmt_data)
            elif select_fin == 'Cash Flow':
                if select_fin_time == 'Annual':
                    st.header(single_tick + "'s " + select_fin_time + ' Cash Flow')
                    stmt_data = ticker_select.cashflow
                    stmt_data = clean_stmt(stmt_data)
                else:
                    st.header(single_tick + "'s " + select_fin_time + ' Cash Flow')
                    stmt_data = ticker_select.quarterly_cashflow
                    stmt_data = clean_stmt(stmt_data)
            else:
                if select_fin_time == 'Annual':
                    st.header(single_tick + "'s " + select_fin_time + ' Income Statement')
                    stmt_data = ticker_select.income_stmt
                    stmt_data = clean_stmt(stmt_data)
                else:
                    st.header(single_tick + "'s " + select_fin_time + ' Income Statement')
                    stmt_data = ticker_select.quarterly_income_stmt
                    stmt_data = clean_stmt(stmt_data)
                
            return stmt_data
        
        col1, col2= st.columns(2)
        with col1:
            selected_fin = st.selectbox("Select a finanacial statement", ['Income Statement','Balance Sheet','Cash Flow'])
        with col2:
            selected_fin_time = st.selectbox("Select a finanacial period", ['Annual','Quarterly'])
        
        stat_data = get_stmt(ticker_selected, selected_fin, selected_fin_time, single_tick = single_ticker)
        download_stmt(stat_data, selected_fin, selected_fin_time)
        st.dataframe(stat_data, width = 1400, height= 600)
        st.write("")