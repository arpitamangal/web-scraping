## Locate Pizzeria in San Francisco
Scrape resturant information, their geolocation and save in MongoDB : Yellow Pages and Position Stack

### Scrape Shop Information
Search on yellowpages.com for the top 30 “Pizzeria” in San Francisco and save the page as, “sf_pizzeria_search_page.htm”.

From the saved page, parse out all shop information (search rank, name, linked URL [this store’s YP URL], star rating If It Exists, number of reviews IIE, TripAdvisor rating IIE, number of TA reviews IIE, “$” signs IIE, years in business IIE, review IIE, and amenities IIE).

### Save in MongoDB    
Create a MongoDB collection called “sf_pizzerias” that stores all the extracted shop information, one document for each shop.


### Get address and geolocation 

Download each shop's page (stored as linked UR). Store the page to disk, “sf_pizzerias_[SR].htm” (where [SR] is the search rank). Parse each shop’s address, phone number, and website

Signup on  https://positionstack.com/ and get access key for API call.

Query each shop address’from shop page and get geolocation (long, lat) from https://positionstack.com/.  Update each shop document on the MongoDB collection “sf_pizzerias” to contain the shop’s address, phone number, website, and geolocation.
    
    

