import math
import random
from swagger_server.database import db


class NeuralNet:

    # NN Construct
    def __init__(self, inData, outData, neurones, layersNB, learningRate):
        self.inData = inData
        self.outData = outData
        self.neurones = neurones
        self.layersNB = layersNB
        self.learningRate = learningRate
        self.weights = db.getPoids()
        # if not in db, reset the weights
        if self.weights is None or len(self.weights) != layersNB+1:
            self.reset()

    def reset(self):
        self.weights = []
        # Hidden layers initialisation
        for i in range(self.layersNB):
            layer = []
            for j in range(self.neurones):
                layer.append([random.uniform(-0.01, 0.01) for x in range((self.inData + 1) if i == 0 else (self.neurones + 1))])

            self.weights.append(layer)

        # Out layer
        layer = []
        for j in range(self.outData):
            layer.append([random.uniform(-1, 1) for x in range(self.neurones + 1)])
        self.weights.append(layer)

        # Save to the BDD
        db.savePoids(self.weights)

    def activation(self, value):
        # Sigmoid fix for math range
        if value < -709:
            return 1
        return 1 / (1 + math.exp(-value))

    def train(self, trainData, solutions):
        accuracy = 0

        nbIteration = len(trainData)

        for index in range(nbIteration):

            # ---------------------------- PROPAGATION -------------------------------

            outputLayers = []
            t = trainData[index]
            inData = t + [1]  # bias
            for layer in range(len(self.weights)):
                outputLayers.append(inData)
                outData = []
                for neurone in range(len(self.weights[layer])):
                    outData.append(self.activation(sum([a * b for a, b in zip(inData, self.weights[layer][neurone])])))
                inData = outData
                if layer != len(self.weights)-1:
                    inData += [1]

            # ---------------------------- BACK PROP -------------------------------
            expected = [0 for _ in range(self.outData)]
            expected[solutions[index]] = 1
            newLayers = {}

            if solutions[index] == inData.index(max(inData)):
                accuracy += 1

            # Input Data for the back propagation
            inBack = [(expected[c] - inData[c]) * inData[c] * (1 - inData[c]) for c in range(len(inData))]

            # Propagate the graph reversed
            for layer in reversed(range(len(self.weights))):
                pLayer = layer
                newLayer = []

                # Calculate the correction for the weights
                for neurone in range(len(self.weights[layer])):
                    newWeights = []
                    for w in range(len(self.weights[layer][neurone])):
                        newWeights.append(self.weights[layer][neurone][w] + (outputLayers[pLayer][w] * inBack[neurone] * self.learningRate))

                    newLayer.append(newWeights)
                newLayers[layer] = newLayer

                # Calculate the new input for the next layer
                newInBack = []
                for i in range(len(self.weights[layer][0])):
                    r = 0
                    for j in range(len(self.weights[layer])):
                        r += self.weights[layer][j][i] * inBack[j]
                    newInBack.append(r * outputLayers[pLayer][i] * (1 - outputLayers[pLayer][i]))

                inBack = newInBack

            # Apply weights
            for l in range(len(self.weights)):
                self.weights[l] = newLayers[l]

        # End of the training
        print("Accuracy : ", float(accuracy)/nbIteration)
        db.savePoids(self.weights)

    def guess(self, data):
        # Propagate the input to the output to calculate the result of the neural network
        inData = data + [1]  # bias
        for layer in range(len(self.weights)):
            outData = []
            for neurone in range(len(self.weights[layer])):
                outData.append(self.activation(sum([a * b for a, b in zip(inData, self.weights[layer][neurone])])))
            inData = outData
            if layer != len(self.weights) - 1:
                inData += [1]

        return inData.index(max(inData))
    
    def percents(self, data):
        # Propagate the input to the output to calculate the result of the neural network
        inData = data + [1]  # bias
        for layer in range(len(self.weights)):
            outData = []
            for neurone in range(len(self.weights[layer])):
                outData.append(self.activation(sum([a * b for a, b in zip(inData, self.weights[layer][neurone])])))
            inData = outData
            if layer != len(self.weights) - 1:
                inData += [1]

        # Return the raw output of the neural network
        return inData
