import sys
import pandas as pd
import numpy as np
import copy
import random

## N Queens Problem

# Number of backtracks
backtracks = 0

#This is the class representing the board state. Shows board, current player and winner
class State:
    def __init__(self, length):
        self.board = generateBoard(length)
        self.length = length
        self.constraints = generateConstraints(length)
       

    def __str__(self):
        return "State(board='{}', length='{}')".format(self.board, self.length)
    
    def __repr__(self):
        return str(self)
    

def regenerateConstraints(state, newQueen):
    constraints = copy.deepcopy(state.constraints)
    length = state.length
    boardLength = len(state.board)
    constraints[boardLength - 1] = [newQueen]
    for i in range(boardLength, length):
        #print("I:" + str(i))
        # Horizontal check
        if(newQueen in constraints[i]):
            constraints[i].remove(newQueen)
            #print("Horizontal Check:" + str(constraints[i]))
        # Diagonal check
        diagonalCheck = i - (boardLength - 1)
        # Upwards diagonal
        if(newQueen + diagonalCheck in constraints[i]):
            constraints[i].remove(newQueen+diagonalCheck)
            #print(constraints[i])
        # Downwards diagonal
        if(newQueen - diagonalCheck in constraints[i]):
            constraints[i].remove(newQueen-diagonalCheck)
            #print(constraints[i])
    return constraints

def generateConstraints(length):
    w, h = length, length
    matrix = [[0 for x in range(w)] for y in range(h)]
    for i in range(length):
        for j in range(length):
            matrix[i][j] = j
    return matrix

def checkConstraintError(constraints, length):
    for i in range(length):
        if(not bool(constraints[i])):
           return True
    return False


def backtrack(state, algorithm_type):
    if(algorithm_type == "basic"):
        return basic(state)
    elif(algorithm_type == "forward"):
        return forward(state)
    else:
        return "error"


def basic(state):
    global backtracks
    if queensFilled(state):
        return state
    for i in range(state.length):
        state.board.append(i)
        if(checkCollisions(state) == 0):
            recursiveState = copy.deepcopy(state)
            result = basic(recursiveState)
            if result is not None:
                return result
        state.board.pop()
    #print(state.board)
    backtracks += 1
    return None

def forward(state):
    global backtracks
    if queensFilled(state):
        return state
    for i in range(state.length):
        state.board.append(i)
        currentLength = len(state.board)
        if(checkCollisions(state) == 0):
            constraints = state.constraints
            if(i in constraints[currentLength-1]):
                recursiveState = copy.deepcopy(state)
                constraints = regenerateConstraints(state, i)
                #print(i)
                #print(constraints)
                if(not checkConstraintError(constraints, state.length)):
                    recursiveState.constraints = constraints
                    result = forward(recursiveState)
                    if result is not None:
                        return result
        state.board.pop()
    #print(state.board)
    backtracks += 1
    return None


def queensFilled(state):
    board = state.board
    if len(board) == state.length:
        return True
    return False

def checkCollisions(state):
    board = state.board
    n = len(board)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            #Same row
            if board[i] == board[j]:
                attacks += 1
            #Same diagonal
            elif abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks

def generateBoard(n):
    return []

def boardVisualization(state):
    arr = [['0' for j in range(state.length)] for i in range(state.length)]
    for i in range(state.length):
        if(len(state.board) > i):
            arr[state.board[i]][i] = 'Q'
    for j in range(state.length):
        print(arr[j])

def queenPrinter(board):
    stringBuilder = "\nSolution: "
    for i in range(len(board)):
        stringBuilder = stringBuilder + "Q" + str(i) + "= " + str(board[i]) + ", "
    stringBuilder = stringBuilder.removesuffix(", ")
    print(stringBuilder)
    

def main():
    algorithm_type = sys.argv[1]
    size = int(sys.argv[2])
    state = State(size)

    state = backtrack(state, algorithm_type)
     

    queenPrinter(state.board)
    print("Backtrack count: " + str(backtracks))
    boardVisualization(state)


if __name__ == "__main__":
    main()
