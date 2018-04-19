from pymongo import MongoClient
from pymongo import ReadPreference


class Database:

    def __init__(self):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        self.dataTrain = client.Reconnaissance_Chiffre.get_collection("DataTrain")
        self.confusionMatrix = client.Reconnaissance_Chiffre.get_collection("ConfusionMatrix")
        self.dataTest = client.Reconnaissance_Chiffre.get_collection("DataTest")

    def insertDataTrain (self, data):
        self.dataTrain.insert(data)
    
    def getAllDataTrain(self):
        return list(self.dataTrain.find())

    def addMatrix(self, methodName, matrix):
        result = self.confusionMatrix.find_one({"method":methodName})
        self.confusionMatrix.insert({"method":methodName, "matrix":matrix}) if not result else self.confusionMatrix.find_and_modify({"method":methodName, "matrix":matrix}) 
        return True

    def getMatrix(self, methodName):
        matrix = self.confusionMatrix.find_one({"method": methodName})
        return matrix["matrix"]

    def getAllMatrix(self):
        return list(self.confusionMatrix.find())

    def getAllDataTest(self):
        return list(self.dataTest.find())

    def ImportDataTest(self, datas):
        #TO DO
        print(datas)
        

db = Database()