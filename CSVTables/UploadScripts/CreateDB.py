import pandas as pd
import mysql.connector as mysql
from mysql.connector.errors import Error



try:
    db = mysql.connect(
        host="",
        user="",
        passwd=""
    )
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE db_workshop_V2")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)