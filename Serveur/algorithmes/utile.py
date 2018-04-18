def centrage(image1,image2):
	

def distance(image1,image2):
	x=len(image1)
	y=len(image1[0])
	retour = 0
	for i in range (0,x):
		for j in range(0,y):
			if image1[i][j] != image2[i][j]:
				retour+=1
	return retour;

