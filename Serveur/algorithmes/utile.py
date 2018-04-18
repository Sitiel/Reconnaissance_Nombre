def centrage(image1,image2):
	

def distance(image1,image2):
	x=len(image1)
	retour = 0
	for i in range (0,x):
		if image1[i]!= image2[i]:
			retour+=1
	return retour;

