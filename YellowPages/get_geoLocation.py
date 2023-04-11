from bs4 import BeautifulSoup
import requests
import time
import json

from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


access_key ='access_key'

# # API
#query each shop address’from shop page and get geolocation (long, lat) from https://positionstack.com/.  Update each shop document on the MongoDB collection “sf_pizzerias” to contain the shop’s address, phone number, website, and geolocation.
    

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
                                params={"access_key": access_key,
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

