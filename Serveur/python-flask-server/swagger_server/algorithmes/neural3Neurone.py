import math
import random
import copy
import csv

#classe neurone inutilisé et non fini
class Neurone:
	

	def __init__(self,nbInput):
		self.poids = [2*random.random()-1 for i in range(nbInput+1)]
		self.sortie = 0
		self.entrees = []

	def calculate(self,entrees):
		entreeSygmTab = [ x * y for x,y in zip(self.poids,entrees)]
		entreeSygm = sum(entreeSygmTab)
		self.sortie = self.sigmoid(entreeSygm)
		self.entrees=entrees

	def sigmoid(self, x):
		return 1 / (1 + exp(-x))

	def sigmoid_derivative(self, x):
		return x * (1 - x)

	def getSortie(self):
		return self.sortie

	def getPoids(self):
		return self.poids

	def recalculPoids(self,erreur,tauxApp):
		for i in range (len(self.poids)):
			self.poids[i]=self.poids[i]-self.entrees[i]*erreur*tauxApp

