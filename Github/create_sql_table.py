

import mysql.connector


## function to create database and table in SQL
def create_sql_table(SQL_DB,SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF):
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