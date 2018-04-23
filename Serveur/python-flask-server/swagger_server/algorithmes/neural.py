import math
import random

class NeuralNet:

    def __init__(self, inData, outData, neurones, layersNB, learningRate):
        self.inData = inData
        self.outData = outData
        self.neurones = neurones
        self.layersNB = layersNB
        self.learningRate = learningRate
        self.weights = []
        for i in range(layersNB):
            layer = []
            for j in range(neurones):
                layer.append([0 for x in range((inData+1) if i == 0 else (neurones+1))])

            self.weights.append(layer)

        # Out layer
        layer = []
        for j in range(outData):
            layer.append([0 for x in range(neurones+1)])
        self.weights.append(layer)

    def activation(self, value):
        return 1 / (1 + math.exp(-value))

    def train(self, trainData, solutions):
        # print([len(l) * len(l[0]) for l in self.weights], sep="-")
        accuracy = 0
        neurones = []

        nbIteration = len(trainData)

        for index in range(nbIteration):
            t = trainData[index]
            inData = t + [1] # bias
            for layer in range(len(self.weights)):
                neurones.append(inData)
                outData = []
                for neurone in range(len(self.weights[layer])):
                    outData.append(self.activation(sum([a * b for a, b in zip(inData, self.weights[layer][neurone])])))
                inData = outData
                if layer != len(self.weights)-1:
                    inData += [1]

            # BACK PROP
            expected = [0 for _ in range(self.outData)]
            expected[solutions[index]] = 1
            newLayers = {}

            print("Solution : ", solutions[index], inData.index(max(inData)))
            if solutions[index] == inData.index(max(inData)):
                accuracy += 1
                # print("response : ", inData.index(max(inData)), inData)

            # print("Neurones : ", neurones)

            inBack = [-(expected[c] - inData[c]) * inData[c] * (1 - inData[c]) for c in range(len(inData))]
            # print("Expected : ", expected)
            # print("Get : ", inData)
            # print("InBack : ", inBack, end="\n\n")



            for layer in reversed(range(1, len(self.weights))):
                newLayer = []
                # print("Inback size : ", len(inBack), " neurones : ", len(self.weights[layer][0]))

                for neurone in range(len(self.weights[layer])):
                    newNeurones = []
                    for w in range(len(self.weights[layer][neurone])):
                        newNeurones.append(self.weights[layer][neurone][w] - (neurones[layer][w]*inBack[neurone] * self.learningRate))
                    newLayer.append(newNeurones)
                newLayers[layer] = newLayer

                newInBack = []
                for i in range(len(self.weights[layer][0])):
                    r = 0
                    for j in range(len(self.weights[layer])):
                        r += self.weights[layer][j][i] * inBack[j]
                    newInBack.append(r * neurones[layer][i] * (1 - neurones[layer][i]))


                # print("New layer : ", newLayer)
                # print("new in : ", newInBack)
                inBack = newInBack

            for l in range(1, len(self.weights)):
                self.weights[l] = newLayers[l]
        print("Accuracy : ", accuracy/nbIteration)
        print(self.weights)

    def guess(self, data):
        inData = data + [1]  # bias
        for layer in range(len(self.weights)):
            outData = []
            for neurone in range(len(self.weights[layer])):
                outData.append(self.activation(sum([a * b for a, b in zip(inData, self.weights[layer][neurone])])))
            inData = outData
            if layer != len(self.weights) - 1:
                inData += [1]

        return inData.index(max(inData))