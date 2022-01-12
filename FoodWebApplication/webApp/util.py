from datetime import datetime, timedelta
import random


def generateRandomNumberRecipe(lowBound: int, highBound: int):
    """
    Function generate random ID number in recipe table
    :param lowBound: int
    :param highBound: int
    :return: int, random unique number for new item to insert table
    """
    from webApp.routes import sqlDB
    # Keep rolling random number until free id is found
    while True:
        randNumber = random.randint(lowBound, highBound)
        cursor = sqlDB.dbCursor
        recipeIdTuple = (randNumber,)
        query = "SELECT * FROM recipes WHERE recipeId = %s"
        cursor.execute(query, recipeIdTuple)
        number = cursor.fetchone()

        # Check if id is used in table, if not return it
        if not number:
            return randNumber


def generateRandomNumberKeyword(lowBound: int, highBound: int):
    """
    Function generate random ID number in keyword table
    :param lowBound: int
    :param highBound: int
    :return: int, random unique number for new item to insert table
    """
    from webApp.routes import sqlDB
    # Keep rolling random number until free id is found
    while True:
        randNumber = random.randint(lowBound, highBound)
        cursor = sqlDB.dbCursor
        keywordIdTuple = (randNumber,)
        query = "SELECT * FROM keywords WHERE KeywordID = %s"
        cursor.execute(query, keywordIdTuple)
        number = cursor.fetchone()

        # Check if id is used in table, if not return it
        if not number:
            return randNumber


def generateRandomNumberIngredient(lowBound: int, highBound: int):
    """
    Function generate random ID number in ingredient table
    :param lowBound: int
    :param highBound: int
    :return: int, random unique number for new item to insert table
    """
    from webApp.routes import sqlDB
    # Keep rolling random number until free id is found
    while True:
        randNumber = random.randint(lowBound, highBound)
        cursor = sqlDB.dbCursor
        IngredientIdTuple = (randNumber,)
        query = "SELECT * FROM Ingredients WHERE IngredientID = %s"
        cursor.execute(query, IngredientIdTuple)
        number = cursor.fetchone()

        # Check if id is used in table, if not return it
        if not number:
            return randNumber


def timeStringToTimedelta(time: str):
    """
    Function convert time format from string to timedelta
    :param time: str, time format in string
    :return: timedelta, time format in timedelta
    """
    t = datetime.strptime(time, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta


def parseString(inputString: str):
    """
    Function return list of elements from given string, divided by ','
    :param inputString: str
    :return: list, list of divided str elements
    """
    dividedList = inputString.split(",")
    # For each element in strip remove spaces suffix/prefix
    for value in dividedList:
        value = value.strip()
    return dividedList
