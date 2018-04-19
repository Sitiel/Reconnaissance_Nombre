
class NeuralNet:

    def __init__(self, inData, outData, neurones, layersNB, learningRate):
        self.inData = inData
        self.outData = outData
        self.neurones = neurones
        self.learningRate = learningRate
        self.weights = []
        for i  in range(layersNB):
            layerSize = outData if i == layersNB-1 else neurones
            for j in range(layerSize):
                self.weights.append([1 for k in range(inData if i == 0 else neurones)])



    def train(self, trainData):
        print([len(l) for l in self.weights])


