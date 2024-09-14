import pygame,sys
import numpy as np
from random import *
pygame.init()


#Definition des couleurs 
Blanche  =   (255,255,255)
Noire  =   (100,100,100)
Violet = (100,0,100)
Red = (0,50,70)
Jaune = (100,50,0)
Rouge=  (255,0,0)
Jaune_2 = (255,255,0)
Bleu = (0,0,255) 
#Declaration des photos 
fond_ecran = pygame.image.load("Puissance4.jpg")
fond_ecran = pygame.transform.scale(fond_ecran, (778,650))
fond_grille = pygame.image.load("grille.png")
fond_grille = pygame.transform.scale(fond_grille, (500,450))
Menu_photo = pygame.image.load("Foto_menu.jpg")
Menu_photo = pygame.transform.scale(Menu_photo, (778,650))
player_1 = pygame.image.load("P1.png")
player_1 = pygame.transform.scale(player_1, (200,30))
player_2 = pygame.image.load("Pé.png")
player_2 = pygame.transform.scale(player_2, (210,30))
winner_1 = pygame.image.load("winner-1.png")
winner_1 = pygame.transform.scale(winner_1, (778,650))
winner_2 = pygame.image.load("winner-2.png")
winner_2 = pygame.transform.scale(winner_2, (778,650))
#Declaration des musiques 
sound_puissance4 = pygame.mixer.Sound("pixel-fight-8-bit-arcade-music-background-music-for-video-208775.mp3")
sound_menu= pygame.mixer.Sound("game-setting-fantasy-142092.mp3")
sound_grille= pygame.mixer.Sound("8-bit-arcade-mode-158814.mp3")
sound_winner= pygame.mixer.Sound("mixkit-auditorium-moderate-applause-and-cheering-502.wav")
sound_ready_fight =pygame.mixer.Sound("READY FIGHT  SOUND EFFECT.mp3")
sound_jeton =pygame.mixer.Sound("mixkit-arcade-game-jump-coin-216.wav")

#Taille de screen
largeur_screen = 778  
haut_screen = 650
size = (largeur_screen ,haut_screen)

#taille de la grille
max_colonne  =  6
max_ligne = 5
#variable permettant de savoir quand choisir une autre colonne
p = 0 
# variables permetant de recuperer la ligne et la colonne à chaque tour 
ligne_matrice = [0]
ligne_matrice_pc = [0]
colonne_matrice = [0]
#Constante pour la taille de chaque hitbox en largueur et en hauteur de la grille (calcul plus facile par rapport à usage)
taille_hitbox_x_grille = 67  
taille_hitbox_y_grille =72


#Creer écran
screen = pygame.display.set_mode(size) 
clock= pygame.time.Clock()  #Horloge
MATRICE_JEU =np.array([ [0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0],
                        [0,0,-1,1,0,0,0],
                        [0,-1,1,1,0,0,0],
                        [0,-1,-1,1,1,0,0],
                        [0,1,-1,-1,-1,1,0],
])
#Le tour à chaque passage
tour = [-1]

# Liste pour contenir les scores des joueurs
score_joueurs = [0, 0]  

#Fonction qui permet d'afficher du texte sur l'ecran graphique en pygame au milieu de la fenêtre 
def ecrire_text_ecran (text,taille_lettre,type_de_lettre,distance_x,distance_y,coulor) :
        font = pygame.font.SysFont(type_de_lettre,taille_lettre)
        text = font.render(text,True,coulor)
        center_x =(largeur_screen // 2) - (text.get_width() // 2) + distance_x
        center_y =(haut_screen // 2) - (text.get_height() // 2) + distance_y

        screen.blit(text, [center_x, center_y])

#fonction qui met à zero tous les positions de la grille 
def recommencer_jeu ():
    score_joueurs[0] = 0
    score_joueurs[1] = 0
    for i in range (0,6):
        for j in range (0,7):
            MATRICE_JEU[i][j]= 0
            
                
#Impresion de la matrice == grille
def matrice_print ():
    for i in range (0,6):
        for j in range (0,7):
            print(MATRICE_JEU[i][j], end=' ')

#met à jour le score en fonction de si un joueur a gagné en ligne           
def verif_largeur():           
    for i in range(0, 6):
        for j in range(0, 4):
            if (MATRICE_JEU[i][j] == -1) and (MATRICE_JEU[i][j+1] == -1) and (MATRICE_JEU[i][j+2] == -1) and (MATRICE_JEU[i][j+3] == -1):
                score_joueurs[0] += 1

            elif (MATRICE_JEU[i][j] == 1) and (MATRICE_JEU[i][j+1] == 1) and (MATRICE_JEU[i][j+2] == 1) and (MATRICE_JEU[i][j+3] == 1):
                score_joueurs[1] += 1

#verifie si jeton peut etre mis dans colonne 
def colonne_libre(): 
    colonne = MATRICE_JEU[:, colonne_matrice[0]]
    i = 0
    for elem in colonne :
        if (elem != 0) :
            i = i + 1
    if (i == max_colonne) :
        
        ligne_matrice[0] = -1
    else:
        ligne_matrice[0] = i
#verifie si jeton peut etre mis dans colonne 
def colonne_libre_pc(k): 
    colonne = MATRICE_JEU[:, k]
    i = 0
    for elem in colonne :
        if (elem != 0) :
            i = i + 1
    if (i == max_colonne) :
        print("Colonne pleine!!!\n")
        ligne_matrice_pc[0] = -1
    else:
        ligne_matrice_pc[0] = i

#met à jour le score en fonction de si un joueur a gagné en colonne
def verif_hauteur():           
    for i in range(0, 3):
        for j in range(0, 7):
            if (MATRICE_JEU[i][j] == -1) and (MATRICE_JEU[i+1][j] == -1) and (MATRICE_JEU[i+2][j] == -1) and (MATRICE_JEU[i+3][j] == -1):
                score_joueurs[0] += 1  
            elif (MATRICE_JEU[i][j] == 1) and (MATRICE_JEU[i+1][j] == 1) and (MATRICE_JEU[i+2][j] == 1) and (MATRICE_JEU[i+3][j] == 1):
                score_joueurs[1] += 1               
# Vérification des diagonales 
def verif_diagonale():
    ligne = len(MATRICE_JEU)
    colonnes = len(MATRICE_JEU[0])

    # Vérification des diagonales descendantes (de gauche à droite)
    for i in range(ligne - 3):
        for j in range(colonnes - 3):
            if (MATRICE_JEU[i][j] == -1 and 
                MATRICE_JEU[i+1][j+1] == -1 and 
                MATRICE_JEU[i+2][j+2] == -1 and 
                MATRICE_JEU[i+3][j+3] == -1):
                score_joueurs[0] += 1
            elif (MATRICE_JEU[i][j] == 1 and 
                  MATRICE_JEU[i+1][j+1] == 1 and 
                  MATRICE_JEU[i+2][j+2] == 1 and 
                  MATRICE_JEU[i+3][j+3] == 1):
                score_joueurs[1] += 1

    # Vérification des diagonales ascendantes (de gauche à droite)
    for i in range(3, ligne):
        for j in range(colonnes - 3):
            if (MATRICE_JEU[i][j] == -1 and 
                MATRICE_JEU[i-1][j+1] == -1 and 
                MATRICE_JEU[i-2][j+2] == -1 and 
                MATRICE_JEU[i-3][j+3] == -1):
                score_joueurs[0] += 1
            elif (MATRICE_JEU[i][j] == 1 and 
                  MATRICE_JEU[i-1][j+1] == 1 and 
                  MATRICE_JEU[i-2][j+2] == 1 and 
                  MATRICE_JEU[i-3][j+3] == 1):
                score_joueurs[1] += 1


 # Vérification des tours de chaque joueur, player 1 et player 2
def tour_joueur():
    if (tour[0] == -1):
        tour[0] = 1
    else:
        tour[0] = -1

 # Vérification des tours de chaque joueur, player 1 et player PC
def tour_joueur_pc():
    tour[0] = 1
    ecriture_matrice()

    tour [0] = -1
    i = randint(0,6)
    colonne_libre_pc(i)
    while ligne_matrice_pc[0] == -1:            #vérifie continuellement que la colonne n'est pas pleine, sinon reprend une autre valeur random
        i = randint(0,6)
        colonne_libre_pc(i)

    MATRICE_JEU[5 - ligne_matrice_pc[0],i] = tour[0]


def ecriture_matrice():
    MATRICE_JEU[5 - ligne_matrice[0],colonne_matrice[0]] = tour[0]
    
#Dessin de chaque hitbox pour une meilleure visualisation
def dessin_rect():    
    #ligne 6
    for i in range (0,6):
        for j in range (0,7):
           pygame.draw.rect(screen, Noire, (171+taille_hitbox_x_grille*j-j,464-taille_hitbox_y_grille*i+i,taille_hitbox_x_grille,taille_hitbox_y_grille), 1)

#Dessin de Jeton en fonction du changement de la matrice de jeu et aussi choisir couleur pertinent       
def dessin_circle(i,j,color):
    if(color == 1):
        circle_color = Rouge
    else:
        circle_color = Jaune_2
    if(i==0 ):
        if(j==0):
            pygame.draw.circle(screen, circle_color, (533-67*5+5,146), 30)
        if(j==1):
            pygame.draw.circle(screen, circle_color, (533-67*4+4,146), 30)
        if(j==2):   
            pygame.draw.circle(screen, circle_color, (533-67*3+2,146), 30) 
        if(j==3):
            pygame.draw.circle(screen, circle_color, (533-67*2+1,146), 30)
        if(j==4):
            pygame.draw.circle(screen, circle_color, (533-67,146), 30) 
        if(j==5):
            pygame.draw.circle(screen, circle_color, (533,146), 30)  
        if(j==6):
            pygame.draw.circle(screen, circle_color, (533+67,146), 30)
    if(i==1):
        if(j==0):
            pygame.draw.circle(screen, circle_color, (533-67*5+5,146+71), 31)
        if(j==1):
            pygame.draw.circle(screen, circle_color, (533-67*4+4,146+71), 31)
        if(j==2):
            pygame.draw.circle(screen, circle_color, (533-67*3+2,146+71), 31) 
        if(j==3):
            pygame.draw.circle(screen, circle_color, (533-67*2+1,146+71), 31)
        if(j==4):
            pygame.draw.circle(screen, circle_color, (533-67,146+71), 31) 
        if(j==5):
            pygame.draw.circle(screen, circle_color, (533,146+71), 31)  
        if(j==6):
            pygame.draw.circle(screen, circle_color, (533+67,146+71), 31)
    if(i==2):
        if(j==0):
            pygame.draw.circle(screen, circle_color, (533-67*5+5,146+71*2-1), 31)
        if(j==1):
            pygame.draw.circle(screen, circle_color, (533-67*4+4,146+71*2-1), 31)
        if(j==2):
            pygame.draw.circle(screen, circle_color, (533-67*3+2,146+71*2-1), 31) 
        if(j==3):
            pygame.draw.circle(screen, circle_color, (533-67*2+1,146+71*2-1), 31)
        if(j==4):
            pygame.draw.circle(screen, circle_color, (533-67,146+71*2-1), 31) 
        if(j==5):
            pygame.draw.circle(screen, circle_color, (533,146+71*2-1), 31)  
        if(j==6):
            pygame.draw.circle(screen, circle_color, (533+67,146+71*2-1), 31) 
    if(i==3):
        if(j==0):
            pygame.draw.circle(screen, circle_color, (533-67*5+5,146+71*3-1), 31)
        if(j==1):
            pygame.draw.circle(screen, circle_color, (533-67*4+4,146+71*3-1), 31)
        if(j==2):
            pygame.draw.circle(screen, circle_color, (533-67*3+2,146+71*3-1), 31) 
        if(j==3):
            pygame.draw.circle(screen, circle_color, (533-67*2+1,146+71*3-1), 31)
        if(j==4):
            pygame.draw.circle(screen, circle_color, (533-67,146+71*3-2), 31) 
        if(j==5):
            pygame.draw.circle(screen, circle_color, (533,146+71*3), 31)  
        if(j==6):
            pygame.draw.circle(screen, circle_color, (533+67,146+71*3-2), 31)
    if(i==4):
        if(j==0):
            pygame.draw.circle(screen, circle_color, (533-67*5+5,146+71*4-1), 31)
        if(j==1):
            pygame.draw.circle(screen, circle_color, (533-67*4+4,146+71*4-2), 31)
        if(j==2):
            pygame.draw.circle(screen, circle_color, (533-67*3+2,146+71*4-2), 31) 
        if(j==3):
            pygame.draw.circle(screen, circle_color, (533-67*2+1,146+71*4-1), 31)
        if(j==4):
            pygame.draw.circle(screen, circle_color, (533-67,146+71*4-2), 31) 
        if(j==5):
            pygame.draw.circle(screen, circle_color, (533,146+71*4-1), 31)  
        if(j==6):
            pygame.draw.circle(screen, circle_color, (533+67,146+71*4-2), 31)
    if(i==5):
        if(j==0):
            pygame.draw.circle(screen, circle_color, (533-67*5+5,146+71*5-3), 31)
        if(j==1):
            pygame.draw.circle(screen, circle_color, (533-67*4+4,146+71*5-3), 31)
        if(j==2):
            pygame.draw.circle(screen, circle_color, (533-67*3+2,146+71*5-3), 31) 
        if(j==3):
            pygame.draw.circle(screen, circle_color, (533-67*2+1,146+71*5-3), 31)
        if(j==4):
            pygame.draw.circle(screen, circle_color, (533-67,146+71*5-3), 31) 
        if(j==5):
            pygame.draw.circle(screen, circle_color, (533,146+71*5-1), 31)  
        if(j==6):
            pygame.draw.circle(screen, circle_color, (533+67,146+71*5-3), 31)       

#Fonction qui mis en place la postion de hitbox de menu 3 en total (Quit, play 1 vs 1, play 1 vs PC et permet le changement de l'écran)   
def logique_menu():
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        mouse_axe_x = MENU_MOUSE_POS[0]
        mouse_axe_y = MENU_MOUSE_POS[1]

        if(mouse_axe_x> 435 and mouse_axe_x < 631 and mouse_axe_y > 450 and mouse_axe_y < 525 ):  
                    sys.exit()
        elif(mouse_axe_x> 486 and mouse_axe_x < 607 and mouse_axe_y > 120 and mouse_axe_y < 205 ):
                    sound_ready_fight.play()
                    grille_1_vs_1()
        elif(mouse_axe_x> 146 and mouse_axe_x < 267 and mouse_axe_y > 303 and mouse_axe_y < 423 ):
                    sound_ready_fight.play()
                    grille_PC()
#Fonction qui appele de manière continue la grille en cas d'une modification et appelle la fonction dessin_circle() pour mettre un jeton   
def logique_grille():
    
    for i in range (0,6):
        for j in range (0,7):
             if(MATRICE_JEU[i][j] == 1):
                color =1 #Rouge 
                dessin_circle(i,j,color)
             elif(MATRICE_JEU[i][j] == -1):
                color =-1 #Jaune
                dessin_circle(i,j,color)

#Fonction qui permet de récuperer la position de la souris sur la grille ou dehors de la grille en changent la colonne dans laquel la souris est positionnée, actualisation constante 
def colonne_matrice_logique():
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    mouse_axe_x = MENU_MOUSE_POS[0]
    mouse_axe_y = MENU_MOUSE_POS[1]
    if(mouse_axe_x > 171 and mouse_axe_x <taille_hitbox_x_grille+171 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5 ):
       colonne_matrice[0]= 0 
        
    elif(mouse_axe_x > taille_hitbox_x_grille+171 and mouse_axe_x <taille_hitbox_x_grille*2+171-2 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5 ):
       colonne_matrice[0]= 1
        
    elif(mouse_axe_x > taille_hitbox_x_grille*2+171-2 and mouse_axe_x <taille_hitbox_x_grille*3+171-3 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5 ):
       colonne_matrice[0]= 2
        
    elif(mouse_axe_x > taille_hitbox_x_grille*3+171-3 and mouse_axe_x <taille_hitbox_x_grille*4+171-4 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5):
       colonne_matrice[0]= 3
        
    elif(mouse_axe_x > taille_hitbox_x_grille*4+171-4 and mouse_axe_x <taille_hitbox_x_grille*5+171-5 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5):
       colonne_matrice[0]= 4
        
    elif(mouse_axe_x > taille_hitbox_x_grille*5+171-5 and mouse_axe_x <taille_hitbox_x_grille*6+171-6 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5):
       colonne_matrice[0]= 5
        
    elif(mouse_axe_x > taille_hitbox_x_grille*6+171-6 and mouse_axe_x<taille_hitbox_x_grille*7+171-7 and mouse_axe_y < 464+taille_hitbox_x_grille and mouse_axe_y > 464-taille_hitbox_y_grille*5+5 ):
       colonne_matrice[0]= 6
        
    else :
       colonne_matrice[0]= -1 #Dehors de la grille         
#Dessin du carré rouge ou jaune en fonction de tour de jouer 
def dessin_rect_tour_jour():
    if(tour[0] == -1):
        pygame.draw.rect(screen, Rouge, (10,30,270,70), 3)
    elif(tour[0] == 1):
        pygame.draw.rect(screen, Jaune_2, (500,30,270,70), 3)
#Fonction qui permet d'aller' dans un écran de victoire si le score a changé 
def logique_winner():
    if(score_joueurs[0] == 1):
        ecran_winner_2()
    if(score_joueurs[1] == 1):
        ecran_winner_1()
        
#Fonction qui permet de mettre la chanson au debut 
def sound_puissance_4():
    sound_puissance4.play(1)

#Fonction qui permet d'actualiser l'ecran de debut
def actualization_ecran_Puissance_4():
   
    
    pygame.display.flip()
    screen.blit(fond_ecran,[0,0])
    clock.tick(60)
#Fonction qui permet d'actualiser l'ecran de debut
def actualization_event_Puissance_4():
     for event in pygame.event.get(): 
            #Quitter le jeu jamais oublier
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
               menu()
def actualization_ecran_menu():
    pygame.display.flip()
    screen.fill(Blanche)
    screen.blit(Menu_photo,[0,0])
    clock.tick(60)  
def actualization_event_menu():
      for event in pygame.event.get(): 
            #Quitter le jeu
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                logique_menu()
def sound_sur_menu() :
    sound_winner.stop()
    sound_puissance4.stop()
    sound_menu.play(1)


def fonction_affichag_text_menu():
    ecrire_text_ecran("1 vs 1",50,"agencyfbgras",160,-160,Violet) 
    ecrire_text_ecran("vs",50,"agencyfbgras",-180,0,Red) 
    ecrire_text_ecran("PC",50,"agencyfbgras",-180,60,Red)  
    ecrire_text_ecran("Quit",50,"agencyfbgras",138,160,Jaune) 


def sound_grille_PC():
    sound_menu.stop()
    sound_grille.play(1)


def actualization_ecran_grille_PC():
    pygame.display.flip()
    screen.fill(Blanche)
    screen.blit(fond_grille,[152,100])
    screen.blit(player_1,[40,50])
    screen.blit(player_2,[530,50])


def actualization_event_grille_PC():
      for event in pygame.event.get(): 
            #Quitter le jeu
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                sound_jeton.play()
                if ((ligne_matrice[0] != -1) and (colonne_matrice[0] != -1)):
                    tour_joueur_pc()


def dessin_circle_avec_mouse():
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    mouse_axe_x = MENU_MOUSE_POS[0]
    mouse_axe_y = MENU_MOUSE_POS[1]
    if(tour[0]==1):
        pygame.draw.circle(screen, Jaune_2, (mouse_axe_x,mouse_axe_y), 31)
    elif(tour[0]==-1):
        pygame.draw.circle(screen, Rouge, (mouse_axe_x,mouse_axe_y), 31)
def sound_grille_1_vs_1():   
    sound_menu.stop()
    sound_grille.play(1)


def actualization_ecran_grille_1_vs_1():
    pygame.display.flip()
    screen.fill(Blanche)
    screen.blit(fond_grille,[152,100])
    screen.blit(player_1,[40,50])
    screen.blit(player_2,[530,50])
    clock.tick(60)


def actualization_event_grille_1_vs_1():
      for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                sound_jeton.play()
                if ((ligne_matrice[0] != -1) and (colonne_matrice[0] != -1)):
                    tour_joueur()
                    ecriture_matrice()

def sound_ecran_winner_2():
    sound_grille.stop()
    sound_winner.play(1)

def actualization_ecran_ecran_winner_2():
    pygame.display.flip()
    screen.fill(Blanche)
    screen.blit(winner_2,[0,0])

def actualization_event_ecran_winner_2():
    for event in pygame.event.get(): 
            #Quitter le jeu jamais oublier
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                menu()
def actualization_ecran_winner_1():
    pygame.display.flip()
    screen.fill(Blanche)
    screen.blit(winner_1,[0,0])
def actualization_event_winner_1():
    for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                menu()
def sound_ecran_winner_1():
    sound_grille.stop()
    sound_winner.play(1)

#fonction qui permet d'afficher l'écran de victoire 
def ecran_winner_1():
    sound_ecran_winner_1()
    while True:
        actualization_event_winner_1()
        actualization_ecran_winner_1()
        
def ecran_winner_2():
    sound_ecran_winner_2()
    while True:
        actualization_event_ecran_winner_2()
        actualization_ecran_ecran_winner_2()

#fonction qui permet d'afficher l'écran de match 1 vs 1
def grille_1_vs_1():
    sound_grille_1_vs_1()
    while True:
        actualization_ecran_grille_1_vs_1()
        actualization_event_grille_1_vs_1()
        dessin_rect_tour_jour()
        colonne_matrice_logique()
        colonne_libre()
        logique_grille()
        dessin_rect()
        verif_diagonale()
        verif_hauteur()
        verif_largeur()
        logique_winner()
        dessin_circle_avec_mouse()

#fonction qui permet d'afficher l'écran de match 1 vs PC
def grille_PC():
    sound_grille_PC()
    while True:
        dessin_rect_tour_jour()
        actualization_ecran_grille_PC()
        actualization_event_grille_PC()
        colonne_matrice_logique()
        colonne_libre()
        logique_grille()
        dessin_rect()
        verif_diagonale()
        verif_hauteur()
        verif_largeur()
        logique_winner()
        dessin_circle_avec_mouse()
#fonction qui permet d'afficher l'écran de menu 
def menu():
    sound_sur_menu() 
    while True:
        recommencer_jeu()
        actualization_event_menu()
        actualization_ecran_menu()              
        fonction_affichag_text_menu()
#fonction qui permet d'afficher l'écran de Puissance 4
def Puissance_4():
    sound_puissance_4()
    while True :
        actualization_event_Puissance_4()
        actualization_ecran_Puissance_4()
Puissance_4()