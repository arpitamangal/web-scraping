# ## Loading page  https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390 



from bs4 import BeautifulSoup
import requests
header = {'User-Agent':'Mozilla/5.0'}
url= "https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390"
page = requests.get(url,headers=header)
soup = BeautifulSoup(page.text, 'lxml')


# ### Accessing List price and saving to string


##reading the list price
list_price_html = soup.select("p.list-price span.sr-only")
##printing and saving list price
for i in list_price_html: 
    list_price = i.text
    print(list_price)


# ### Accessing Current Price and saving to string

##reading the final price
final_price_html = soup.select("p.final-price span.sr-only")
##printing and saving current price
for i in final_price_html:
    final_price = i.text
    print(i.text)


# ### Python's (or Java's) regex (!!) functionality to convert the prices to "1234.56" (no dollar sign, comma, just a "." separator for cents)


##printing the list price to check for regex format
list_price


##editing format of list price using regex
import re
re.sub(".([0-9]).([0-9]{3})\s+.*?([0-9]{2}).*\s+", r"\1\2.\3",list_price)


##printing the current price to check for regex format
final_price 



##editing format of current price using regex
re.sub(".([0-9]).([0-9]{3})\s+.*?([0-9]{2}).*\s+", r"\1\2.\3",final_price)


# ### print both, the list price and the current price to screen / terminal


print(re.sub(".([0-9]).([0-9]{3})\s+.*?([0-9]{2}).*\s+", r"\1\2.\3",list_price))


print(re.sub(".([0-9]).([0-9]{3})\s+.*?([0-9]{2}).*\s+", r"\1\2.\3",final_price))

