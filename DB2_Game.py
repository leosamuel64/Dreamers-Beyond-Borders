#! /usr/bin/python3

import os
import time
import random
import math
import pygame
import sys
from pygame.locals import *

"""
------------------------------  INITIALISATION DE PYGAME  ------------------------------
"""
def selectScreenSize(w,h):
    coeff=0.9
    if 0.75*w>h:
        h*=coeff
        return int(h*4/3),int(h)
    else:
        w*=coeff
        return int(w),int(w*3/4)

pygame.init()
pygame.font.init()

infoScreen = pygame.display.Info()

DISPLAY_SIZE_X,DISPLAY_SIZE_Y = selectScreenSize(infoScreen.current_w,infoScreen.current_h)


ecran = pygame.display.set_mode((DISPLAY_SIZE_X,DISPLAY_SIZE_Y))






"""
------------------------------  INITIALISATION DU MODULE SONORE  ------------------------------
"""
try:
    pygame.mixer.pre_init(44100,-16,2,2048)
    pygame.mixer.init()
except pygame.error:
    print("Avertissement #2 : Aucune interface audio trouvée  ")

pygame.display.set_caption("Loading ...")

"""
------------------------------  FONCTIONS INTERMEDIAIRES  ------------------------------    
"""



def texte(text,size):
    """
    Entrées :   - text : Texte à afficher
                - size : Taille du texte
    Sortie  :   - Le texte prêt à afficher      
    """
    f = pygame.font.Font(None,size)
    textFont = f.render(text,True,(255,255,255))
    return textFont

def HitBox(x,y,sizeX,sizeY):
    """ Créer une Hitbox rectangulaire de coin gauche supérieur x,y"""
    return  [   (x-sizeX,y-sizeY),
                (x+sizeX,y+sizeY)
            ]       

def dansBoite(box,x,y):
    """
    Entrées :   - box : Liste de tupple (représente les coordonées du coin haut gauche et bas droit d'un rectangle)
                - x : position x
                - y : possition y
    Sortie  :   - Indique si le point (x,y) est dans le rectangle représentée par box
    """
    if (x>box[0][0] and x < box[1][0]) and  (y>box[0][1] and y < box[1][1]):
        return True
    else:
        return False

def music(chemin):
    """
    Lance le son chemin et ne plante pas si il n'y a pas de moyen de lire le son
    """
    try:
        pygame.mixer.music.load(chemin)  
        pygame.mixer.music.play(-1)
    except pygame.error:
        v = os.path.exists(chemin)  ## Vérifie si le fichier existe
        if not v:
            raise Exception("Erreur #1 : Le fichier audio n'a pas été trouvé -> {}".format(chemin))
        
def image(chemin,x,y):
    """
    Creer une instance image de dimension x*y 
    """
    try:
        img = pygame.image.load(chemin)
        img = pygame.transform.scale(img, (x, y))
        return img
    except pygame.error :
        v = os.path.exists(chemin)  ## Vérifie si le fichier existe
        if not v:
            raise Exception("Erreur #3 : Le fichier image n'a pas été trouvé -> {}".format(chemin))

def transition(img,suite):
    """
    Affiche un texte, attend que l'utilisateur valide et passe à la suite
    txt : Liste des textes (chaque element du tableau correspond à une ligne)
    suite : Procédure qui ne prend pas d'argument
    """
    jeu=True
    
    while jeu:
        for event in pygame.event.get():
            if event.type == QUIT:
                jeu = False
            if event.type == KEYDOWN:
                if event.key == Tv:
                    jeu=False
                    suite()

        ecran.fill((0,0,0))
        ecran.blit(img,(0,0))
        time.sleep(0.002)
        pygame.display.flip()
            

def load_Image(path,deb,fin):
    res = ["PictureList"]
    for i in range(deb,fin+1):
        num=i
        if num<10:
            num='0'+str(num) 
        pic = pygame.image.load(path+str(num)+".png")
        pic = pygame.transform.scale(pic, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
        res.append(pic)
    return res

def load_question(path):
    CountriesList = ["CountryList"]
    AnswersList = ["AnswerList"]

    file = open(path, "r")
    lines = file.readlines()
    lines.pop(0)

    for line in lines:
        tempCountries=[]
        tempAnswers=[]
        res = line.strip().split(';')

        for i in range(1,9):
            tempCountries.append(res[i])
        for i in range(9,17):
            tempAnswers.append(int(res[i]))

        CountriesList.append(tempCountries)
        AnswersList.append(tempAnswers)

    return CountriesList,AnswersList

def load_DictCountries(path,Listpath):
    file=open(Listpath,'r')
    List=file.readlines()
    res = {}
    for i in List:
        i=i.strip()
        pic = pygame.image.load(path+i+".png")
        pic = pygame.transform.scale(pic, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
        res[i] = pic
    return res

def load_perso():
    perso=[]
    for y in range(0,DISPLAY_SIZE_Y):
        perso.append(image("Data/Layout/ballon.png",int(y/7),int(y/7)))
    return perso

def calcul_position(n):
    INTER_SIZE = 0.04*DISPLAY_SIZE_X
    B_SIZE = 0.16*DISPLAY_SIZE_X
    if n<=3:
        y=0.8*DISPLAY_SIZE_Y
    else:
        y=0.9*DISPLAY_SIZE_Y
    n=n%4
    x=(n)*B_SIZE + (n+1)*INTER_SIZE
    return (int(x),int(y))


def affiche_bouton(res,countries):
    for i in range(0,8):
        if not res[i]:
            img=pygame.transform.scale(DictCountries[countries[i]], (int(0.14*DISPLAY_SIZE_X), int(0.14*DISPLAY_SIZE_X*0.29)))
            ecran.blit(img,calcul_position(i))
        else:
            img = pygame.transform.scale(DictCountries[countries[i]+"2"], (int(0.16*DISPLAY_SIZE_X), int(0.16*DISPLAY_SIZE_X*0.29)))
            ecran.blit(img,calcul_position(i))

def clique(res):
    INTER_SIZE = 0.04*DISPLAY_SIZE_X
    B_SIZE = 0.16*DISPLAY_SIZE_X
    (1)*B_SIZE + (1+1)*INTER_SIZE
    Box1 = [((0)*B_SIZE + (0+1)*INTER_SIZE,int(0.8*DISPLAY_SIZE_Y)),(((1)*B_SIZE + (1)*INTER_SIZE,(int(0.9*DISPLAY_SIZE_Y))))]
    Box2 = [((1)*B_SIZE + (1+1)*INTER_SIZE,int(0.8*DISPLAY_SIZE_Y)),(((2)*B_SIZE + (1+1)*INTER_SIZE,(int(0.9*DISPLAY_SIZE_Y))))]
    Box3 = [((2)*B_SIZE + (2+1)*INTER_SIZE,int(0.8*DISPLAY_SIZE_Y)),((3)*B_SIZE + (2+1)*INTER_SIZE,int(0.9*DISPLAY_SIZE_Y))]
    Box4 = [((3)*B_SIZE + (3+1)*INTER_SIZE,int(0.8*DISPLAY_SIZE_Y)),(((4)*B_SIZE + (3+1)*INTER_SIZE,(int(0.9*DISPLAY_SIZE_Y))))]
    Box5 = [((0)*B_SIZE + (0+1)*INTER_SIZE,int(0.9*DISPLAY_SIZE_Y)),(((1)*B_SIZE + (0+1)*INTER_SIZE,(DISPLAY_SIZE_Y)))]
    Box6 = [((1)*B_SIZE + (1+1)*INTER_SIZE,int(0.9*DISPLAY_SIZE_Y)),(((2)*B_SIZE + (1+1)*INTER_SIZE,(DISPLAY_SIZE_Y)))]
    Box7 = [((2)*B_SIZE + (2+1)*INTER_SIZE,int(0.9*DISPLAY_SIZE_Y)),(((3)*B_SIZE + (2+1)*INTER_SIZE,(DISPLAY_SIZE_Y)))]
    Box8 = [((3)*B_SIZE + (3+1)*INTER_SIZE,int(0.9*DISPLAY_SIZE_Y)),(((4)*B_SIZE + (3+1)*INTER_SIZE,(DISPLAY_SIZE_Y)))]

    x,y = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()
    if dansBoite(Box1,x,y) and press[0]:
        res[0]=not res[0]
    if dansBoite(Box2,x,y) and press[0]:
        res[1]=not res[1]
    if dansBoite(Box3,x,y) and press[0]:
        res[2]=not res[2]
    if dansBoite(Box4,x,y) and press[0]:
        res[3]=not res[3]
    if dansBoite(Box5,x,y) and press[0]:
        res[4]=not res[4]
    if dansBoite(Box6,x,y) and press[0]:
        res[5]=not res[5]
    if dansBoite(Box7,x,y) and press[0]:
        res[6]=not res[6]
    if dansBoite(Box8,x,y) and press[0]:
        res[7]=not res[7]

def affiche_Question(res,num):
    txt = texte("Requested answers : "+str(sum(AnswersList[num])),int(0.08*DISPLAY_SIZE_Y))
    img=ImageList[num]
    Ok =image("Data/Buttons/OK.png",int(0.1*DISPLAY_SIZE_X),int(0.1*DISPLAY_SIZE_X))
    ecran.blit(img,(int(0.2*DISPLAY_SIZE_X),(int(0.05*DISPLAY_SIZE_Y))))
    clique(res)
    affiche_bouton(res,CountriesList[num])
    ecran.blit(Ok,(int(0.8*DISPLAY_SIZE_X),int(0.8*DISPLAY_SIZE_Y)))
    ecran.blit(txt,((int(0.1*DISPLAY_SIZE_X),int(0.7*DISPLAY_SIZE_Y))))


def affiche_Monument(n):
    place = [   (int(0.56*DISPLAY_SIZE_X),int(0.72*DISPLAY_SIZE_Y)),
                (int(0.36*DISPLAY_SIZE_X),int(0.77*DISPLAY_SIZE_Y)),
                (int(0.07*DISPLAY_SIZE_X),int(0.59*DISPLAY_SIZE_Y)),
                (int(0.39*DISPLAY_SIZE_X),int(0.58*DISPLAY_SIZE_Y)),
                (int(0.55*DISPLAY_SIZE_X),int(0.41*DISPLAY_SIZE_Y)),     
            ]
    for i in range (0,n+1):
        ecran.blit(monumentList[i],place[i])

def fonctionVide():
    ()

"""
------------------------------  PARAMETRES  ------------------------------
"""
load = texte("Loading...",int((0.1*DISPLAY_SIZE_X)))
ecran.blit(load,(DISPLAY_SIZE_X/4,DISPLAY_SIZE_Y/3))
pygame.display.flip()

IMAGE_SIZE_X=int(0.6*DISPLAY_SIZE_X)
IMAGE_SIZE_Y=int(IMAGE_SIZE_X*0.75)

BUTTON_SIZE_X = 100
BUTTON_SIZE_Y = 50

Tv = K_SPACE
Tz = K_UP
Tq = K_LEFT
Td = K_RIGHT
Ts = K_DOWN

"""
------------------------------  INITIALISATION DES DONNEES  ------------------------------
"""

ecran = pygame.display.set_mode((DISPLAY_SIZE_X,DISPLAY_SIZE_Y))
load = texte("Loading...",int((0.1*DISPLAY_SIZE_X)))
ecran.blit(load,(DISPLAY_SIZE_X/4,DISPLAY_SIZE_Y/3))
pygame.display.flip()

ImageList = load_Image("Data/Pictures/",1,47)

CountriesList,AnswersList = load_question("Data/Countries.csv")

DictCountries = load_DictCountries("Data/Buttons/","Data/Names.csv")

scoreList = [   image("Data/Layout/Livelmeter/Level 0.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Level 1.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Level 2.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Level 3.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Level 4.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Level 5.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Level 6.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2)),
                image("Data/Layout/Livelmeter/Livel 7 -Max.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/2))
]

persoTab=load_perso()

monumentList=[image("Data/Layout/Monuments/Francia 2.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/5)),
image("Data/Layout/Monuments/Francia.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/5)),
image("Data/Layout/Monuments/grecia.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/5)),
image("Data/Layout/Monuments/lituania.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/5)),
image("Data/Layout/Monuments/turchia.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_Y/5))
]



"""
------------------------------  SCENES DU JEU  ------------------------------
"""


def intro():
    """
    Affiche le générique d'introduction
    """

    jeu = True
        ## Taille de la police
    size = int(0.07*DISPLAY_SIZE_X)
        ## Génération des textes
    img=image("Data/Design/chargement.png",DISPLAY_SIZE_X,DISPLAY_SIZE_Y)
        ## Variable temporelle
    t=0 
        ## Temps par texte
    t1=1/3
        # Boucle de l'affichage
    while jeu:
            ## Detection de la croix
        for event in pygame.event.get():
            if event.type == QUIT:
                jeu = False

        if t < t1:
            ecran.fill((0,0,0))
            ecran.blit(img, (0,0)) 
        elif t<2*t1:
            ecran.fill((0,0,0))
            ecran.blit(img, (0,0)) 
        elif t<3*t1:
            ecran.fill((0,0,0))
            ecran.blit(img, (0,0)) 
        else:
            menu()
            jeu = False

        time.sleep(0.002)
        pygame.display.flip()
        t+=0.002
        
def menu():
    """
    Affiche le menu
    """
    jeu = True
    img=image("Data/Design/menufond.png",DISPLAY_SIZE_X,DISPLAY_SIZE_Y)
    ## Textes au repos
    optiontxt = texte("Credits",int(DISPLAY_SIZE_X/20))
    Jouertxt = texte("Play",int(DISPLAY_SIZE_X/20))
    Quittertxt = texte("Quit",int(DISPLAY_SIZE_X/20))
    
    ## Textes quand la souris passe dessus
    optiontxtS = texte("Credits",int(DISPLAY_SIZE_X/18))
    JouertxtS = texte("Play",int(DISPLAY_SIZE_X/18))
    QuittertxtS = texte("Quit",int(DISPLAY_SIZE_X/18)) 
    Merci = texte("Thank you for playing !",int(DISPLAY_SIZE_X/20))

    ## Rectangles autour des textes
    jouerBox = [(DISPLAY_SIZE_X/2,(DISPLAY_SIZE_Y/2)-100),((DISPLAY_SIZE_X/2+200,(DISPLAY_SIZE_Y/2)))]
    optionBox = [(DISPLAY_SIZE_X/2,(DISPLAY_SIZE_Y/2)),((DISPLAY_SIZE_X/2+200,(DISPLAY_SIZE_Y/2)+100))]
    QuitterBox = [(DISPLAY_SIZE_X/2,(DISPLAY_SIZE_Y/2)+100),((DISPLAY_SIZE_X/2+230,(DISPLAY_SIZE_Y/2)+200))]

    while jeu:
        ## On récupère la position de la souris
        x,y = pygame.mouse.get_pos()

        ## Detection de la croix
        for event in pygame.event.get():
                if event.type == QUIT:
                    jeu = False
        
        ecran.blit(img,(0,0))
        if dansBoite(jouerBox,x,y):
            ecran.blit(JouertxtS, jouerBox[0]) 
            
            ## Récupère l'état des boutons sous la forme d'un tupple 0/1 (Gauche,molette,Droite)
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                ## Appeller la suite ici
                music("Data/Music/Dreamersontheborder.mp3")
                img=image("Data/Design/presentation.png",DISPLAY_SIZE_X,DISPLAY_SIZE_Y)
                regle = image("Data/Design/rule.png",DISPLAY_SIZE_X,DISPLAY_SIZE_Y)
                transition(img, fonctionVide)
                transition(regle, fonctionVide)
                tableau_principal()
                jeu=False
        else:
            ecran.blit(Jouertxt, jouerBox[0])

        if dansBoite(optionBox,x,y):
            ecran.blit(optiontxtS, optionBox[0]) 
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                info()
                jeu = False
        else:       
            ecran.blit(optiontxt, optionBox[0]) 

        if dansBoite(QuitterBox,x,y):   
            ecran.blit(QuittertxtS, QuitterBox[0]) 
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                ecran.fill((0,0,0))
                ecran.blit(Merci, (DISPLAY_SIZE_X/2-200,DISPLAY_SIZE_Y/2)) 
                pygame.display.flip()
                time.sleep(1)
                jeu = False
        else:
            ecran.blit(Quittertxt, QuitterBox[0]) 

        time.sleep(0.002)
        pygame.display.flip()
    # pygame.QUIT()
    # sys.exit()

def info():
    """
    Scene du menu info avec la version ...
    """
    jeu = True
    img=image("Data/Design/credits.png",DISPLAY_SIZE_X,DISPLAY_SIZE_Y)
    # On charge les images
    flecheNorm = image("data/design/Back_Arrow.png",int(DISPLAY_SIZE_X/10),int(DISPLAY_SIZE_X/10))
    flecheBig = image("data/design/Back_Arrow.png",int(DISPLAY_SIZE_X/7),int(DISPLAY_SIZE_X/7))

    # On charge les textes
    Titre = texte("Dreamers Beyond Borders",int(DISPLAY_SIZE_X/15))
    create = texte("ERASMUS +",int(DISPLAY_SIZE_X/20))
    version = texte("Version : 1",int(DISPLAY_SIZE_X/20))
    Annee = texte("2018-2021",int(DISPLAY_SIZE_X/20))

    # Hitbox de la flèche de retour
    flecheBox = [(int(DISPLAY_SIZE_X/10),int(DISPLAY_SIZE_Y/10)),(2*int(DISPLAY_SIZE_X/10),2*int(DISPLAY_SIZE_Y/10))]

    while jeu:

            ## On récupère la possition de la souris
        x,y = pygame.mouse.get_pos()
        ecran.blit(img,(0,0))
            ## Detection de la croix
        for event in pygame.event.get():
                if event.type == QUIT:
                    jeu = False
        if dansBoite(flecheBox,x,y):
            ecran.blit(flecheBig, (flecheBox[0][0],flecheBox[0][1]))
            press = pygame.mouse.get_pressed()
            if press[0] == 1:
                menu()
                jeu=False
        else:
            ecran.blit(flecheNorm, (flecheBox[0][0],flecheBox[0][1]))

       

        time.sleep(0.002)
        pygame.display.flip()



def tableau_principal():
    jeu = True
    question = False
    vitesse=1
    score=5
    malus=100
    box1=[(int(0.56*DISPLAY_SIZE_X),int(0.72*DISPLAY_SIZE_Y)),(int(0.69*DISPLAY_SIZE_X),int(0.89*DISPLAY_SIZE_Y))]
    box2=[(int(0.36*DISPLAY_SIZE_X),int(0.77*DISPLAY_SIZE_Y)),(int(0.49*DISPLAY_SIZE_X),int(0.97*DISPLAY_SIZE_Y))]
    box3=[(int(0.07*DISPLAY_SIZE_X),int(0.59*DISPLAY_SIZE_Y)),(int(0.19*DISPLAY_SIZE_X),int(0.78*DISPLAY_SIZE_Y))]
    box4=[(int(0.39*DISPLAY_SIZE_X),int(0.58*DISPLAY_SIZE_Y)),(int(0.51*DISPLAY_SIZE_X),int(0.75*DISPLAY_SIZE_Y))]
    box5=[(int(0.55*DISPLAY_SIZE_X),int(0.41*DISPLAY_SIZE_Y)),(int(0.69*DISPLAY_SIZE_X),int(0.58*DISPLAY_SIZE_Y))]
    

    box = [box1,box2,box3,box4,box5]
    fond =  image("Data/Layout/AllexceptMonuments.png",int(DISPLAY_SIZE_X),int(DISPLAY_SIZE_Y))
    x,y=int(8*DISPLAY_SIZE_X/10),int(8*DISPLAY_SIZE_Y/10)
    momentumX=0
    momentumY=0
    monument=0
    fin=False
    # pygame.key.set_repeat(1,20)
    while jeu:
        perso = persoTab[int(y)]

        for event in pygame.event.get():
            if event.type == QUIT:
                jeu = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    jeu = False

                if event.key == Tz:
                    momentumY-=vitesse
                    
                if event.key == Ts:
                    momentumY+=vitesse
                    
                if event.key == Td:
                    momentumX+=vitesse
                    
                if event.key == Tq:
                    momentumX-=vitesse
                    
                if event.key == K_SPACE and monument==5 :
                    jeu=False
                    menu()
        xm,ym = pygame.mouse.get_pos()
        # print("x : "+str(x/DISPLAY_SIZE_X))
        # print("y : "+str(y/DISPLAY_SIZE_Y))
        if monument<5:
            if dansBoite(box[monument],x,y) and not fin and monument<5:
                monument+=1
                score+=2
        
        
        if not question and not fin:            
            # Calcul des coords pour la fusée et les astéroides
            if x+momentumX < DISPLAY_SIZE_X-3 and x+momentumX > 3:
                x+= momentumX
            else:
                momentumX=0

            if y+momentumY < DISPLAY_SIZE_Y-3 and y+momentumY > 3:
                y+= momentumY
            else:
                momentumY=0
            
            if abs(momentumY)+abs(momentumX) > 0:
                malus-=8

            if malus<0:
                score-=1
                malus=100
            if score <0:
                score=0
                question=True
                num = random.randint(1,len(ImageList)-1)
                res=[0,0,0,0,0,0,0,0]
            
            randX,randY=random.randint(-1,1),random.randint(-1,1)
            x+=randX
            y+=randY

            ecran.blit(fond,(0,0))
            if monument<5:
                affiche_Monument(monument)
            else:
                None
            ecran.blit(perso,(x,y))
            ecran.blit(scoreList[score%8],(10,int(0.1*DISPLAY_SIZE_Y)))
            
        else:
            ecran.blit(fond,(0,0))
            affiche_Question(res,num)
            BoiteOK = [(int(0.8*DISPLAY_SIZE_X),int(0.8*DISPLAY_SIZE_Y)),(DISPLAY_SIZE_X,DISPLAY_SIZE_Y)]
            press = pygame.mouse.get_pressed()
            xm,ym = pygame.mouse.get_pos()
            if dansBoite(BoiteOK,xm,ym) and press[0]:
                momentumX,momentumY=0,0
                if res==AnswersList[num]:
                    score+=5
                    question=False
                else:
                    num = random.randint(1,len(ImageList)-1)
                    res=[0,0,0,0,0,0,0,0]
        if monument==5:
            finimage=image("Data/Design/fin.png",DISPLAY_SIZE_X,DISPLAY_SIZE_Y)
            ecran.blit(finimage,(0,0))
            
        time.sleep(0.0166)
        pygame.display.flip()



    
        
"""
------------------------------  FINAL  ------------------------------
"""

pygame.display.set_caption("Dreamers Beyond Borders : The Game")

intro()


