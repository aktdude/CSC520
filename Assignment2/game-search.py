import sys
import pandas as pd
import numpy as np
import copy

#This is the class representing the board state. Shows board, current player and winner
class State:
    def __init__(self, board):
        self.board = board
        self.current = whichStart(board)
        self.winner = check_winner(board)

    def __str__(self):
        return "State(board='{}',current='{}', winner='{}' )".format(self.board, self.current, self.winner)
    
    def __repr__(self):
        return str(self)
    



# Temp nodes_number assignment
global nodes_number
nodes_number = 1

# This function determines who is going first based on the start state
def whichStart(start_state):
    counts = {0: 0, 1: 0, 2: 0}
    for row in start_state:
        for num in row:
            counts[num] += 1
    if(counts[0] == 0):
        return 3
    elif((counts[1] + counts[2]) % 2 == 0):
        return 1
    else:
        return 2

# This checks who won the game or if no one won
def check_winner(board):
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0

# This function simply converts from the winner integer to the message I want to show
def check_winner_int(winner_to_check):
    if(winner_to_check == 0):
        return "Tied"
    elif(winner_to_check == 1):
        return "Player 1"
    elif(winner_to_check == 2):
        return "Player 2"
    else:
        return "Error"

# This begins the minimax algorithm by sending to the max first. It returns a single action
def minimax(initial_state):
    result = max_value(initial_state, initial_state.current, 0)
    best_move = result[1]
    return best_move

# The maximizer function for minimax
def max_value(state, maximizer, depth):
    #print(state)
    board = state.board
    state.winner = check_winner(board)
    # Winner Check
    global nodes_number
    if(state.winner != 0):
        if(state.winner == maximizer):
            return 100 - depth, 999
        else:
            return -100 + depth, -999
    elif(state.current == 3):
        return 0, 0
    # Initialize best_value and best_move
    best_value = float('-inf')
    best_move = 0
    # Check all possible moves
    for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                   
                    nodes_number = nodes_number + 1
                    board[i][j] = state.current
                    recursive_state = State(copy.deepcopy(board))
                    board[i][j] = 0  
                    state.board = board
                    # Go down the recursive path
                    result = min_value(recursive_state, maximizer, depth + 1)
                    value = result[0]
                    if value > best_value:
                        best_value = value
                        best_move = (i, j)
    return best_value, best_move

#Minimizer for minimax, same as maximizer except reverse goal.
def min_value(state, maximizer, depth):
    #print(state)
    global nodes_number
    board = state.board
    state.winner = check_winner(board)
    # Winner Check
    if(state.winner != 0):
        #nodes_number = nodes_number + 1
        if(state.winner == maximizer):
            return 100 - depth, 999
        else:
            return -100 + depth, -999
    elif(state.current == 3):
        #nodes_number = nodes_number + 1
        return 0, 0
    # Initialize best_value and best_move
    best_value = float('inf')
    best_move = 0
    # Check all possible moves
    for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    nodes_number = nodes_number + 1
                    board[i][j] = state.current
                    recursive_state = State(copy.deepcopy(board))
                    board[i][j] = 0  
                    state.board = board
                    # Go down the recursive path
                    result = max_value(recursive_state, maximizer, depth + 1)
                    value = result[0]
                    if value < best_value:
                        best_value = value
                        best_move = (i, j)
    return best_value, best_move 
   
# Starting position for alpha beta
def alpha_beta_search(initial_state):
    result = max_ab_value(initial_state, initial_state.current, 0, float('-inf'), float('inf'))
    best_move = result[1]
    return best_move

# Same as maximizer for minimax with pruning
def max_ab_value(state, maximizer, depth, alpha, beta):
    #print(state)
    board = state.board
    state.winner = check_winner(board)
    if(state.winner != 0):
        global nodes_number
        if(state.winner == maximizer):
            return 100 - depth, 999
        else:
            return -100 + depth, -999
    elif(state.current == 3):
        return 0, 0
    best_value = float('-inf')
    best_move = 0
    for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    nodes_number = nodes_number + 1
                    board[i][j] = state.current
                    recursive_state = State(copy.deepcopy(board))
                    board[i][j] = 0  
                    state.board = board
                    # Go down the recursive path
                    result = min_ab_value(recursive_state, maximizer, depth + 1, alpha, beta)
                    value = result[0]
                    if value > best_value:
                        best_value = value
                        best_move = (i, j)
                    # Added pruning step
                    if(best_value >= beta):
                        return best_value, best_move
                    if(best_value > alpha):
                        alpha = best_value
    return best_value, best_move

# Same as minimizer for minimax with pruning
def min_ab_value(state, maximizer, depth, alpha, beta):
    #print(state)
    board = state.board
    state.winner = check_winner(board)
    if(state.winner != 0):
        global nodes_number
        #nodes_number = nodes_number + 1
        if(state.winner == maximizer):
            return 100 - depth, 999
        else:
            return -100 + depth, -999
    elif(state.current == 3):
        #nodes_number = nodes_number + 1
        return 0, 0
    best_value = float('inf')
    best_move = 0
    for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    nodes_number = nodes_number + 1
                    board[i][j] = state.current
                    recursive_state = State(copy.deepcopy(board))
                    board[i][j] = 0  
                    state.board = board
                    # Go down the recursive path
                    result = max_ab_value(recursive_state, maximizer, depth + 1, alpha, beta)
                    value = result[0]
                    if value < best_value:
                        best_value = value
                        best_move = (i, j)
                    # Added pruning step
                    if(best_value <= alpha):
                        return best_value, best_move
                    if(best_value < beta):
                        beta = best_value
    return best_value, best_move

# Algorithm for processing move by move
def tic_tac_toe(state, algorithm):
    global nodes_number
    nodes_number = 1
    first_nodes_number = 0
    #Print initial state
    print(array_to_string(state.board) + '\n' + "------------\n")
    # while moves can be made and there is no winner
    while(state.current != 3 and state.winner == 0):
        nodes_number = 1
        if(algorithm == 'a'):
            result = minimax(state)
        elif(algorithm == 'b'):
            result = alpha_beta_search(state)
        state.board[result[0]][result[1]] = state.current
        print(array_to_string(state.board) + '\n' + "------------\n")
        first_nodes_number = max(nodes_number, first_nodes_number)
        # New State values
        state.current = whichStart(state.board)
        state.winner = check_winner(state.board)
    nodes_number = first_nodes_number
    return state.board, state.winner



# Given the string from the parameter, turn into an array
def string_to_array(string):
    numbers = string.split(',')
    array = []
    for number in numbers:
        array.append([int(x) for x in number.split()])
    return array

# Given the array, turn it into a string in the wanted format
def array_to_string(array):
    #Special formatting for first row
    result = "[["
    row1 = False
    for row in array:
        if( row1 ):
            result += " ["
        result += " ".join(str(x) for x in row) + "]\n"
        row1 = True
    # Special formatting for last row
    result = result[:-1]
    result += "]"
    return result

# Get the game type from the arguments
game_type = sys.argv[1]
minimax_bool = False
alphabeta_bool = False
if(game_type == 'a'):
    minimax_bool = True
elif(game_type == 'b'):
    alphabeta_bool = True
else:
    sys.exit('You must choose a for minimax or b for alpha-beta pruning')

# Get start state from parameter
start_board = string_to_array(sys.argv[2])
start_state = State(start_board)
result = 0

#Check starting player
start_player = start_state.current

#Output
print("Starting player: ")
if(start_player == 1):
    print("Player 1\n")
elif(start_player == 2):
    print("Player 2\n")
else:
    print("No moves left\n")



if(minimax_bool is True):
    print("Chosen Algorithm: Minimax\n")
    print("Sequence of board states:\n")
    result = tic_tac_toe(start_state, 'a')
    
if(alphabeta_bool is True):
    print("Chosen Algorithm: Alpha Beta Pruning \n")
    print("Sequence of board states:\n")
    result = tic_tac_toe(start_state, 'b')
    
winner = result[1]





if(result == 0):
    print("There was an error because result never changed")
else:
    winner_print = check_winner_int(winner)
    print("Winner: " + winner_print + '\n')
    print("Number of game tree nodes: " + str(nodes_number) + '\n')
    
    
