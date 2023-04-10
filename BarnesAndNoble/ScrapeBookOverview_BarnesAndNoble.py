
## Code that loads the first page with 40 items per page of “B&N Top 100” and access the overview of each book.


## Loading Packages

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from bs4 import BeautifulSoup
import requests
import time



header = {'User-Agent':'Mozilla/5.0'}
url= "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
## load url
page = requests.get(url,headers=header)
soup = BeautifulSoup(page.text, 'lxml')


##storing the list of books product page url
div = soup.select("div.product-shelf-title")
urlList =[]
for i in div:
    a=i.find_all("a")
    book_url = [element["href"] for element in a]
    urlList.append(book_url[0])
print("Length of url list:", len(urlList))



##loading each book url
index=1
for url in urlList:
    book_url = "https://www.barnesandnoble.com" + str(url)
    page = requests.get(book_url,headers=header)
    soup = BeautifulSoup(page.text, 'lxml')
    
    ##saving as htm file
    filename = "bn_top100_" + str(index) + ".htm"
    with open(filename, "w", encoding = 'utf-8') as file:
     file.write(str(soup))
    index = index +1
    print("Saved File", filename)
    time.sleep(5)


##accessing htm file from the folder and accessing overview of each book
index = 1 
while index <= 40:
    filename = "bn_top100_" + str(index) + ".htm"
    
    # Opening the html file
    htmlFile = open(filename, "r")
  
    # Reading the file
    page = htmlFile.read()
  
    # Creating a BeautifulSoup object and specifying the parser
    soup = BeautifulSoup(page, 'lxml')

    ## reading overview
    overview = soup.find_all('div',{'class': 'text--medium overview-content p-lg-4 p-sm-0 bookseller-cont'})
    
    ##printing first 100 characters of overview
    print("Overview of", filename)
    overview_text=""
    for i in overview:
        overview_text =  overview_text + " " + i.text.replace('\n', ' ').replace('\r', '').strip()
    print(overview_text[:100])
    index = index+1
    time.sleep(5)
    



