

# # Go to Apache Hadoop Github Repo's contributors’ endpoint https://api.github.com/repos/apache/hadoop/contributors. Extract the JSON corresponding to the first 100 contributors from this API. Store the information as a SQL database.

import get_user_information
import create_sql_table
import insert_data_sql_table
import create_index_sql_table
import warnings


def main():
    #store the user information as list
    value_list = get_user_information.get_user_information()
    
    #ignore warnings
    warnings.filterwarnings("ignore")
    SQL_DB = "ucdavis"

    ##setting the data types for the SQL table
    SQL_TABLE_URBAN = "hadoop_contributors"
    SQL_TABLE_URBAN_DEF = "(" +                 "login VARCHAR(50)" +                ",id INT NOT NULL PRIMARY KEY" +                 ",location VARCHAR(100)" +                 ",email VARCHAR(50)" +                 ",hireable VARCHAR(50)" +                 ",bio TEXT" +                 ",twitter_username VARCHAR(50)" +                 ",public_repos INT" +                 ",public_gists INT" +                 ",followers INT" +                 ",following INT" +                 ",created_at VARCHAR(50)" +                 ")"

    ##creating table
    create_sql_table.create_sql_table(SQL_DB,SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF)

    ##inserting values to the table
    insert_data_sql_table.insert_data_sql_table(SQL_TABLE_URBAN, SQL_TABLE_URBAN_DEF,value_list)

    #creating index in already existing column
    create_index_sql_table.create_index_sql_table(SQL_DB,SQL_TABLE_URBAN,"login")
    create_index_sql_table.create_index_sql_table(SQL_DB,SQL_TABLE_URBAN,"location")
    create_index_sql_table.create_index_sql_table(SQL_DB,SQL_TABLE_URBAN,"hireable")



if __name__ == '__main__':
    main()
    
    

