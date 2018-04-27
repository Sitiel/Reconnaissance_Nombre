import random
import copy
import math
from lireOut import lireOutTxt

percentParam = []

# function to change one param
def changeOneParam(param,borneMax,paramToChange):
	param[paramToChange]=round(random.random()*borneMax-3,2)
	return param

# function use to get the param to change, determined by a random and the parameter utility
def chooseParamToChange():
	global percentParam
	i = sum(percentParam)
	j=int(random.random()*i)
	for k in range (len(percentParam)):
		j-= percentParam[k]
		if j<=0 :
			return k

#use to load the parameter utility determined by 2 another process who save the parameter who make a big change
def reloadParamToChange():
	global percentParam
	a0 = [1]*14
	a = lireOutTxt("out.txt")
	b = lireOutTxt("out2.txt")
	percentParam = [x + y + z for x,y,z in zip(a,b,a0)]

#use to calcul the percent with the temperature
def calculRecuit(delta,temp):
	return math.exp(-delta/temp)

#use to calcul the acceptation with the delta and the temperature
def calculAcceptation(delta, temp):
	recuit = calculRecuit(delta,temp)
	i = random.random()
	return i<=recuit

#use to calculate the temperature on each loop
def calculTemp(temp, variationTemp):
	return temp*variationTemp

#use to calculate the first temp
def firstTemp(delta, pourcentage):
	return -delta/math.log(pourcentage)

#use to calcul the temperature variation to reach 0 of temp on the iteration max
def firstVariationTemp(tempInit,nbIterationMax):
	return math.fabs(math.pow(tempInit,1/nbIterationMax)-2)

#use to launch calcul
def recuitCalcul(variablesCount, evaluate):
	#hyperParameter
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

#use to evalu, not used
def evalu(param):
	return math.fabs(sum(param)-1500)