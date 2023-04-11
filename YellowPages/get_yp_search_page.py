

from bs4 import BeautifulSoup
import requests
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



