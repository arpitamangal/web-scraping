
from bs4 import BeautifulSoup
import json
import re
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

#open the search result page "sf_pizzeria_search_page.htm" and parses out all shop information (search rank, name, linked URL [this store’s YP URL], star rating If It Exists, number of reviews IIE, TripAdvisor rating IIE, number of TA reviews IIE, “$” signs IIE, years in business IIE, review IIE, and amenities IIE).
    

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
