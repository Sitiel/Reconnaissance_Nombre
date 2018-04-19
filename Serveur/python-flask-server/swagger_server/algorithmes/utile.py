# image 1 est l'image model, image 2 est l'image a centrer
def centrage(image1, image2, largeur, hauteur):
    i = 0
    dist = 0
    imageRet = image2
    imageCourante = image2
    bestDistance = largeur * hauteur
    for k in range(0, largeur):
        for j in range(0, hauteur):
            imageCourante = deplacementImage(imageCourante, 2, largeur, hauteur)
            dist = distance(imageCourante, image1)
            if bestDistance > dist:
                bestDistance = dist
                i = k * largeur + j
                imageRet = imageCourante
            if bestDistance == 0:
                return imageCourante
        imageCourante = deplacementImage(imageCourante, 1, largeur, hauteur)
        dist = distance(imageCourante, image1)
        if bestDistance > distance(imageCourante, image1):
            bestDistance = dist
            i = k * (largeur + 1)
            imageRet = imageCourante
        if bestDistance == 0:
            return imageCourante
    return imageRet


# direction correspond a un entier, 1 pour la droite, 2 pour le haut
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


def distValue(image1, image2):
    x = len(image1)
    retour = 0
    img = centrage(image1, image2, 6, 8)
    for i in range(0, x):
        if img[i] != image2[i]:
            retour += 1
    return retour