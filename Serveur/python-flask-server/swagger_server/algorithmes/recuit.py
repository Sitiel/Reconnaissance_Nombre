import random
import copy
import math
from lireOut import lireOutTxt

percentParam = []

def changeOneParam(param,borneMax,paramToChange):
	param[paramToChange]=round(random.random()*borneMax-20,2)
	return param

def chooseParamToChange():
	global percentParam
	i = sum(percentParam)
	j=int(random.random()*i)
	for k in range (len(percentParam)):
		j-= percentParam[k]
		if j<=0 :
			return k

def reloadParamToChange():
	global percentParam
	a0 = [1]*48
	a = lireOutTxt("out.txt")
	b = lireOutTxt("out2.txt")
	percentParam = [x + y + z for x,y,z in zip(a,b,a0)]

def calculRecuit(delta,temp):
	return math.exp(-delta/temp)

def calculAcceptation(delta, temp):
	recuit = calculRecuit(delta,temp)
	i = random.random()
	return i<=recuit

def calculTemp(temp, variationTemp):
	return temp*variationTemp

def firstTemp(delta, pourcentage):
	return -delta/math.log(pourcentage)

def firstVariationTemp(tempInit,nbIterationMax):
	return math.fabs(math.pow(tempInit,1/nbIterationMax)-2)

def recuitCalcul(variablesCount, evaluate):
	#hyperParameter

	print("calcul du recuit")
	nbIterationMax = 500000
	iteration = 0
	maxBorne = 100
	notProgressing = 0
	borneNotProgressing = 1000
	delta=48

	temp = firstTemp(delta,0.36)/10
	variationTemp=firstVariationTemp(temp,nbIterationMax)

	accepted = 0
	currentValue = 0
	current = [round(random.randint(0,maxBorne/4)-5,2) for i in range(variablesCount)]
	#current = [1 for i in range(variablesCount)]
	currentBest=copy.deepcopy(current)
	currentBestValue = evaluate(current)

	reloadParamToChange()

	while(iteration<nbIterationMax):
		if iteration%1000 == 0 : 
			reloadParamToChange()
			print("iteration:" , iteration)
			print("currentValue: ", currentValue," currentBestValue: ",currentBestValue," hyper Parametre : ",currentBest)
		#i = random.randint(0,len(current)-1)
		i=chooseParamToChange()
		changeOneParam(current,maxBorne,i)
		currentValue = evaluate(current)
		if currentValue > currentBestValue :
			print("new best, currentValue: ",currentValue, "with", currentBest)
			#if(currentValue-currentBestValue >2) :
			#	with open('/out2.txt' , 'a') as f:
			#		print("index : ", i, file=f)
			currentBestValue = currentValue
			currentBest[i] = current[i]
			notProgressing = 0
		else:
			if not calculAcceptation(currentBestValue-currentValue,temp):
				if accepted == 1 :
					accepted = 0
					current = copy.deepcopy(currentBest)
				else :
					current[i]=currentBest[i]
			else :
				accepted = 1
		notProgressing += 1
		iteration += 1
		temp = calculTemp(temp,variationTemp)
		#print(temp,"  ",iteration)
	#print(variationTemp)
	print("Current best :", currentBest, "with", currentBestValue)
	return currentBest

def evalu(param):
	return math.fabs(sum(param)-1500)