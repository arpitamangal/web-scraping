
from bs4 import BeautifulSoup
import json
import re
from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


# # MongoDB
#open the search result page "sf_pizzeria_search_page.htm" and create a MongoDB collection called “sf_pizzerias” that stores all the  shop information, one document for each shop.
    


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

    

