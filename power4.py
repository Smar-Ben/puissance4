# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 20:11:09 2020

@author: Benoit
"""
from random import randint        
class Board:
    
    def __init__(self):
        #nombre de ligne
        self.row = 6
        #nombre de colonne
        self.col = 7
        #tableau de jeu
        self.tab = [ [ ' ' for i in range (self.col) ] for j in range(self.row)]
        #boléen pour voir si il y a une victoire d'un joueur
        self.victory = False
        #int qui permet de savoir quelle jouer va jouer 
        self.turn = 0
        #score qui détermine la victoire
        self.WINNING_SCORE = 10000
    
    #affiche le plateau de jeu   
    def affichage(self):
        #affichage des numéro de colonnes
        print("  "+"   ".join([ str(i) for i in range(1,self.col + 1)]))
        #texte qui est affiché entre chaque texte
        sep = [ '-' for i in range (29) ]
        print("".join(sep))
        #affichage du tableau de jeu
        for i in range(self.row):
            txt =''
            for j in range(self.col):
                txt += '| '+self.tab[i][j]+' '
            txt += '|'
            print(txt)
            print("".join(sep))
            
    #fonction qui lance le jeu
    #mode : int vaut 1 si joueur vs joueur, 2 si joueur contre IA
    def launchGame(self, mode) :
        #si le mode est en joueur contre joueur, alors le joueur qui commence est choisi aléatoirement
        if mode == 1:
            self.turn = randint(0,1)
        #boucle de jeu
        while self.victory == False:
            #affichage
            self.affichage()
            #le joueur place un jeton
            if self.turn % 2 == 0:
                print("Tour de O")
                self.selectRow()
            elif self.turn % 2 == 1 and mode == 1:
                print("Tour de X")
                self.selectRow()
            #l'ordinateur place un jeton en fonction d'une algo minmax
            else: 
                print("Tour de l'ordi")
                result = self.alphaBeta(-99999999, 99999999, 0, 4)
                self.placeToken(result[0],False)
                #utilisez fonction min-max
            #si quelqu'un n'a pas gagné ou que le plateau n'est pas rempli
            if self.victory == False and self.isFull() == False :
                self.turn += 1
            #dans le cas d'une victoire, on arrête le jeu
            elif self.victory == True :
                if self.turn % 2 == 0 :
                    self.affichage()
                    print('Vicoire de O')
                else:
                    self.affichage()
                    print('Victoire de X')
            #si il y a égalité alors on arrête le jeu
            else :
                self.affichage()
                print('Egalité')
                self.victory = True
                    
    #fonction qui retourne vrai si le plateau est rempli sinon retourne faux
    def isFull(self):
        for i in range(self.col):
            if self.tab[0][i] == " ":
                return False
        return True
    
    #fonctionne qui demande au joueur de sélectionner une colonnne
    def selectRow(self) :
        turnOver = False
        #tant que le joueur n'a pas sélectionner une colonne valide
        #alors on lui demande de sélectionner une colonne
        while turnOver == False :
            print("Selectionner une colonne :")
            choice = int(input())
            if choice >= 1 and choice <=self.col:
                if self.tab[0][choice - 1] != ' ' :
                    print("Impossible de remplir cette colonne")
                else :
                    self.placeToken(choice-1,False)
                    turnOver = True
            else :
                print("selectionnez un autre chiffe")
                
    #permet de placer un jeton
    #choice : int -> colonne où l'on place le jeton
    #isMinMax : booléen -> en foncton du booléen, on regarde ou non si le jeu est terminé
    def placeToken(self, choice, isMinMax):
        for i in range(self.row - 1, -1, -1) :
            if self.tab[i][choice] == " " :
                if self.turn % 2 == 0 :
                    self.tab[i][choice] = "O"
                    if isMinMax == False:
                        self.checkVictory(choice, i,"O")
                else:
                    self.tab[i][choice] = "X"
                    if isMinMax == False:
                        self.checkVictory(choice, i,"X")
                break
            
    #fonction qui vérifie si il y a un puissance 4 dans le jeu
    def checkVictory(self, choice, row, token):
        
        tab = self.tab
        #on vérifie si il y a un puissance quatre horizontale
        for c in range(choice-3,choice+1):
            if  (c >=0 and c + 3 < self.col) and tab[row][c] == token and tab[row][c+1] == token and tab[row][c+2] == token and tab[row][c+3] == token:
                self.victory = True
                exit()
        #on vérifie si il y a un puissance quatre verticale
        if (row + 3 < self.row) and (self.tab[row+1][choice] == token) and (self.tab[row+2][choice] == token) and (self.tab[row+3][choice] == token):
            self.victory = True 
            print
     
        #vérification verticale
        for row in range(3, self.row):
            for col in range(0, self.col - 3):
                if tab[row][col] == token and tab[row-1][col+1] == token and tab[row-2][col+2] == token and tab[row-3][col+3] == token:
                    self.victory = True
                    exit()
        #calcul diagnole
        for row in range(0, self.row - 3):
            for col in range(0, self.col - 3):
                if tab[row][col] == token and tab[row+1][col+1] == token and tab[row+2][col+2] == token and tab[row+3][col+3] == token:
                    self.victory = True
                    exit()
            
    #méthode utilisé uniquement par l'IA
    #fonction min max avec élagage alpha béta
    def alphaBeta(self, alpha, beta, deep, deep_max):
        #on calcule le score
        actualScore = self.calculScore()
        if deep == deep_max or actualScore == -self.WINNING_SCORE or actualScore == self.WINNING_SCORE or self.isFull() == True:
            return [-1, actualScore]
        #calcul du min
        elif self.turn % 2 == 0:
            score = [-1, 99999999] 
            col = self.colPossible()
            for noeud in col:
                self.placeToken(noeud,True)
                self.turn +=1
                scoreInter = self.alphaBeta(alpha, beta, deep+1, deep_max)
                if(score[0] == -1 or score[1] > scoreInter[1]):
                    score[0] = noeud
                    score[1] = scoreInter[1]
                self.removeToken(noeud)
                self.turn -=1
                if alpha > score[1]:
                    return score
                beta = min(beta, score[1])
        #calcul du max
        else:
            score = [-1, -99999999] 
            col = self.colPossible()
            for noeud in col:
                self.placeToken(noeud,True)
                self.turn +=1
                scoreInter = self.alphaBeta(alpha, beta, deep+1, deep_max)
                if(score[0] == -1 or score[1] < scoreInter[1]):
                    score[0] = noeud
                    score[1] = scoreInter[1]
                self.removeToken(noeud)
                self.turn -=1 
                if score[1] > beta:
                    return score
                alpha = max(alpha, score[1])
        return score
    
    #calcule les lignes qui ne sont pas entiérement remplies 
    def colPossible(self):
        col = []
        for i in range(self.col):
            if self.tab[0][i] == " ":
                col.append(i)
        return col
    
    #calcule le score du plateau de jeu
    def calculScore(self):
        score=[0, 0, 0, 0]
        #calcul score vertical
        for row in range(0, self.row - 3):
            for col in range(0, self.col):
                inter = self.scorePosition(row, col, 1, 0)
                #mettre condition si inter == self.WINNING_SCORE
                if inter == self.WINNING_SCORE:
                    return self.WINNING_SCORE
                elif inter == -self.WINNING_SCORE:
                    return -self.WINNING_SCORE
                score[0] += inter
        #calcul score horizontal
        for row in range(0, self.row):
            for col in range(0, self.col - 3):
                inter = self.scorePosition(row, col, 0, 1)
                #mettre condition si inter == self.WINNING_SCORE
                if inter == self.WINNING_SCORE:
                    return self.WINNING_SCORE
                elif inter == -self.WINNING_SCORE:
                    return -self.WINNING_SCORE
                score[1] += inter       
        #calcul diagnole
        for row in range(3, self.row):
            for col in range(0, self.col - 3):
                inter = self.scorePosition(row, col, -1, 1)
                #mettre condition si inter == self.WINNING_SCORE
                if inter == self.WINNING_SCORE:
                    return self.WINNING_SCORE
                elif inter == -self.WINNING_SCORE:
                    return -self.WINNING_SCORE
                score[2] += inter
        #calcul diagnole
        for row in range(0, self.row - 3):
            for col in range(0, self.col - 3):
                inter = self.scorePosition(row, col, 1, 1)
                #mettre condition si inter == self.WINNING_SCORE
                if inter == self.WINNING_SCORE:
                    return self.WINNING_SCORE
                elif inter == -self.WINNING_SCORE:
                    return -self.WINNING_SCORE
                score[3] += inter
        return sum(score)
    
    #calcul le score d'une ligne ou d'une colonne ou d'une diagonale (cela dépend de la valeur de offx et offy)
    def scorePosition(self, row, col, offx, offy):
        score_human = 0
        score_ia = 0
        for i in range(4):
            if(self.tab[row][col] ==  "O"):
                score_human += 1
            elif (self.tab[row][col] ==  "X"):
                score_ia += 1
            row += offx
            col += offy
        if score_human == 4:
            return -self.WINNING_SCORE
        elif score_ia == 4:
            return self.WINNING_SCORE
        return score_ia
    
    #enlève un jeton du plateau de jeu en fonction de la colonne selectionné
    def removeToken(self, choice):
        for i in range(6) :
            if self.tab[i][choice] != " " :
                self.tab[i][choice] = " "
                break
    
#lance le jeu
def select(choice):
    board = Board()
    #lance une partie humain contre humain
    if choice == '1' :
        board.launchGame(1)
    #lance une partie IA contre humain
    elif choice == '2' :
        board.launchGame(2)
    #quitte le jeu
    elif choice == '3' :
        print("Vous quittez le jeu")
    else :
        print("Choissisez un autre nombre\n\n33")

# fonction qui lance le jeu
def menu():
    choice = 0
    #si l'utilisateur ne quitte pas le jeu, alors c'est pas fini
    while choice != "3":
        textMenu=("Puissance 4","1.Joueur vs Joueur", "2.Joueur vs IA","3.Quitter");
        for txt in textMenu:
            print(txt)
        print("Choisir une option:")
        choice = input();
        select(choice);

menu()
#affichage([ [ ' ' for i in range (29) ] for j in range(6)]);
#affichage("df")
##fonciton qui permet d'effacer la console
