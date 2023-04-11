from bs4 import BeautifulSoup
import requests
import time

from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

#read all URLs stored in “sf_pizzerias” database and download each shop page. Store the page to disk, “sf_pizzerias_[SR].htm” (where [SR] is the search rank).
    
def download_shop_page():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        database= client["sf_pizzerias"]
        table = database["sf_pizzerias"]
        
        for record in table.find():
            url = "https://www.yellowpages.com" + record["linked_url"]
            page = requests.get(url,headers=headers)
            soup = BeautifulSoup(page.text, 'lxml')
            
            filename = "sf_pizzerias_" + record["search_rank"] + ".htm"
            with open(filename, "w", encoding = 'utf-8') as file:
                file.write(str(soup))
                print("Saved File:", filename)
            time.sleep(10)
    except:
        print("Error in download_shop_page()...")
        
    return


