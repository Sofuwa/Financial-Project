# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:58:28 2022

@author: osofuwa
"""

import pandas as pd
import streamlit as st

def Holders(tabs,ticker_selected):
    with tabs[7]:
        st.title("Holders")
        st.subheader("Major Holders")
        st.write("Breakdown")
        major_holders = ticker_selected.major_holders
        major_holders = major_holders.rename(columns={0:"Value", 1:"Breakdown"})
        major_holders = major_holders[["Breakdown","Value"]]
        major_holders = major_holders.set_index('Breakdown')
        st.dataframe(major_holders, width = 400)
        
        st.write("")
        st.subheader("Institutional Holders")
        inst_holders = ticker_selected.institutional_holders
        inst_holders.loc[:, ["Value","Shares"]] = inst_holders[["Value","Shares"]].applymap('{:,}'.format)
        inst_holders.loc[:, "% Out"] = inst_holders["% Out"].map('{:.2%}'.format)
        inst_holders["Date Reported"] = pd.to_datetime(inst_holders["Date Reported"]).dt.strftime("%b %d, %Y")
        inst_holders = inst_holders.set_index('Holder')
        st.dataframe(inst_holders, width = 800)
        
        st.write("")
        st.subheader("Top Mutual Fund Holders")
        mut_holders = ticker_selected.mutualfund_holders
        mut_holders.loc[:, ["Value","Shares"]] = mut_holders[["Value","Shares"]].applymap('{:,}'.format)
        mut_holders.loc[:, "% Out"] = mut_holders["% Out"].map('{:.2%}'.format)
        mut_holders["Date Reported"] = pd.to_datetime(mut_holders["Date Reported"]).dt.strftime("%b %d, %Y")
        mut_holders = mut_holders.set_index('Holder')
        st.dataframe(mut_holders, width = 800)