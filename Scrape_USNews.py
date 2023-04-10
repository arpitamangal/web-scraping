
# ## Loading page https://www.usnews.com/


from bs4 import BeautifulSoup
import requests
header = {'User-Agent':'Mozilla/5.0'}
url= "https://www.usnews.com/"
page = requests.get(url,headers=header)
soup = BeautifulSoup(page.text, 'lxml')


# ### read + print the URL of the _second_ current top story to the screen (terminal)


##reading top stories 
top_stories_div = soup.find("div",class_="Box-w0dun1-0 ArmRestTopStories__Container-s0vo7p-0 dWWnRo jkIDND")
top_stories_a = top_stories_div.find_all("a")



##accessing urls for top stories
urls = [element["href"] for element in top_stories_a]
urls


##filtering to keep only unique urls
import numpy as np
indexes = np.unique(urls, return_index=True)[1]
urls_unq=[urls[index] for index in sorted(indexes)]
urls_unq

##accessing the url for second top story
urls_unq[1]


# ### load that page of second top story


##loading url for second top story
url_1= urls_unq[1]
page_1 = requests.get(url_1,headers=header)
soup_1 = BeautifulSoup(page_1.text, 'lxml')


# ### read + print the header as well as the first 3 sentences of the main body to the screen
# 

##reading header 
header = soup_1.find("h1",class_="Heading-sc-1w5xk2o-0 iQhOvV")
## printing header
print(header.text)



## reading main body
body = soup_1.find("div",class_="Box-w0dun1-0 article-body__ArticleBox-sc-138p7q2-2 dWWnRo eYFKbH")
## printing first 3 sentences of main body
index = 0
for i in body:
    if len(i.text) != 0 :
        print(i.text)
        index = index+ 1
    if index == 3 :
        break

