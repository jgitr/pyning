# -*- coding: utf-8 -*-


"""
Part 1:
Description:
 - Scraping multiple pages of news from nasdaq.com.
 - Saving result it as .csv file at local disk.
 - Saving web page source code temporarily after request.

Usage: Executing this whole file in your IDE or from Terminal.

Memo:
Adjusting range(start, end) to define how many pages you want to scrape
Toggling refresh to decide if you want to refresh the pages that have been stored locally.

Author: Junjie Hu, hujunjie@hu-berlin.de
Last modified date: 19-11-2017
"""

"""
Created on Mon Nov 20 14:35:31 2017
Part 2:
    Take output data frame from part 1 and scrape the text to which the links point.
    Apply sentiment analysis. Retrieve underlying stock movements for specified time and date (from output data frame, part 1).
    Check for causality between news arrival and price movements.
@author: Julian
"""

# Part 1
from bs4 import BeautifulSoup as soup
import requests
import datetime
import os
import pandas as pd
import pickle

# Part 2
from selenium import webdriver
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
import pysentiment as ps
#from wordcloud import WordCloud


# Part 1

def nasdaq_news_scraping(page=1, refresh=False):
    # Argument page equals 1 by default
    if page == 1:
        # Visit the home page if page equals 1
        nasdaq_url = 'http://www.nasdaq.com/news/market-headlines.aspx'
    else:
        # Change url by different argument
        nasdaq_url = 'http://www.nasdaq.com/news/market-headlines.aspx?page=' + str(page)

    if (not os.path.exists(direct + '/temp/' + str(page) + '.pkl')) or (refresh is True):
        # connect to the website if the webpage source code file is not exist of we need to refresh it
        url_request = requests.get(nasdaq_url)
        # save the request object after scraping
        with open(direct + '/temp/' + str(page) + '.pkl', 'wb') as url_file:
            pickle.dump(url_request, url_file)
    else:
        # else, we open the source code file from local disk to save time
        with open(direct + '/temp/' + str(page) + '.pkl', 'rb') as url_file:
            url_request = pickle.load(url_file)
    url_content = url_request.content
    parsed_content = soup(url_content)
    containers = parsed_content.find_all('p')

    title_list_page = []
    time_list_page = []
    link_list_page = []
    tag_list_page = []

    for container in containers:
        container_a = container.find_all('a', {"id": "two_column_main_content_la1_rptArticles_hlArticleLink_0"})
        for item in container_a:
            news_link = item.get('href').strip()
            news_title = item.text.strip()
            title_list_page.append(news_title)
            print(news_title)
            link_list_page.append(news_link)
            print(news_link)
        container_span = container.find_all('span', {'class': 'small'})
        for item in container_span:
            item_split = item.text.split(' - ', 1)
            time = datetime.datetime.strptime(item_split[0], '%m/%d/%Y %I:%M:%S %p')
            time_list_page.append(time)
            print(time)
            try:
                tag = item_split[1].split('  in ')[1].strip()
            except Exception:
                tag = []
            tag_list_page.append(tag)
            print(tag)
    return title_list_page, time_list_page, link_list_page, tag_list_page


direct = os.getcwd()
# direct = os.getcwd() + '/DEDA_Class_2017_WebScrapingIntro'

title_list = []
time_list = []
link_list = []
tag_list = []

for page_num in range(1, 10):
    print("\nThis is Page: ", page_num)
    # Using the function defined previously with certain arguments as input
    nasdaq_news_page = nasdaq_news_scraping(page=page_num, refresh=False)
    title_list.extend(nasdaq_news_page[0])
    time_list.extend(nasdaq_news_page[1])
    link_list.extend(nasdaq_news_page[2])
    tag_list.extend(nasdaq_news_page[3])

nasdaq_info = zip(title_list, time_list, link_list, tag_list)
nasdaq_info_df = pd.DataFrame(list(nasdaq_info), columns=['title', 'time', 'link', 'tag'])
print(os.getcwd())
nasdaq_info_df.to_csv(direct + '/Nasdaq_News_MultiPages.csv')


# Part 2

p = "C:/Users/Julian/pyning"
os.chdir(p)

 # Resort dictionary in list
 # Reconvert to dictionary
def valueSelection(dictionary, length, startindex = 0): # length is length of highest consecutive value vector
    
    # Test input
    lengthDict = len(dictionary)
    if length > lengthDict:
        return print("length is longer than dictionary length");
    else:
        d = dictionary
        items = [(v, k) for k, v in d.items()]
        items.sort()
        items.reverse()   
        itemsOut = [(k, v) for v, k in items]
    
        highest = itemsOut[startindex:startindex + length]
        dd = dict(highest)
        wanted_keys = dd.keys()
        dictshow = dict((k, d[k]) for k in wanted_keys if k in d)

        return dictshow;


# Get Text behind Link
ndf = nasdaq_info_df.size
r = range(ndf)

# Start Selenium
browser = webdriver.Firefox()

for i in r:
            
            url = nasdaq_info_df.link[i]
            print(url)
            print(nasdaq_info_df.time[i])
            print(nasdaq_info_df.title[i])
            print(nasdaq_info_df.tag[i])
            
            # Extract text
            browser.get(url)
            id = "articlebody"
            text = browser.find_element_by_id(id).text

            # Some expressions still left
            # Differ between quotes!
            expression = "[()]|(\“)|(\”)|(\“)|(\”)|(\,|\.|-|\;|\<|\>)|(\\n)|(\\t)|(\=)|(\|)|(\-)|(\')|(\’)"
            cleantextCAP = re.sub(expression, '', text)
            cleantext = cleantextCAP.lower()       
            
            # Count and create dictionary
            dat = list(cleantext.split())
            dict1 = {}
            for i in range(len(dat)):
                print(i)
                word = dat[i]
                dict1[word] = dat.count(word)
                continue
            
            # Filter Stopwords
            keys = list(dict1)
            filtered_words = [word for word in keys if word not in stopwords.words('english')]
            dict2 = dict((k, dict1[k]) for k in filtered_words if k in filtered_words)
            
            # Select highest values for statistics at bottom...
            # dictshow = valueSelection(dictionary = dict2, length = 7, startindex = 0)
            
            # Sentiment Analysis
            hiv4 = ps.HIV4()
            tokens = hiv4.tokenize(cleantext)
            score = hiv4.get_score(tokens)
            print(score)
            
            # Polarity
            # Formula: (Positive - Negative)/(Positive + Negative)
            
            # Subjectivity
            # Formula: (Positive + Negative)/N
            
            # If most frequent words or header contains stock name:
            # Get Stock data 
            

            
browser.close()
browser.stop_client()

"""
Some plots

# Save dictionaries for wordcloud
text_file = open("Output.txt", "w")
text_file.write(str(cleantext))
text_file.close()


# Plot
n = range(len(dictshow))
plt.bar(n, dictshow.values(), align='center')
plt.xticks(n, dictshow.keys())
plt.title("Most frequent Words")
#plt.savefig("plot.png")

# Overview
overview =  valueSelection(dictionary = dict2, length = 50, startindex = 0)
nOverview = range(len(overview.keys()))
plt.bar(nOverview, overview.values(), color = "g", tick_label = "")
plt.title("Word Frequency Overview")
plt.xticks([])
#plt.savefig("overview.png")

"""
