import json
from os import path

class Settings():
    def __init__(self, filename):
        self.__filename = filename
        self.__data = {}

    def hasSettings(self):
        return path.isfile(self.__filename)

    def setTitle(self, title):
        self.__data[title] = {}

    def setSettings(self, title, **data):
        print (data)
        self.__data[title] = data

    def getSettings(self, title=None):
        with open(self.__filename, 'r+') as file:
            self.__data = json.load(file)

        if title is not None:
            data = self.__data[title]
        else:
            data = self.__data

        return data

    def save(self):
        with open(self.__filename, 'w+') as file:
            json.dump(self.__data, file, indent=4)
