
import mysql.connector

##function to create index in an existing column
#When we index a column in SQL, SQL first sorts the data using the index and the uses binary serach on sorted array to perform a  search operation. This reduced the complexity of search operation making it faster to execute the where statement.
def create_index_sql_table(SQL_DB,SQL_TABLE_URBAN,column):
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
