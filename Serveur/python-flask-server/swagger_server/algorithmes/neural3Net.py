import math
import random
import copy
import csv
from neural3Neurone import neurone

class Net:
	
	def __init__(self, nbLayers, nbNeuroneByLayer, nbSortie, nbEntree, tauxApprentissage):
		self.sortie = [Neurone(nbNeuroneByLayer) for i in range (nbSortie)]
		self.layers = []
		self.tauxApprentissage = tauxApprentissage
		NeuronneEntry = [Neurone(nbEntree) for i in range (nbNeuroneByLayer)]
		self.layers.append(NeuronneEntry)
		for i in range (nbLayers-1) :
			layer = [Neurone(nbNeuroneByLayer) for i in range (nbNeuroneByLayer)]
			self.layers.append(layer)

	def calculate(self, entrees):
		currentEntry = entrees
		nextEntry = []
		for i in range (len(self.layers)):
			for j in range(len(self.layers[i])):
				self.layers[i][j].calculate(currentEntry)
				nextEntry.append(self.layers[i][j].getSortie())

			currentEntry = copy.deepcopy(nextEntry)
			nextEntry=[]
		sortie = []

		for i in range(len(self.sortie)):
			self.sortie[i].calculate(currentEntry)
			sortie.append(self.sortie[i].getSortie())

		return sortie

	def result(self,sortie):
		return sortie.index(max(sortie))

	def retroPropagation(self,sortie, attendu):
		erreur = []
		poids = []
		oldErreur=[]
		for i in range (len(sortie)):
			erreur.append(self.tauxErreur(sortie[i],attendu[i]))
		for i in rangel
		for i in reversed(range(len(self.layers))):
			for j in range(len(self.layers[i])):
				poids.append(self.layers[i][j].getPoids())
				self.layers[i][j].recalculPoids(erreur[j],self.tauxApprentissage)

			erreur=[]
			if i != 0:
				for j in range(len(self.layers[i-1])):
					erreur.append(produitMat(poids[i],erreur))
			poids=[]

	
	def tauxErreur(self, sortie, attendu):
		return (attendu-sortie)*sortie*(1-sortie)

	def produitMat(self,poids,erreur):
		return sum([x * y, for x,y in zip(poids,erreur)])
