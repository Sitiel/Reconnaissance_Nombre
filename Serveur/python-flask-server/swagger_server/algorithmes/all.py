from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye,trainBaye
from swagger_server.algorithmes.neural import NeuralNet
import swagger_server.algorithmes.utile
from swagger_server.database import db    


def testAll (image, retK, retB):
    n = NeuralNet(48, 10, 30, 2, 0.1)
    percents = n.percents(swagger_server.algorithmes.utile.centrageSolo(image,6, 8))
    retN = percents.index(max(percents))
    if max(percents) > 0.9:
        return retN
    else:
        if retK == percents.index(max(percents)):
            return retN
        else:
            if (retK == retB):
                return retN
            else:
                return retB