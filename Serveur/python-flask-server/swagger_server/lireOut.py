def lireOutTxt(file):
	number=[0 for i in range(48)]
	i = 0
	with open(file, "r") as f:
		for line in f.readlines():
			i = int(line[9:])
			number[i]+=1
	return number