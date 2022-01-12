import pandas as pd
import mysql.connector as mysql
from mysql.connector.errors import Error

Recipes = pd.read_csv('C:\\Users\\USER\\Desktop\\DB workshop\\RecipesV10.csv', index_col=False, delimiter = ',')
Recipes.head()

try:
    conn = mysql.connect(host='', database='', user='', password='')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS Recipes;')
        print("table dropped if was on")
        print('Creating table Recipes:')

# in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE Recipes(RecipeID int, RecipeName CHAR(100), CookTime TIME, PrepTime TIME, TotalTime TIME, TheDescription LONGTEXT, AggregatedRating FLOAT, ReviewCount INT, RecipeServings INT, RecipeInstructions LONGTEXT, PRIMARY KEY(RecipeID))")
        print("Table Recipes has created. begin inserting:")
        #loop through the data frame   (no headers)
        for i,row in Recipes.iterrows():
            #here %S means string values 
            sql = "INSERT INTO db_workshop_V2.Recipes VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
        print("inserting complete")
except Error as e:
            print("Error while connecting to MySQL", e)