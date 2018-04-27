from pymongo import MongoClient
from pymongo import ReadPreference
import csv

def deplacementImage(image, direction, largeur, hauteur):
    x = len(image)
    profondeur = 0
    imageRet = []
    if direction == 1:
        for i in range(0, x):
            if (i + 1) % largeur == 0:
                imageRet.append(image[largeur * profondeur])
                profondeur += 1
            else:
                imageRet.append(image[i + 1])
    elif direction == 2:
        for i in range(0, x):
            if (i < x):
                imageRet.append(image[0 - largeur + profondeur])
                profondeur += 1
            else:
                imageRet.image[i - largeur]
    return imageRet


class Database:
    def __init__(self):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        self.dataTrain = client.Reconnaissance_Chiffre.get_collection("DataTrain")
        self.confusionMatrix = client.Reconnaissance_Chiffre.get_collection("ConfusionMatrix")
        self.dataTest = client.Reconnaissance_Chiffre.get_collection("DataTest")
        self.poids = client.Reconnaissance_Chiffre.get_collection("Poids")

    def insertDataTrain(self, data):
        self.dataTrain.insert(data)

    def getAllDataTrain(self):
        return list(self.dataTrain.find())

    def addMatrix(self, methodName, matrix):
        result = self.confusionMatrix.find_one({"method": methodName})
        self.confusionMatrix.insert(
            {"method": methodName, "matrix": matrix}) if not result else self.confusionMatrix.find_and_modify(
            {"method": methodName}, {"method": methodName, "matrix": matrix})
        return True

    def removeMatrix(self):
        self.confusionMatrix.delete_one({"method": "kmeans"})
        self.confusionMatrix.delete_one({"method": "bayesienne"})
        self.confusionMatrix.delete_one({"method": "neural"})
        self.confusionMatrix.delete_one({"method": "all"})
        
    def getMatrix(self, methodName):
        matrix = self.confusionMatrix.find_one({"method": methodName})
        if matrix is None:
            return [[0 for i in range(10)] for j in range(10)]
        return matrix["matrix"]

    def getAllMatrix(self):
        r = []
        for l in self.confusionMatrix.find():
            del l["_id"]
            r.append(l)
        return r

    def duplicateAllDB(self):
        all = db.getAllDataTrain()
        for d in all:
            img = d['data']
            for i in range(6):
                for j in range(8):
                    img = deplacementImage(img, 2, 6, 8)
                    doNotDuplicate = db.getAllDataTrain()
                    for x in doNotDuplicate:
                        if x['data'] == img:
                            break
                    else:
                        self.insertDataTrain({'data': img, 'solution': d['solution']})

                    img = deplacementImage(img, 1, 6, 8)
                    doNotDuplicate = db.getAllDataTrain()
                    for x in doNotDuplicate:
                        if x['data'] == img:
                            break
                    else:
                        self.insertDataTrain({'data': img, 'solution': d['solution']})


    def getAllDataTest(self):
        return list(self.dataTest.find())

    def importDataTest(self):
        with open('sauvBase.csv', 'r') as csvfile:
            s = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in s:
                self.dataTest.insert({"data": list(map(int, row[1:])), "solution": row[0]})

    def sauvBaseToCsv(self, csvFile):
        data = self.getAllDataTrain()
        with open(csvFile, 'w') as csvfile:
            # writer = csv.writer(csvfile, delimiter=',')
            for document in data:
                # writer.writerow([document['value'],document['data'][0]])
                csvfile.write(str(document['solution']) + ",")
                for i in range(48):
                    if (i == 47):
                        csvfile.write(str(document['data'][i]) + "\n")
                    else:
                        csvfile.write(str(document['data'][i]) + ",")

    def savePoids(self, poids):
        result = self.poids.find_one({"method": "reseau"})
        self.poids.insert(
            {"method": "reseau", "poids": poids}) if not result else self.poids.find_and_modify(
            {"method": "reseau"}, {"method": "reseau", "poids": poids})
        return True

    def getPoids(self):
        res = self.poids.find_one()
        if res == None:
            return None
        return res["poids"]
        
db = Database()