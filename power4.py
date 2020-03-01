# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 20:11:09 2020

@author: Benoit
"""
#from IPython import get_ipython
from random import *


def select(choice):
    if (choice == '1') :
        lauchGame(1)
    elif (choice == '2') :
        print("j")
    elif (choice == '3') :
        print("Vous quittez le jeu")
    else :
        print("Choissisez un autre nombre\n\n33")

def init():
    return [ [ ' ' for i in range (29) ] for j in range(6)]

def affichage(tab):
    sep = [ '-' for i in range (29) ]
    print("".join(sep))
    for i in range(6):
        txt =''
        for j in range(7):
            txt += '| '+tab[i][j]+' '
        txt += '|'
        print(txt)
        print("".join(sep))

def lauchGame(mode):
    tab = init()
    gameOver = False
    turn = randint(0,1)
    while(gameOver == False):
        if (turn % 2 == 0):
            print("Tour de J1")
        else: 
            print("Tour de J2")
        affichage(tab)

def menu():
    choice = 0
    while(choice != "3"):
        textMenu=("Puissance 4","1.Joueur vs Joueur", "2.Joueur vs IA","3.Quitter");
        for txt in textMenu:
            print(txt)
        print("Choisir une option:")
        choice = input();
        select(choice);
#menu();
#affichage("df")
print()
##fonciton qui permet d'effacer la console
#get_ipython().magic('clear')
