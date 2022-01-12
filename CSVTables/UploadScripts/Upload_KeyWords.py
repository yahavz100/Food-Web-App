import pandas as pd
import mysql.connector as mysql
from mysql.connector.errors import Error


KeyWords = pd.read_csv('C:\\Users\\USER\\Desktop\\DB workshop\\KeywordsV2.csv', index_col=False, delimiter = ',')
KeyWords.head()

try:
    conn = mysql.connect(host='', database='', user='', password='')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS Keywords;')
        print('Creating table Keywords:')

# in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE Keywords(KeywordID int, KeywordName char(80), PRIMARY KEY(KeywordID))")
        print("Table Keywords has created. begin inserting:")
        #loop through the data frame   (no headers)
        for i,row in KeyWords.iterrows():
            #here %S means string values 
            sql = "INSERT INTO db_workshop_V2.Keywords VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
        print("inserting complete")
except Error as e:
            print("Error while connecting to MySQL", e)