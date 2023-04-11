
import mysql.connector


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