from pymongo import MongoClient
from pymongo import ReadPreference


class Database:

    def __init__(self):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        self.collection = client.Reconnaissance_Chiffre.get_collection("DataTrain")

    def insertTrainData (self, data):
        self.collection.insert(data)
    
    def getAllTrainData(self):
        return list(self.collection.find())

db = Database()