from datetime import datetime, timedelta
import random


class PageResult:
    def __init__(self, data, page=1, number=20):
        self.__dict__ = dict(zip(['data', 'page', 'number'], [data, page, number]))
        self.full_listing = [self.data[i:i + number] for i in range(0, len(self.data), number)]

    def __iter__(self):
        for i in self.full_listing[self.page - 1]:
            yield i

    def __repr__(self):  # used for page linking
        return "/displayitems/{}".format(self.page + 1)  # view the next page


def generateRandomNumber(lowBound: int, highBound: int):    # todo make recipes-table as %s
    from webApp.routes import sqlDB
    while True:
        randNumber = random.randint(lowBound, highBound)
        cursor = sqlDB.dbCursor
        recipeIdTuple = (randNumber,)
        query = "SELECT * FROM recipes WHERE recipeId = %s"
        cursor.execute(query, recipeIdTuple)
        number = cursor.fetchone()
        if not number:
            return randNumber


def timeStringToTimedelta(time: str):
    t = datetime.strptime(time, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta


def parseString(inputString: str):
    dividedList = inputString.split(",")
    for value in dividedList:
        value = value.strip()
    return dividedList
