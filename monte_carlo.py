# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:19:27 2022

@author: osofuwa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as web
from dateutil.relativedelta import relativedelta
import streamlit as st

def Montecarlo(tabs,single_ticker,ticker_selected):
    with tabs[8]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            mc_start_date = st.date_input("Select a start date", (dt.date.today()-relativedelta(years=10)), key="mc_start_date")
        with col2:
            mc_end_date = st.date_input("Select an end date", (dt.date.today()), key="mc_end_date")
        with col3:
            selected_horizon = st.selectbox("Select a time horizon", [30, 60, 90])
        with col4:
            selected_sim = st.selectbox("Number of simulations", [200, 500, 1000])
        
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False) 
        class MonteCarlo(object):
            mc_start = str(dt.date.today()-relativedelta(years=1))
            mc_end = str(dt.date.today())
            def __init__(self, ticker, data_source, seed, start_date=mc_start, end_date=mc_end, time_horizon=30, n_simulation=200):
                
                # Initiate class variables
                self.ticker = ticker  # Stock ticker
                self.data_source = data_source  # Source of data, e.g. 'yahoo'
                self.start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')  # Text, YYYY-MM-DD
                self.end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')  # Text, YYYY-MM-DD
                self.time_horizon = time_horizon  # Days
                self.n_simulation = n_simulation  # Number of simulations
                self.seed = seed  # Random seed
                self.simulation_df = pd.DataFrame()  # Table of results
                
                # Extract stock data
                self.stock_price = web.DataReader(ticker, data_source, self.start_date, self.end_date)
                
                # Calculate financial metrics
                # Daily return (of close price)
                self.daily_return = self.stock_price['Close'].pct_change()
                # Volatility (of close price)
                self.daily_volatility = np.std(self.daily_return)
                
            def run_simulation(self):
                
                # Run the simulation
                np.random.seed(self.seed)
                self.simulation_df = pd.DataFrame()  # Reset
                
                for i in range(self.n_simulation):
        
                    # The list to store the next stock price
                    next_price = []
        
                    # Create the next stock price
                    last_price = self.stock_price['Close'][-1]
        
                    for j in range(self.time_horizon):
                        
                        # Generate the random percentage change around the mean (0) and std (daily_volatility)
                        future_return = np.random.normal(0, self.daily_volatility)
        
                        # Generate the random future price
                        future_price = last_price * (1 + future_return)
        
                        # Save the price and go next
                        next_price.append(future_price)
                        last_price = future_price
        
                    # Store the result of the simulation
                    next_price_df = pd.Series(next_price).rename('sim' + str(i))
                    self.simulation_df = pd.concat([self.simulation_df, next_price_df], axis=1)
        
            def plot_simulation_price(self):
                
                # Plot the simulation stock price in the future
                fig, ax = plt.subplots()
                fig.set_size_inches(15, 10, forward=True)
        
                plt.plot(self.simulation_df)
                plt.title('Monte Carlo simulation for ' + self.ticker + \
                          ' stock price in next ' + str(self.time_horizon) + ' days')
                plt.xlabel('Day')
                plt.ylabel('Price')
        
                plt.axhline(y=self.stock_price['Close'][-1], color='red')
                plt.legend(['Current stock price is: ' + str(np.round(self.stock_price['Close'][-1], 2))])
                ax.get_legend().legendHandles[0].set_color('red')
        
                plt.show()
            
            def plot_simulation_hist(self):
                
                # Get the ending price of the 200th day
                ending_price = self.simulation_df.iloc[-1:, :].values[0, ]
        
                # Plot using histogram
                fig, ax = plt.subplots()
                plt.hist(ending_price, bins=50)
                plt.axvline(x=self.stock_price['Close'][-1], color='red')
                plt.legend(['Current stock price: $' + str(np.round(self.stock_price['Close'][-1], 2))])
                ax.get_legend().legendHandles[0].set_color('red')
                ax.set_yticklabels([])
                ax.set_yticks([])
                return fig
            
            def value_at_risk(self):
                # Price at 95% confidence interval
                future_price_95ci = np.percentile(self.simulation_df.iloc[-1:, :].values[0, ], 5)
        
                # Value at Risk
                VaR = self.stock_price['Close'][-1] - future_price_95ci
                return (str(np.round(VaR, 2)), str(np.round(self.stock_price['Close'][-1], 2)))
                #print('VaR at 95% confidence interval is: ' + str(np.round(VaR, 2)) + ' USD')
                
        # Initiate
        mc_sim = MonteCarlo(ticker=single_ticker, data_source='yahoo',
                            start_date=str(mc_start_date), end_date=str(mc_end_date),
                            time_horizon=selected_horizon, n_simulation=selected_sim, seed=241)
        # Get data
        mc_data = mc_sim.stock_price
        # Run simulation
        mc_sim.run_simulation()
        # Value at risk
        mc_result = mc_sim.value_at_risk()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Value at Risk (VAR)')
            st.write('The current stock price for '+single_ticker+ ' is $'+mc_result[1])
            st.write('The value at risk for investing in '+single_ticker+ ' over the next '+str(selected_horizon)+
                     ' days is approximately $'+mc_result[0])
            st.subheader('Recommendation')
            st.write('This is the recommendation given by analysts:')
            try:
                st.write('**Total Analyst Opinions:** '+str(ticker_selected.info['numberOfAnalystOpinions']))
            except:
                st.write('**Total Analyst Opinions:** No opinion available')
            try:
                st.write('**Buy or Sell:** '+ticker_selected.info['recommendationKey'].upper())
            except:
                st.write('**Buy or Sell:** No recommendation available')
            try:
                st.write('**Recommendation Mean:** '+str(ticker_selected.info['recommendationMean']))
            except:
                st.write('**Recommendation Mean:** No recommendation mean available')
            
        with col2:
            st.write("")
            st.write("")
            mc_hist = mc_sim.plot_simulation_hist()
            st.pyplot(mc_hist)