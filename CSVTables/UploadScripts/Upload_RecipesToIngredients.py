import pandas as pd
import mysql.connector as mysql
from mysql.connector.errors import Error


RecipesToIngredients = pd.read_csv('C:\\Users\\USER\\Desktop\\DB workshop\\RecipesToIngredientsV4.csv', index_col=False, delimiter = ',', encoding= 'unicode_escape')
RecipesToIngredients.head()
try:
    conn = mysql.connect(host='', database='', user='', password='')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS RecipesToIngredients;')
        print('Creating table RecipesToIngredients:')

# in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE RecipesToIngredients(RecipeID int, IngredientID int, RecipeIngredientQuantities char(50), PRIMARY KEY(RecipeID, IngredientID))")
        print("Table RecipesToIngredients has created. begin inserting:")
        #loop through the data frame   (no headers)
        for i,row in RecipesToIngredients.iterrows():
            #here %S means string values 
            sql = "INSERT INTO db_workshop_V2.RecipesToIngredients VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            # print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
        print("inserting complete")
except Error as e:
            print("Error while connecting to MySQL", e)