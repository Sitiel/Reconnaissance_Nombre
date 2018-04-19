import math

def moyenne(listImage):
	listRetour = []
	for i in range(len(listImage[0])):
		a = [v[i] for v in listImage]
		listRetour.append(sum(a)/len(a))
	return listRetour

def ecartType(listImage,moyenne) :
	imageRet = [0 for x in range (len(listImage[0]))]
	for i in range (len(listImage[0])) :
		for j in range (len(listImage)) :
			imageRet[i] += math.pow(listImage[j][i]-moyenne[i],2)
	for i in range (len(imageRet)) :
		imageRet[i]= math.sqrt(imageRet[i]/len(imageRet))
	return imageRet
		
def loiNormale(x,moyenne,ecartType) :
	var = math.pow(ecartType,2)
	num = math.exp(-(math.pow(x-moyenne,2))/(2*var))
	denom = math.pow((2*math.pi*var),0.5)
	return num/denom

def evaluateur(data, solutions, toFind):
	dataSorted = []
	dataEcarType = []
	dataMoyenne = []
	for j in range (2):
		dataSorted.append([v for i,v in enumerate(data) if solutions[i]==j])

	for k in range (0,len(dataSorted)) :
		dataMoyenne.append(moyenne(dataSorted[k]))
		dataEcarType.append(ecartType(dataSorted[k],dataMoyenne[k]))

	bestPercent = 0
	number = -1

	for k in range (0,len(dataMoyenne)) :
		currentPercent = -1
		for j in range (len(dataMoyenne[0])) :
			if dataEcarType[k][j] == 0 :
				currentPercent += loiNormale(toFind[j],dataMoyenne[k][j],1)
			else :
				currentPercent += loiNormale(toFind[j],dataMoyenne[k][j],dataEcarType[k][j])
		if currentPercent > bestPercent :
			bestPercent = currentPercent
			number = k
	return number



