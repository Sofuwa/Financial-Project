# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:24:07 2022

@author: osofuwa
"""
import time
from PIL import Image, ImageOps
import urllib.request as ureq
from bs4 import BeautifulSoup
import requests
import timeago
import datetime as dt
import streamlit as st

def News(tabs,ticker_selected):
    with tabs[9]:
        @st.cache(allow_output_mutation=True,suppress_st_warning=True, show_spinner=False) 
        def add_border(input_image, border):
            img = Image.open(ureq.urlopen(input_image))
            if isinstance(border, int) or isinstance(border, tuple):
                bimg = ImageOps.expand(img, border=border)
            else:
                raise RuntimeError('Border is not an integer or tuple!')
            return bimg
    
        news_title = []
        news_publisher = []
        news_time = []
        news_image = []
        news_link = []
        news_article = []
    
        for i in range(len(ticker_selected.news)):
            try:
              news_title.append(ticker_selected.news[i]['title'])
              news_publisher.append(ticker_selected.news[i]['publisher'])
              how_long = ticker_selected.news[i]['providerPublishTime']
              date_time = dt.datetime.fromtimestamp(how_long)  
              news_time.append(timeago.format(date_time, dt.datetime.now()))
              news_image.append(ticker_selected.news[i]['thumbnail']['resolutions'][0]['url'])
              newslink = ticker_selected.news[i]['link']
              news_link.append(newslink)
              page = requests.get(newslink) 
              soup = BeautifulSoup(page.content , 'html.parser')
              find_divs = soup.find_all("div", {"class": "caas-body"})
              find_p = soup.find_all('p')[0].get_text().replace('\xa0','')
              if find_p == 'Thank you for your patience.':
                  news_article.append('')
              else:
                  news_article.append(find_p)
              time.sleep(1.5)
            except:
              news_title.append('N/A')
              news_publisher.append('N/A')
              news_time.append('N/A')
              news_image.append('N/A')
              news_article.append('')
                
        st.header('Recent News')
    
        for i in range(len(news_link)):
            if news_title[i] != 'N/A':
                try:
                    in_img = news_image[i]
                    bf = add_border(in_img, border=(6, 6))
                    st.image(bf,width=200)
                except:
                    in_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvJVfKp6sdYToK8eEOMaR8PKdmPA0PXjpZDag6FgJp2HWoBGHcTphYSj0ZaXWJ4ThlJ7I&usqp=CAU"
                    bf = add_border(in_img, border=(6, 6))
                    st.image(bf,width=200)
                st.subheader(news_title[i])
                st.markdown('**Published by:** %s' %news_publisher[i])
                st.caption(news_time[i])
                st.write(news_article[i])
                st.markdown("*[Read full article](%s)*" %news_link[i])
                st.write("")
                st.write("")
                st.write("")
            else:
                pass
