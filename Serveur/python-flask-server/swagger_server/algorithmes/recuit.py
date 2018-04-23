import random
import copy
import math

def changeOneParam(param,borneMax,paramToChange):
	param[paramToChange]=random.random()*borneMax
	return param


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
	nbIterationMax = 500000
	iteration = 0
	maxBorne = 1000
	notProgressing = 0
	borneNotProgressing = 1000
	delta=100

	temp = firstTemp(delta,0.36)/10
	variationTemp=firstVariationTemp(temp,nbIterationMax)

	accepted = 0
	currentValue = 0
	current = [random.randint(0,maxBorne) for i in range(variablesCount)]
	currentBest=copy.deepcopy(current)
	currentBestValue = evaluate(current)

	while(iteration<nbIterationMax):
		i = random.randint(0,len(current)-1)
		changeOneParam(current,maxBorne,i)
		currentValue = evaluate(current)
		if currentValue < currentBestValue :
			print("new best, currentValue: ",currentValue)
			currentBestValue = currentValue
			currentBest[i] = current[i]
			notProgressing = 0
		else:
			if not calculAcceptation(currentValue-currentBestValue,temp):
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
	return currentBest

def evalu(param):
	return math.fabs(sum(param)-1500)