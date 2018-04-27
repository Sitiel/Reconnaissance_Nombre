# image 1 est l'image model, image 2 est l'image a centrer
import copy

#centrage(image a centrer, image modele, largeur image, hauteur image)
#permet de centrer l'image1 par rapport a l'image2
def centrage(image2, image1, largeur, hauteur):
    i = 0
    dist = 0
    imageRet = copy.deepcopy(image2)
    imageCourante = copy.deepcopy(image2)
    bestDistance = largeur * hauteur
    for k in range(0, largeur):
        for j in range(0, hauteur):
            imageCourante = deplacementImage(imageCourante, 2, largeur, hauteur)
            dist = distance(imageCourante, image1)
            if bestDistance > dist:
                bestDistance = dist
                i = k * largeur + j
                imageRet = copy.deepcopy(imageCourante)
            if bestDistance == 0:
                return imageCourante
        imageCourante = deplacementImage(imageCourante, 1, largeur, hauteur)
        dist = distance(imageCourante, image1)
        if bestDistance > distance(imageCourante, image1):
            bestDistance = dist
            i = k * (largeur + 1)
            imageRet = copy.deepcopy(imageCourante)
        if bestDistance == 0:
            return imageCourante
    return imageRet

#centrage(image, largeur image, hauteur image)
#permet de centrer l'image au centre du cadre
def centrageSolo(image, largeur, hauteur):
    hautGauche = [0 for i in range (largeur+hauteur)]
    basDroite = [largeur+hauteur for i in range (largeur+hauteur)]
    for k in range(len(image)):
        if image[k] == 1 :
            basDroite[k%largeur] = 0
            basDroite[(int)(k/largeur)+largeur] = 0
        else :
            if basDroite[k%largeur] == largeur+hauteur :
                hautGauche[k%largeur] += 1
            else :
                basDroite[k%largeur] += 1
            if basDroite[(int)(k/largeur)+largeur] == largeur+hauteur :
                hautGauche[(int)(k/largeur)+largeur] += 1
            else :
                basDroite[(int)(k/largeur)+largeur] += 1

    haut = min(hautGauche[0:largeur])
    gauche = min(hautGauche[largeur:-1])
    bas = min(basDroite[0:largeur])
    droite = min(basDroite[largeur:-1])

    bas = (int)(((bas - haut)/2 + hauteur) % hauteur)
    gauche = (int)(((gauche - droite)/2 + largeur) % largeur)

    for i in range (bas) :
        image = deplacementImage (image, 2, largeur,hauteur)
    for i in range (gauche) :
        image = deplacementImage (image, 1, largeur,hauteur)

    return image


# deplacement image permet de deplacer l'image vers la gauche ou le bas dans son cadre, tout ce qui passe d'un coté revient de l'autre
# direction correspond a un entier, 1 pour la gauche, 2 pour le bas
def deplacementImage(image, direction, largeur, hauteur):
    x = len(image)
    profondeur = 0
    imageRet = []
    if direction == 1:
        for i in range(0, x):
            if (i + 1) % largeur == 0:
                imageRet.append(image[largeur * profondeur])
                profondeur += 1
            else:
                imageRet.append(image[i + 1])
    elif direction == 2:
        for i in range(0, x):
            if (i < x):
                imageRet.append(image[0 - largeur + profondeur])
                profondeur += 1
            else:
                imageRet.image[i - largeur]
    return imageRet


# distance calcule le nombre de différence entre deux tableaux de meme taille
def distance(image1, image2):
    x = len(image1)
    retour = 0
    for i in range(0, x):
        if image1[i] != image2[i]:
            retour += 1
    return retour

#distValue fait la meme chose que distance mais en l'image1 par rapport a l'image2
def distValue(image1, image2):
    x = len(image1)
    retour = 0
    img = centrage(image1, image2, 6, 8)
    for i in range(0, x):
        if img[i] != image2[i]:
            retour += 1
    return retour

#permet d'afficher l'image avec des 0 et des 1
def printImage(image,largeur,hauteur):
    for i in range (hauteur):
        a = ""
        for j in range (largeur):
            a += str(image[j+i*largeur])
        print(a)
