import get_yp_search_page
import parse_yp_shop_info
import save_yp_shop_info_mongoDB
import download_shop_page
import parse_shop_page
import get_geoLocation



def main():
    #Search on yellowpages.com for the top 30 “Pizzeria” in San Francisco.  Save the search result page to disk, “sf_pizzeria_search_page.htm”.
    print("Executing get_yp_search_page()...")
    get_yp_search_page.get_yp_search_page()
    print("")
    
    #open the search result page "sf_pizzeria_search_page.htm" and parses out all shop information (search rank, name, linked URL [this store’s YP URL], star rating If It Exists, number of reviews IIE, TripAdvisor rating IIE, number of TA reviews IIE, “$” signs IIE, years in business IIE, review IIE, and amenities IIE).
    print("Executing parse_yp_shop_info()...")
    parse_yp_shop_info.parse_yp_shop_info()
    print("")
    
    
    #open the search result page "sf_pizzeria_search_page.htm" and create a MongoDB collection called “sf_pizzerias” that stores all the extracted shop information, one document for each shop.
    print("Executing save_yp_shop_info_mongoDB()...")
    save_yp_shop_info_mongoDB.save_yp_shop_info_mongoDB()
    print("")
    
    
    #read all URLs stored in “sf_pizzerias” database and download each shop page. Store the page to disk, “sf_pizzerias_[SR].htm” (where [SR] is the search rank).
    print("Executing download_shop_page()...")
    download_shop_page.download_shop_page()
    print("")
    
    #read the 30 shop pages saved and parse each shop’s address, phone number, and website
    print("Executing parse_shop_page()...")
    parse_shop_page.parse_shop_page()
    print("")
    
    #query each shop address’from shop page and get geolocation (long, lat) from https://positionstack.com/.  Update each shop document on the MongoDB collection “sf_pizzerias” to contain the shop’s address, phone number, website, and geolocation.
    print("Executing get_geoLocation()...")
    get_geoLocation.get_geoLocation()
    print("")


if __name__ == "__main__":
    main()
    
    