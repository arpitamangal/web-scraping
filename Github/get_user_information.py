


from bs4 import BeautifulSoup
import requests
import time
import json
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


#On Github generate a personal access token and store in variable personal_access_token
personal_access_token = 'personal_access_token'


def get_json_response():
    try:
        url = "https://api.github.com/repos/apache/hadoop/contributors"
        #The API request is a GET request and the variable name that handles the items per page is "per_page"
        response = requests.get(url,
                                headers=headers,params={'per_page': 100},
                                auth=('ArpitaMangal',personal_access_token))
        json_response = response.json()
        print("Stored json response")
        return json_response
    except:
      print("Problem with the connection...")


# # For each of the 100 contributors extracted, write code that accesses their user information and extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", "followers", "following", "created_at" (and print those to screen)


def get_user_information():
    try: 
        json_response = get_json_response()
        key_list = ["login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", "followers", "following", "created_at"]
        value_list = []
        k=1
        for i in json_response:
            url = i['url']
            page = requests.get(url,
                                headers=headers,
                                auth=('ArpitaMangal',personal_access_token))
            doc = BeautifulSoup(page.content, 'html.parser')
            json_dict = json.loads(str(doc))
            value=[]
            print("Contributor# :", k)
            for key in key_list:
                print(key,":", json_dict[key])
                value.append(json_dict[key])
            print(" ")
            value_list.append(value)
            k=k+1
            time.sleep(10)
        return value_list
    except:
        print("Problem with scraping user information...")