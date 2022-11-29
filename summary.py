# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:13:04 2022

@author: osofuwa
"""
import numpy as np
import pandas as pd
import math
import streamlit_nested_layout
import plotly.express as px
import yahoo_fin.stock_info as yf_si
import streamlit as st

def Summary(tabs, single_ticker, ticker_selected, ticker_list):
    with tabs[1]:
        stat_json = yf_si.get_quote_table(single_ticker)
        col1, col2, col3 = st.columns([1.5,2.2,4.5])
        with col1:
            col1_stat = [["Previous Close", str(stat_json["Previous Close"])],["Open", str(stat_json["Open"])], 
                         ["Bid", stat_json["Bid"]],["Ask", stat_json["Ask"]],["Day's Range", stat_json["Day's Range"]], 
                         ["52 Week Range", stat_json["52 Week Range"]],["Volume", str(format(int(stat_json["Volume"]),',d'))],
                         ["Avg. Volume", str(format(int(stat_json["Avg. Volume"]),',d'))]]
            col1_df = pd.DataFrame(data = col1_stat, columns=["Stat","Value"])
            col1_df = col1_df.replace({'Values':{'N/A (N/A)':'N/A', np.nan:'N/A','nan':'N/A'}})
            col1_df = col1_df.set_index('Stat')
            st.write("")
            st.write("")
            st.dataframe(col1_df, width = 250)
            
        with col2:
            col2_stat = [["Market Cap", str(stat_json["Market Cap"])],["Beta (5Y Monthly)", str(stat_json["Beta (5Y Monthly)"])], 
                         ["PE Ratio (TTM)", str(stat_json["PE Ratio (TTM)"])],["EPS (TTM)", str(stat_json["EPS (TTM)"])],
                         ["Earnings Date", stat_json["Earnings Date"]], 
                         ["Forward Dividend & Yield", stat_json["Forward Dividend & Yield"]],
                         ["Ex-Dividend Date", stat_json["Ex-Dividend Date"]],
                         ["1y Target Est", str(stat_json["1y Target Est"])]]
            col2_df = pd.DataFrame(data = col2_stat, columns=["Stat","Value"])
            col2_df = col2_df.replace({'Values':{'N/A (N/A)':'N/A', np.nan:'N/A','nan':'N/A'}})
            col2_df = col2_df.set_index('Stat')
            st.write("")
            st.write("")
            st.dataframe(col2_df, width = 350)
        
        with col3:
            @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
            def summary_data(chart_ticker,period='1mo'):
                history = chart_ticker.history(period)
                history = history.reset_index()
                y_max = math.ceil(history['Close'].max())
                y_min = math.floor(history['Close'].min())
                
                fig = (px.area(history, x="Date", y="Close",template="seaborn",color_discrete_sequence=["#0000FF"])
                      .update_layout(yaxis=dict(side="right"),yaxis_range=[y_min,y_max], 
                             margin=dict(l=20, r=20, t=20, b=20), 
                             width=700,height=325,
                             modebar_remove=['zoom','pan','autoscale','zoomIn2d','zoomOut2d','resetScale'], 
                             hovermode="x unified",
                             hoverlabel_align = 'left',
                             hoverlabel=dict(bgcolor="black",font_size=16,font_color="white",font_family="Calibri"))
                      .update_xaxes(title = None,visible=True, showticklabels=True)
                      .update_yaxes(title = None,visible=True, showticklabels=True,
                                    showspikes=True, spikecolor="black", spikethickness=0.5, spikesnap="cursor", spikemode="across")
                      .update_traces(mode=None,line_width=1,hovertemplate="Close: %{y:.2f}"))
                return fig
            but1, but2, but3, but4, but5, but6, but7, but8, but9, but10 = st.columns([1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1])
            with but2:
               st.write("")
               but2_result = st.button('1M')
            with but3:
               st.write("")
               but3_result = st.button('3M')
            with but4:
               st.write("")
               but4_result = st.button('6M')
            with but5:
               st.write("")
               but5_result = st.button('YTD')
            with but6:
               st.write("")
               but6_result = st.button('1Y')
            with but7:
               st.write("")
               but7_result = st.button('3Y')
            with but8:
               st.write("")
               but8_result = st.button('5Y')
            with but9:
               st.write("")
               but9_result = st.button('Max')
    
            if but2_result:
                summary_chart = summary_data(ticker_selected,period='1mo')
                st.plotly_chart(summary_chart)
            elif but3_result:
                summary_chart = summary_data(ticker_selected,period='3mo')
                st.plotly_chart(summary_chart)
            elif but4_result:
                summary_chart = summary_data(ticker_selected,period='6mo')
                st.plotly_chart(summary_chart)
            elif but5_result:
                summary_chart = summary_data(ticker_selected,period='ytd')
                st.plotly_chart(summary_chart)
            elif but6_result:
                summary_chart = summary_data(ticker_selected,period='1y')
                st.plotly_chart(summary_chart)
            elif but7_result:
                summary_chart = summary_data(ticker_selected,period='3y')
                st.plotly_chart(summary_chart)
            elif but8_result:
                summary_chart = summary_data(ticker_selected,period='5y')
                st.plotly_chart(summary_chart)
            elif but9_result:
                summary_chart = summary_data(ticker_selected,period='max')
                st.plotly_chart(summary_chart)
            else:
                summary_chart = summary_data(ticker_selected,period='1mo')
                st.plotly_chart(summary_chart)