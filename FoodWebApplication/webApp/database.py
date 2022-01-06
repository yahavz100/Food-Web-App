import mysql.connector
from mysql.connector import Error


class DatabaseSQL:
    def __init__(self):
        try:
            self.dbConnection = mysql.connector.connect(
                    host="localhost",
                    user="team16",
                    passwd="0016",
                    database="db_workshop_v2"
                )
            if self.dbConnection.is_connected():
                print("Connection to mySQL database server success", self.dbConnection.get_server_info())
            else:
                print("Not connected to mySQL")
        except Error as e:
            print("Error while connecting to mySQL", e)
        self.dbCursor = self.dbConnection.cursor()

