import numpy as np

max_colonne  =  6
max_ligne = 5

indix_colonne = 1
joueur = 2

MATRICE_JEU = np.array([
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0],
                [0,1,0,0,0,0,0],
                [0,1,0,0,0,0,0],
            ])


def nouveau_jeu(): #fonction qui renvoie nouveau plateau de jeu
    return MATRICE_JEU

def est_plein_colonne(tab):
    if len(tab)>= max_colonne :
        print(len(tab))
        return True
    else :
        return False
    
    
def colonne_libre(MATRICE_JEU, indix_colonne):  #verifie si jetons peut etre mis dans colonne 
    colonne = MATRICE_JEU[:, indix_colonne]
    i = 0
    for elem in colonne :
        if (elem != 0) :
            i = i + 1
    if (i == max_colonne) :
        print("Colonne pleine!!!\n")
        return False #colonne pleine
    else:
        return True #colonne libre

def place_jeton(MATRICE_JEU, indix_colonne, joueur):
    if ( colonne_libre(MATRICE_JEU, indix_colonne) == True ):
        colonne = MATRICE_JEU[:, indix_colonne]
        i = 0
        for i in range(5, -1, -1):
            if colonne[i] == 0:
                ( MATRICE_JEU[:, indix_colonne] )[i] = joueur
                print("Jeton joueur",joueur,"placé !\n")
                return MATRICE_JEU
            
    else:
        print("Impossible d'inserrer jeton.\n")
        return MATRICE_JEU
