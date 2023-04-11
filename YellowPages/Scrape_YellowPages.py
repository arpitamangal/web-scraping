#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from bs4 import BeautifulSoup
import requests
import time
import json
import re
from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}



#Search on yellowpages.com for the top 30 “Pizzeria” in San Francisco.  Save the search result page to disk, “sf_pizzeria_search_page.htm”.
def get_yp_search_page():
    try:
        url = "https://www.yellowpages.com/search?"
        #Yellow Pages uses GET requests for its search. 
        page = requests.get(url,
                            headers=headers,
                            params={"search_terms": "Pizzeria",
                                    "geo_location_terms": "San Francisco",
                                    "s":"default"})
        soup = BeautifulSoup(page.text, 'lxml')

        filename = "sf_pizzeria_search_page.htm"
        with open(filename, "w", encoding = 'utf-8') as file:
            file.write(str(soup))
            print("Saved File:", filename)
    except:
        print("Error in get_yp_search_page()...")
        
    return



def parse_yp_shop_info():
    
    try: 
        filename = "sf_pizzeria_search_page.htm"

        # Opening the html file
        htmlFile = open(filename, "r")

        # Reading the file
        page = htmlFile.read()

        # Creating a BeautifulSoup object and specifying the parser
        soup = BeautifulSoup(page, 'lxml')
        
        search_results = soup.select("div.search-results.organic div.result")
        
        #parsing out all shop information 
        for result in search_results:
            print("search_rank:", json.loads(result["data-analytics"])["rank"])

            print("name:", result.select_one("a.business-name span").text)

            print("linked_url:" , result.select_one("a.business-name")["href"])

            extra_rating = result.select_one("a.rating.hasExtraRating")
            if extra_rating is not None:
                print("star_rating:" , extra_rating.select_one("div.result-rating")["class"][1])
                print("num_reviews:" , extra_rating.select_one("span.count").text)

            tripadvisor = result.select_one("div.ratings")
            if bool(re.search("data-tripadvisor", str(tripadvisor))):
                print("ta_rating:" , json.loads(tripadvisor["data-tripadvisor"])["rating"])
                print("ta_reviews:" , json.loads(tripadvisor["data-tripadvisor"])["count"])

            priceRange = result.select_one("div.price-range")
            if priceRange is not None:
                dollar_signs = priceRange.text
                if len(dollar_signs)!=0: print("dollar_signs:" ,dollar_signs)

            years = result.select_one("div.years-in-business div.number")
            if years is not None: print("years_in_business:" , years.text)

            review_soup = result.select_one("p.body.with-avatar")
            if review_soup is not None: print("review:" , review_soup.text)
            
            amenities = [element.text for element in result.select("div.amenities-info span")]
            if len(amenities)!= 0: print("amenities:" , amenities)
                
            print("----------------")
        print(" Parsed shop information... ")
            
    except:
        print("Error in parse_yp_shop_info()...")
    
    return


# # MongoDB


def save_yp_shop_info_mongoDB():
    try: 
        filename = "sf_pizzeria_search_page.htm"

        # Opening the html file
        htmlFile = open(filename, "r")

        # Reading the file
        page = htmlFile.read()

        # Creating a BeautifulSoup object and specifying the parser
        soup = BeautifulSoup(page, 'lxml')
        
        search_results = soup.select("div.search-results.organic div.result")
        
        client = MongoClient("mongodb://localhost:27017/")
        database= client["sf_pizzerias"]
        table = database["sf_pizzerias"]
        
        table.drop()
        
        #parsing out all shop information 
        for result in search_results:
            
            search_rank = json.loads(result["data-analytics"])["rank"]

            name =  result.select_one("a.business-name span").text

            linked_url =  result.select_one("a.business-name")["href"]

            # inserting the document in mongodb table 
            table.insert_one({"search_rank": str(search_rank), "name": name, "linked_url" : linked_url})

            query_doc = { "search_rank": str(search_rank)}

            extra_rating = result.select_one("a.rating.hasExtraRating")
            if extra_rating is not None:
                star_rating =  extra_rating.select_one("div.result-rating")["class"][1]
                num_reviews =  extra_rating.select_one("span.count").text
                table.update_one(query_doc, {"$set": {"star_rating": star_rating, "num_reviews":num_reviews}})


            tripadvisor = result.select_one("div.ratings")
            if bool(re.search("data-tripadvisor", str(tripadvisor))):
                ta_rating =  json.loads(tripadvisor["data-tripadvisor"])["rating"]
                ta_reviews =  json.loads(tripadvisor["data-tripadvisor"])["count"]
                table.update_one(query_doc, {"$set": {"ta_rating": ta_rating, "ta_reviews":ta_reviews}})

            priceRange = result.select_one("div.price-range")
            if priceRange is not None:
                dollar_signs = priceRange.text
                if len(dollar_signs)!=0:
                    table.update_one(query_doc, {"$set": {"dollar_signs": dollar_signs}})


            years = result.select_one("div.years-in-business div.number")
            if years is not None:
                years_in_business =  years.text
                table.update_one(query_doc, {"$set": {"years_in_business": years_in_business}})

            review_soup = result.select_one("p.body.with-avatar")
            if review_soup is not None:
                review =  review_soup.text
                table.update_one(query_doc, {"$set": {"review": review}})


            amenities = [element.text for element in result.select("div.amenities-info span")]
            if len(amenities)!= 0:
                table.update_one(query_doc, {"$set": {"amenities": amenities}})
        print(" Created MongoDB collection called sf_pizzerias")
    except:
        print("Error in save_yp_shop_info_mongoDB()...")
        
    return

    

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


# # Parsing

def parse_shop_page():
    try:
        for rank in range (1,31):

            filename = "sf_pizzerias_" + str(rank) + ".htm"

            # Opening the html file
            htmlFile = open(filename, "r")

            # Reading the file
            page = htmlFile.read()

            # Creating a BeautifulSoup object and specifying the parser
            soup = BeautifulSoup(page, 'lxml')
            
            print("read file:",filename)
            print("address:", soup.select_one("span.address span").text)
            print("phone_number:", soup.select_one("a.phone.dockable strong").text)
            
            website = soup.select_one("a.website-link.dockable")
            if website is not None: print("website:", website['href'])

            print("")
            rank = rank+1
    except:
        print("Error in parse_shop_page()...")
        
    return


# # API

def get_geoLocation():
    try:
        dict_list =[]
        for rank in range (1,31):

            filename = "sf_pizzerias_" + str(rank) + ".htm"

            # Opening the html file
            htmlFile = open(filename, "r")

            # Reading the file
            page = htmlFile.read()

            # Creating a BeautifulSoup object and specifying the parser
            soup = BeautifulSoup(page, 'lxml')
            
            print("filename:",filename)
            address = soup.select_one("span.address span").text
            phone_number = soup.select_one("a.phone.dockable strong").text
            print("address:", address)
            print("phone_number:", phone_number)
            
            shop_dict={"address":address,"phone_number":phone_number}
            
            website = soup.select_one("a.website-link.dockable")
            if website is not None: 
                print("website:", website['href'])
                shop_dict["website"] = website['href']
                
            url = "http://api.positionstack.com/v1/forward"

            page = requests.get(url,
                                headers=headers,
                                params={"access_key": '017190dde2be06740a21022b539da32d',
                                        "query": address})
            doc = BeautifulSoup(page.content, 'html.parser')
            json_dict = json.loads(str(doc))
            latitude = json_dict["data"][0].get("latitude")
            longitude = json_dict["data"][0].get("longitude")
            print("latitude:", latitude)
            print("longitude:", longitude)
            
            shop_dict["geolocation"] = {"latitude":latitude,
                                       "longitude":longitude}

            dict_list.append(shop_dict)
            print("")
            rank = rank+1
            time.sleep(1)
    
        client = MongoClient("mongodb://localhost:27017/")
        database= client["sf_pizzerias"]
        table = database["sf_pizzerias"]
        
        for rank in range (1,31):
            query_doc = { "search_rank": str(rank)}
            table.update_one(query_doc, {"$set": dict_list[rank-1]})
            rank = rank+1
            
        print(" Updated MongoDB collection called sf_pizzerias")
    except:
        print("Error in get_geoLocation()...")
    
    return

if __name__ == "__main__":
    
    #Search on yellowpages.com for the top 30 “Pizzeria” in San Francisco.  Save the search result page to disk, “sf_pizzeria_search_page.htm”.
    print("Executing get_yp_search_page()...")
    get_yp_search_page()
    print("")
    
    #open the search result page "sf_pizzeria_search_page.htm" and parses out all shop information (search rank, name, linked URL [this store’s YP URL], star rating If It Exists, number of reviews IIE, TripAdvisor rating IIE, number of TA reviews IIE, “$” signs IIE, years in business IIE, review IIE, and amenities IIE).
    print("Executing parse_yp_shop_info()...")
    parse_yp_shop_info()
    print("")
    
    
    #open the search result page "sf_pizzeria_search_page.htm" and create a MongoDB collection called “sf_pizzerias” that stores all the extracted shop information, one document for each shop.
    print("Executing save_yp_shop_info_mongoDB()...")
    save_yp_shop_info_mongoDB()
    print("")
    
    
    #read all URLs stored in “sf_pizzerias” database and download each shop page. Store the page to disk, “sf_pizzerias_[SR].htm” (where [SR] is the search rank).
    print("Executing download_shop_page()...")
    download_shop_page()
    print("")
    
    #read the 30 shop pages saved and parse each shop’s address, phone number, and website
    print("Executing parse_shop_page()...")
    parse_shop_page()
    print("")
    
    #query each shop address’from shop page and get geolocation (long, lat) from https://positionstack.com/.  Update each shop document on the MongoDB collection “sf_pizzerias” to contain the shop’s address, phone number, website, and geolocation.
    print("Executing get_geoLocation()...")
    get_geoLocation()
    print("")
    
        
    

