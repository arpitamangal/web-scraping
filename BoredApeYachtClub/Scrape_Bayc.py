from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from pymongo import MongoClient
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


# # Selenium:  The Bored Ape Yacht Club 

#On https://opensea.io/collection/boredapeyachtclubLinks select all apes with “Solid gold” fur and sort them “Price high to low”. 
#Copy the resulting URL.
#Code that uses Selenium to access the resulting URL, click on each of the top-8 most expensive Bored Apes
#store the resulting details page to disk, “bayc_[N].htm”.

def saveBaycHtml():
    try: 
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(10)
        driver.set_script_timeout(120)
        driver.set_page_load_timeout(10)
        url = "https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold"
        
        time.sleep(2)
        for index in range(0,8):
            
            driver.get(url)
            time.sleep(2)
            
            ##storing all the driver elements for the search results
            elements = driver.find_elements(By.CLASS_NAME, "sc-1f719d57-0.fKAlPV.Asset--anchor")
            elements[index].click()
            time.sleep(2)
            
            ##saving page
            page = driver.page_source
            filename = "bayc_" + str(index+1) + ".htm"
            with open(filename, "w", encoding = 'utf-8') as file:
                file.write(page)
                print("Saved File:", filename)
                print("")  
            
            index = index+1
            
        driver.quit()
    except:
        print("Error in saveBaycHtml()...")


# # Save in MongoDB 
#code that goes through all 8 htm files downloaded above and stores each ape’s name (its number) and all its attributes in a document inside a MongoDB collection called “bayc”.


def storeInMongoDB():
    try: 
        # connecting to mongodb server and creating a collection named bayc
        client = MongoClient("mongodb://localhost:27017/")
        database= client["bayc"]
        table = database["bayc"]
        
        table.drop()

        for index in range(1,9):
            filename = "bayc_" + str(index) + ".htm"

            # Opening the html file
            htmlFile = open(filename, "r")

            # Reading the file
            page = htmlFile.read()

            # Creating a BeautifulSoup object and specifying the parser
            soup = BeautifulSoup(page, 'lxml')

            # printing the file name
            print("read file:", filename)

            # storing name of ape required for mongodb database
            name = soup.select("h1.sc-29427738-0.hKCSVX.item--title")[0].text

            # storing attributes of ape required for mongodb database
            attributes = soup.select("div.sc-d6dd8af3-0.hkmmpQ.item--property")
            attribute_list =[]
            for attribute in attributes:
                prop_type = attribute.select("div.Property--type")[0].text
                prop_value = attribute.select("div.Property--value")[0].text
                prop_rarity = attribute.select("div.Property--rarity")[0].text
                prop_dict ={"type": prop_type,
                            "value": prop_value,
                            "rarity": prop_rarity}
                attribute_list.append(prop_dict)

            # inserting the document in mongodb table 
            table.insert_one({"name": name, "attributes":attribute_list})
            time.sleep(2)
            
            # iterating
            index = index+1
            print("")      
        
        print(" Created MongoDB collection called bayc")
    except:
        print("Error in storeInMongoDB()...")



if __name__ == "__main__":
    

    print("Executing saveBaycHtml()...")
    saveBaycHtml()
    print("")

    print("Executing storeInMongoDB()...")
    storeInMongoDB()
    print("")
    

        
    

