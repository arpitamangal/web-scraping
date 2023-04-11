

# # Go to Apache Hadoop Github Repo's contributors’ endpoint https://api.github.com/repos/apache/hadoop/contributors. Extract the JSON corresponding to the first 100 contributors from this API. Store the information as a SQL database.

from bs4 import BeautifulSoup
import requests
import time
import json
import mysql.connector
import warnings
import codecs
headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


#On Github generate a personal access token and store in variable personal_access_token
# personal_access_token = 'personal access token'

personal_access_token = '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'


def get_json_response():
    try:
        url = "https://api.github.com/repos/apache/hadoop/contributors"
        contributors = str(100)
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



## function to create database and table in SQL
def create_sql_table(SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF):
    try:
        
        #connect to server
        conn = mysql.connector.connect(host='localhost',
                                            user='root',
                                            password='password')
        cursor = conn.cursor()
        
        #creating database
        query = "CREATE DATABASE IF NOT EXISTS " + SQL_DB
        print(query)
        cursor.execute(query);
        
        #Doping table if already exists
        query = "DROP TABLE IF EXISTS " + SQL_DB + "." + SQL_TABLE_URBAN + " ;"
        cursor.execute(query)
        print(query)
        
        #Creating table
        query = "CREATE TABLE IF NOT EXISTS " + SQL_DB + "." + SQL_TABLE_URBAN + " " + SQL_TABLE_URBAN_DEF + ";";
        print(query)
        cursor.execute(query);
        
        
        cursor.close()
        conn.close()
        return
    except IOError as e:
        print(e)


##function to insert values to the table
def insert_data_sql_table(SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF,value_list):
    try:
        #connect to server
        conn = mysql.connector.connect(host='localhost',
                                            database='ucdavis',
                                            user='root',
                                            password='password')
        cursor = conn.cursor()
        
        #To create database, we choose datatypes for each for the variables. For "login" the value was a mix of alphabets and numbers, so we choose a datatype VARCHAR but the login name is not too long hance setting the size to 50. Location has a mix of alphabets, characters hence again choosing VARCHAR. SImilary for email, and twitter_username. id, public_repos, public_gists, followers, following take numberic values, hence setting the data type as INT. Bio is lengthy string and choosing the data type Text. The field created_at take the date time value with t and z and so choosing the datatype VARCHAR. 
        #Setting id as the Primary key, as id is unique to a contributor, there are no null values. Additionally, it is a numerical value, would make search options and merge operations easier and faster.
        
        #parametrized version
        parameterized_stmt = "INSERT INTO " + SQL_TABLE_URBAN + """
        (login, id, location, email, hireable, bio, twitter_username, 
        public_repos, public_gists, followers, following, created_at)  
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        k=1
        for value in value_list:
            #parameterized version
            print("Contributor# :", k)
            cursor.execute(parameterized_stmt, value)
            k=k+1
        conn.commit()
        cursor.close()
        conn.close()
    except IOError as e:
        print(e)       


##function to create index in an existing column
#When we index a column in SQL, SQL first sorts the data using the index and the uses binary serach on sorted array to perform a  search operation. This reduced the complexity of search operation making it faster to execute the where statement.
def create_index_sql_table(SQL_TABLE_URBAN,column):
    try:
        
        #connect to server
        conn = mysql.connector.connect(host='localhost',
                                            user='root',
                                            password='password')
        cursor = conn.cursor()
        
        
        query = "CREATE INDEX "+ column + "_index ON "+ SQL_DB + "." + SQL_TABLE_URBAN + " (" + column + ")"
        print(query)
        cursor.execute(query);
        
        cursor.close()
        conn.close()
        return
    except IOError as e:
        print(e)


if __name__ == '__main__':
    
    #store the user information as list
    value_list = get_user_information()
    
    #ignore warnings
    warnings.filterwarnings("ignore")
    SQL_DB = "ucdavis"

    ##setting the data types for the SQL table
    SQL_TABLE_URBAN = "hadoop_contributors"
    SQL_TABLE_URBAN_DEF = "(" +                 "login VARCHAR(50)" +                ",id INT NOT NULL PRIMARY KEY" +                 ",location VARCHAR(100)" +                 ",email VARCHAR(50)" +                 ",hireable VARCHAR(50)" +                 ",bio TEXT" +                 ",twitter_username VARCHAR(50)" +                 ",public_repos INT" +                 ",public_gists INT" +                 ",followers INT" +                 ",following INT" +                 ",created_at VARCHAR(50)" +                 ")"

    ##creating table
    create_sql_table(SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF)

    ##inserting values to the table
    insert_data_sql_table(SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF,value_list)

    #creating index in already existing column
    create_index_sql_table(SQL_TABLE_URBAN,"login")
    create_index_sql_table(SQL_TABLE_URBAN,"location")
    create_index_sql_table(SQL_TABLE_URBAN,"hireable")

