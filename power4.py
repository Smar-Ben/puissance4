# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 20:11:09 2020

@author: Benoit
"""
from random import randint



class IA:
    def __init__(self, board):
        self.board = board
        self.turn = 1
        self.WINNING_SCORE = 100000
    
    
    def start(self):
        result = self.alphaBeta(-99999999, 99999999, 1, 4)
        return result[0]
    
    def alphaBeta(self, alpha, beta, deep, deep_max):
        if deep == deep_max:
            return [-1,self.calculScore()]
        #calcul du min
        elif self.turn % 2 == 0:
            score = [-1, 99999999] 
            col = self.colPossible()
            for noeud in col:
                self.placeToken(noeud)
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
                """
                beta = min(beta, score[1])
                if alpha >= beta:
                    return score
                """
        #calcul du max
        else:
            score = [-1, -99999999] 
            col = self.colPossible()
            for noeud in col:
                self.placeToken(noeud)
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
                """
                alpha = max(alpha, score[1])
                if beta >= alpha:
                    return score
                """
        return score
    
    def colPossible(self):
        col = []
        for i in range(7):
            if self.board[0][i] == " ":
                col.append(i)
        return col
    
    
    def calculScore(self):
        score=[0, 0, 0, 0]
        #calcul score vertical
        for row in range(0, 3):
            for col in range(0, 7):
                inter = self.scorePosition(row, col, 1, 0)
                #mettre condition si inter == self.WINNING_SCORE
                if inter == self.WINNING_SCORE:
                    return inter
                elif inter == -self.WINNING_SCORE:
                    return inter
                score[0] += inter
        #calcul score horizontal
        for row in range(0, 6):
            for col in range(0, 4):
                inter = self.scorePosition(row, col, 0, 1)
                #mettre condition si inter == self.WINNING_SCORE
                score[1] += inter       
        #calcul diagnole
        for row in range(3, 6):
            for col in range(0, 4):
                inter = self.scorePosition(row, col, -1, 1)
                #mettre condition si inter == self.WINNING_SCORE
                score[2] += inter
        #calcul diagnole
        for row in range(0, 3):
            for col in range(0, 4):
                inter = self.scorePosition(row, col, 1, 1)
                #mettre condition si inter == self.WINNING_SCORE
                score[3] += inter
        return sum(score)
    
    
    def affichage(self):
        print("  "+"   ".join([ str(i) for i in range(1,8)]))
        sep = [ '-' for i in range (29) ]
        print("".join(sep))
        for i in range(6):
            txt =''
            for j in range(7):
                txt += '| '+self.board[i][j]+' '
            txt += '|'
            print(txt)
            print("".join(sep))
            
    def scorePosition(self, row, col, offx, offy):
        score_human = 0
        score_ia = 0
        for i in range(4):
            if(self.board[row][col] ==  "O"):
                score_human += 1
            elif (self.board[row][col] ==  "X"):
                score_ia += 1
            row += offx
            col += offy
        if score_human == 4:
            return -self.WINNING_SCORE
        elif score_ia == 4:
            return self.WINNING_SCORE
        return score_ia
        
     
    def placeToken(self, choice):
        for i in range(5, -1, -1) :
            if self.board[i][choice] == " " :
                if self.turn % 2 == 0 :
                    self.board[i][choice] = "O"
                else:
                    self.board[i][choice] = "X"
                break
        
    def removeToken(self, choice):
        for i in range(6) :
            if self.board[i][choice] != " " :
                self.board[i][choice] = " "
                break
        
class Board:
    def __init__(self):
        self.tab = [ [ ' ' for i in range (29) ] for j in range(6)]
        self.victory = False
        self.turn = 0
        
    def affichage(self):
        print("  "+"   ".join([ str(i) for i in range(1,8)]))
        sep = [ '-' for i in range (29) ]
        print("".join(sep))
        for i in range(6):
            txt =''
            for j in range(7):
                txt += '| '+self.tab[i][j]+' '
            txt += '|'
            print(txt)
            print("".join(sep))
    
    def launchGame(self, mode) :
        if mode == 1:
            self.turn = randint(0,1)
        while self.victory == False:
            self.affichage()
            if self.turn % 2 == 0:
                print("Tour de J1")
                self.selectRow()
            elif self.turn % 2 == 1 and mode == 1:
                print("Tour de J2")
                self.selectRow()
            else: 
                print("Tour de l'ordi")
                next_coup = IA(self.tab)
                col = next_coup.start()
                self.placeToken(col+1)
                #utilisez fonction min-max
            if self.victory == False :
                self.turn += 1
            else :
                if self.turn % 2 == 0 :
                    self.affichage()
                    print('Vicoire de J1')
                else:
                    self.affichage()
                    print('Victoire de J2')
        
    def selectRow(self) :
        turnOver = False
        while turnOver == False :
            print("Selectionner une colonne :")
            choice = int(input())
            if choice >= 1 and choice <=7:
                if self.tab[0][choice - 1] != ' ' :
                    print("Impossible de remplir cette colonne")
                else :
                    self.placeToken(choice)
                    turnOver = True
            else :
                print("selectionnez un autre chiffe")
    
    def placeToken(self, choice):
        for i in range(5, -1, -1) :
            if self.tab[i][choice-1] == " " :
                if self.turn % 2 == 0 :
                    self.tab[i][choice-1] = "O"
                    self.checkVictory(choice-1, i,"O")
                else:
                    self.tab[i][choice-1] = "X"
                    self.checkVictory(choice-1, i,"X")
                break
            
    def checkVictory(self, choice, row, token):
        tab = self.tab
        for c in range(choice-3,choice+1):
            if  (c >=0 and c < 7) and tab[row][c] == token and tab[row][c+1] == token and tab[row][c+2] == token and tab[row][c+3] == token:
                self.victory = True
                exit()
        if (row + 3 <= 5) and (self.tab[row+1][choice] == token) and (self.tab[row+2][choice] == token) and (self.tab[row+3][choice] == token):
            self.victory = True 
     
        
        for c in range(0,4):
            if row - c >= 0 and row  -c + 3 <6:
                if choice-c>=0 and choice - c + 3 <7 and tab[row-c][choice-c] == token and tab[row-c+1][choice-c+1] == token and tab[row-c+2][choice-c+2] == token and tab[row-c+3][choice-c+3] == token:
                    self.victory = True
                    print(c)
                    exit()
                if choice-c-3>=0 and tab[row-c][choice-c] == token and tab[row-c+1][choice-c-1] == token and tab[row-c+2][choice-c-2] == token and tab[row-c+3][choice-c-3] == token:
                    self.victory = True
                    print(c)
                    exit()

def select(choice):
    board = Board()
    if choice == '1' :
        board.launchGame(1)
    elif choice == '2' :
        board.launchGame(2)
    elif choice == '3' :
        print("Vous quittez le jeu")
    else :
        print("Choissisez un autre nombre\n\n33")
    
def menu():
    choice = 0
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
