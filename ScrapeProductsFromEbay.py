#!/usr/bin/env python
# coding: utf-8

# In[20]:


#Loading Packages¶
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
import numpy as np
header = {'User-Agent':'Mozilla/5.0'}


# In[21]:


#function to loads eBay's search result page 
def load_page(url,pgn):
    URL = url + str(pgn)
    page = requests.get(URL,headers=header)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup


# In[22]:


#function to save the loaded page as htm in local
def save_page(index,soup):
    filename = "amazon_gift_card_" + str(index) + ".htm"
    with open(filename, "w", encoding = 'utf-8') as file:
     file.write(str(soup))
    print("Saved File:", filename)


# In[23]:


#function to load file from folder and parses them to a Python object.
def load_file(index):
    filename = "amazon_gift_card_" + str(index) + ".htm"
    
    # Opening the html file
    htmlFile = open(filename, "r")
  
    # Reading the file
    page = htmlFile.read()
  
    # Creating a BeautifulSoup object and specifying the parser
    soup = BeautifulSoup(page, 'lxml')
    #div = soup.find_all('div',{'class': 's-item__info clearfix'})
    div = soup.select('#srp-river-results div.s-item__info')
    print("Filename:", filename)
    return div


# In[27]:


#function to print title, price and shipping
def print_details(df,i):
    title = i.select("div.s-item__title > span")[0].text
    price = i.select("span.s-item__price")[0].text
    print("Title:", title )
    print("Price:", price)
    for j in i.select("span.s-item__shipping.s-item__logisticsCost"):
        shipping = j.text
        print("Shipping:", shipping)
        df.loc[len(df.index)] = [title, price, shipping]


# In[25]:


#function to get values using regex 
def regex_sub(text):
    return re.sub(".*?([.0-9]+).*",r"\1",text)


# In[28]:


def main():
    try:
        
        ##loading each book url
        url = "https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&LH_Sold=1&_pgn="
        pgn=1
        while pgn<=10:
            ##Loading Pages
            soup = load_page(url,pgn)
            ##saving as htm file
            save_page(pgn,soup)
            pgn = pgn +1
            time.sleep(10)


        ##creating dataframe to save the title, price and shipping
        df = pd.DataFrame(columns=['Title', 'Price', 'Shipping'])
        ##looping htm file from the folder and parses them to a Python and printing
        index = 1
        while index <= 10:
            div = load_file(index)
            item=1
            for i in div:
                print("item #:", item)
                print_details(df,i)
                print(" ")
                item = item +1
            index = index+1


        ##getting values from the text using regex
        df['Value'] = df['Title'].apply(regex_sub)
        df['Price_int'] = df['Price'].apply(regex_sub)
        df['Shipping_int'] = df['Shipping'].apply(regex_sub)

        df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0).astype(float)
        df['Price_int'] = pd.to_numeric(df['Price_int'], errors='coerce').fillna(0).astype(float)
        df['Shipping_int'] = pd.to_numeric(df['Shipping_int'], errors='coerce').fillna(0).astype(float)

        ##Insights from scraped Data 

        #What fraction of Amazon gift cards sells above face value? Why do you think this is the case?
        
        
        print("Total items:", df.shape)
        print("Value Unknown:", df[df['Value']==0].shape)
        print("Price Unknown:", df[df['Price_int']==0].shape)
        print("Shipping Free:", df[df['Shipping_int']==0].shape)

        df1=df[df['Value']!=0]

        df1['TotalPrice'] =  df1['Price_int'] + df1['Shipping_int']

        df1['SellsAboveValueFlg']=np.where((df1['Value'] < df1['TotalPrice']),1,0 )
        frac = df1['SellsAboveValueFlg'].sum()/df1['SellsAboveValueFlg'].count()
        print("Fraction of Amazon gift cards sells above face value:", frac)

    except:
        print("Problem with the connection...")

if __name__ == '__main__':
    main()


# In[ ]:




