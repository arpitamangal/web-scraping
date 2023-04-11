
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


# # Parsing
#read the 30 shop pages saved and parse each shop’s address, phone number, and website
    

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


