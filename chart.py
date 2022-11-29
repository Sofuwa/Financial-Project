# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:19:20 2022

@author: osofuwa
"""

from numerize import numerize
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st
from ta.trend import MACD
from ta.momentum import RSIIndicator


def Charts(tabs,ticker_list,ticker_selected):
    chart_tickers = list(ticker_list)
    chart_tickers.insert(0,'None')
    with tabs[2]:
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def change_chart_duration():
            if st.session_state["change_chart_duration"] != "None":
                st.session_state["chart_start_date"] = dt.date.today()-relativedelta(years=10)
                st.session_state["chart_end_date"] = dt.date.today()
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def change_chart_date():
            if (st.session_state["chart_start_date"] != dt.date.today()-relativedelta(years=10)) or (st.session_state["chart_end_date"] != dt.date.today()):
                st.session_state["change_chart_duration"] = "None"
                
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def get_full_data(ticker_selected):
            raw_data = ticker_selected.history(period='max', interval='1d')
            raw_data = raw_data.reset_index()
            raw_data = raw_data.iloc[:,:-2]
            raw_data = raw_data.dropna()
            raw_data = raw_data.reset_index(drop=True)
            raw_data['diff'] = raw_data['Close'] - raw_data['Open']
            raw_data['MA50'] = raw_data['Close'].rolling(window=50).mean()
            raw_data['MA200'] = raw_data['Close'].rolling(window=200).mean()
            raw_data.loc[raw_data['diff']>=0, 'Color'] = 'green'
            raw_data.loc[raw_data['diff']<0, 'Color'] = 'red'
            return raw_data
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def merge_data(first_data, second_data):
            second_data = second_data.reset_index()
            second_data = second_data.iloc[:,:-2]
            second_data = second_data.dropna()
            second_data = second_data.reset_index(drop=True)
            second_data = second_data.merge(first_data[['Date','MA50','MA200','Color']],on='Date')
            second_data = second_data.reset_index(drop=True)
            return second_data
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)             
        def get_chart_data(ticker_selected, chart_duration_dict, chart_duration, chart_interval_dict, 
                           chart_interval, chart_start_date, chart_end_date):
            
            if chart_duration != 'None':
                tick_history = ticker_selected.history(period=chart_duration_dict.get(chart_duration), 
                                                       interval=chart_interval_dict.get(chart_interval))
                full_data = get_full_data(ticker_selected)
                tick_history = merge_data(full_data, tick_history)
                
            elif chart_start_date or chart_end_date:
                tick_history = ticker_selected.history(start=chart_start_date, end=chart_end_date, 
                                                       interval=chart_interval_dict.get(chart_interval))
                full_data = get_full_data(ticker_selected)
                tick_history = merge_data(full_data, tick_history)
            return tick_history
       
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False)  
        def charts(plot_data, chart_type, chart_indicator):
            chart_fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7,0.4,0.4,0.4])
            
            macd = MACD(close=plot_data['Close'], 
                        window_slow=26,
                        window_fast=12, 
                        window_sign=9)
    
            rsi = RSIIndicator(plot_data['Close'], window=14)
            
            if chart_type == 'Line':
                chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=plot_data['Close'], marker_color='blue', name='Close'))
            elif chart_type == 'Candle Plot':
                chart_fig.add_trace(go.Candlestick(x=plot_data['Date'],
                                                   open=plot_data['Open'].apply('{:.2f}'.format),
                                                   high=plot_data['High'].apply('{:.2f}'.format),
                                                   low=plot_data['Low'].apply('{:.2f}'.format),
                                                   close=plot_data['Close'].apply('{:.2f}'.format),
                                                   name=''))
    
            if chart_indicator == 'Moving Average 50':
                chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=plot_data['MA50'], marker_color='green', name='50 Day MA'))
            elif chart_indicator == 'Moving Average 200':
                chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=plot_data['MA200'], marker_color='orange', name='200 Day MA'))
            elif chart_indicator == 'Moving Average 50 & 200':
                chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=plot_data['MA50'], marker_color='green', name='50 Day MA'))
                chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=plot_data['MA200'], marker_color='orange', name='200 Day MA'))
            else:
                pass
            
            chart_fig.add_trace(go.Bar(x=plot_data['Date'], 
                                       y=plot_data['Volume'], name='Volume', marker_color=plot_data['Color']), row=2, col=1)
            
            chart_fig.add_trace(go.Bar(x=plot_data['Date'], y=round(macd.macd_diff(),2), name='MACD Diff', marker=dict(color = 'maroon')), row=3, col=1)
            chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=round(macd.macd(),2), line=dict(color='orange', width=1.5), name='MACD'), row=3, col=1)
            chart_fig.add_trace(go.Scatter(x=plot_data['Date'], y=round(macd.macd_signal(),2), line=dict(color='blue', width=1), name='MACD Signal'), row=3, col=1)
            
            chart_fig.add_trace(go.Scatter(x=plot_data['Date'],y=round(rsi.rsi(),2), line=dict(color='peru', width=2), name='RSI'), row=4, col=1)
            
            chart_fig.update_layout(showlegend=False, 
                                    annotations=[dict(x=plot_data['Date'].iloc[-1], y=0.66, xref='x', yref='paper',showarrow=False, xanchor='right', font=dict(size=13),
                                                      text='<b>Trading Volume: <b>' + numerize.numerize(float(plot_data['Volume'].iloc[-1])))],
                                    hoverlabel=dict(bgcolor="black",font_size=16,font_color="white",font_family="Calibri",align="right"), 
                                    hoverlabel_align = 'left',
                                    hovermode="x unified",
                                    xaxis_rangeslider_visible=False,
                                    yaxis=dict(side="right"),
                                    yaxis2=dict(side="right"),
                                    yaxis3=dict(side="right"),
                                    yaxis4=dict(side="right"),
                                    margin=dict(l=20, r=20, t=20, b=45),
                                    width=1350,height=650,
                                    modebar_remove=['zoom','pan','autoscale','zoomIn2d','zoomOut2d','resetScale','lasso2d','select'], 
                                    template='seaborn')
            
            chart_fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
            
            chart_fig.update_yaxes(title_text="<b>Price<b>", row=1, col=1, title_font=dict(size=14), title_font_family="Arial", 
                                showticklabels=True, showspikes=True, spikecolor="black", spikethickness=0.5, spikesnap="cursor", spikemode="across")
            chart_fig.update_yaxes(title_text="<b>Volume<b>", row=2, col=1, title_font=dict(size=14), title_font_family="Arial",
                                showticklabels=True, showspikes=True, spikecolor="black", spikethickness=0.5, spikesnap="cursor", spikemode="across")
            chart_fig.update_yaxes(title_text="<b>MACD<b>", row=3, col=1, title_font=dict(size=14), title_font_family="Arial",
                                showticklabels=True, showspikes=True, spikecolor="black", spikethickness=0.5, spikesnap="cursor", spikemode="across")
            chart_fig.update_yaxes(title_text="<b>RSI<b>", row=4, col=1, title_font=dict(size=14), title_font_family="Arial",
                                showticklabels=True, showspikes=True, spikecolor="black", spikethickness=0.5, spikesnap="cursor", spikemode="across")
            
            return chart_fig
            
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            chart_indicator = st.selectbox("Select an indicator", ['None','Moving Average 50','Moving Average 200',
                                                                   'Moving Average 50 & 200'])
        with col2:
            chart_start_date = st.date_input("Select a start date", (dt.date.today()-relativedelta(years=10)),
                                             on_change=change_chart_date, key="chart_start_date")
        with col3:
            chart_end_date = st.date_input("Select an end date", (dt.date.today()),
                                           on_change=change_chart_date, key="chart_end_date")
        with col4:
            chart_duration_dict = {'None':'None','1M':'1mo', '3M':'3mo', '6M':'6mo', 
                                   'YTD':'ytd', '1Y':'1y', '5Y':'5y', 'Max':'max'}
            chart_duration = st.selectbox("Select a time duration", list(chart_duration_dict.keys()),
                                          on_change=change_chart_duration, key="change_chart_duration")
        with col5:
            chart_interval_dict = {'Daily':'1d', 'Weekly':'1wk', 'Monthly':'1mo'}
            chart_interval = st.selectbox("Interval", list(chart_interval_dict.keys()))
        with col6:
            chart_type = st.selectbox("Select a chart type", ['Line','Candle Plot'])
            
        chart_history = get_chart_data(ticker_selected, chart_duration_dict, chart_duration, chart_interval_dict, 
                                       chart_interval, chart_start_date, chart_end_date)
        
        chart_img = charts(chart_history, chart_type, chart_indicator)
        st.plotly_chart(chart_img)