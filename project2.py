#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 2: Connect Four
Hadley Lim
4 March 2022
"""

from board import Board
from player import Player
from gamestate import GameState

table = {}
ncols = 0
nrows = 0
inarow = 0
pruned = 0

class State():
    def __init__(self):
        self.board = Board(nrows, ncols, inarow)
    def __hash__(self):
        return hash(self.board)
    def __eq__(self, other):
        return self.board == other.board

def printTable(table):
    for state in table:
        print("\nSTATE:", table[state], "\n", state.board.to_2d_string())

def utility(state):
    util = -420
    gameState = state.board.get_game_state()
    if gameState == GameState.TIE:
        util = 0
    elif gameState == GameState.MAX_WIN:
        util = 1
    elif gameState == GameState.MIN_WIN:
        util = -1
    else:
        print("Error. Game is in progress.")
    moves = state.board.get_number_of_moves()
    return util * int(10000.0 * nrows * ncols / moves)

def consecExists(state, consec, playing):
    #Adapted from Prof. Kirlin's code
    consecConfigs = {'one free space':0, 'two free spaces': 0}
    exists = True
    for row in range (0, nrows):
        for col in range (0, ncols):
            if state.board.board[row][col] == 0:
                    continue
            """
            CHECKING FOR MATCHES IN A ROW
            """
            if (col <= ncols - consec):
                for i in range (0, consec - 1):
                    if state.board.board[row][col + i] != playing or \
                       state.board.board[row][col + i] != state.board.board[row][col + i + 1]:
                        exists = False
                        break
                    else: 
                        exists = True
                if exists: 
                    freeSpace = 0
                    # check for empty spaces
                    if col + consec < ncols:
                        if state.board.board[row][col + consec] == 0: 
                            freeSpace += 1
                    if col - 1 > -1:
                        if state.board.board[row][col - 1] == 0:
                            freeSpace += 1
                    if freeSpace == 1:
                        consecConfigs['one free space'] += 1
                    if freeSpace == 2:
                        consecConfigs['two free spaces'] += 1

            """
            CHECKING FOR MATCHES IN A COL
            """            
            if (row <= nrows - consec):
                for i in range (0, consec - 1):
                    if state.board.board[row + i][col] != playing or \
                       state.board.board[row + i][col] != state.board.board[row + i + 1][col]:
                        exists = False
                        break
                    else: 
                        exists = True
                if exists: 
                    freeSpace = 0
                    #check for empty spaces
                    if row + consec <= nrows - 1:
                        if state.board.board[row + consec][col] == 0: 
                            freeSpace += 1
                    #not possible for there to be an empty space below a piece
                    if freeSpace == 1:
                        consecConfigs['one free space'] += 1

            """
            CHECKING FOR MATCHES IN A NE DIAGONAL
            """            
            if (row <= nrows - consec and col <= ncols - consec):
                for i in range (0, consec - 1):
                    if state.board.board[row + i][col + i] !=  playing or \
                       state.board.board[row + i][col + i] != state.board.board[row + i + 1][col + i + 1]:
                        exists = False
                        break
                    else: 
                        exists = True
                if exists: 
                    #check for empty spaces
                    freeSpace = 0
                    if row + consec < nrows and col + consec < ncols:
                        if state.board.board[row + consec][col + consec] == 0: 
                            freeSpace += 1
                    if row - 1 > -1 and col - 1 > -1:
                        if state.board.board[row - 1][col - 1] == 0:
                            freeSpace += 1
                    if freeSpace == 1:
                        consecConfigs['one free space'] += 1
                    if freeSpace == 2:
                        consecConfigs['two free spaces'] += 1

            """
            CHECKING FOR MATCHES IN A NW DIAGONAL
            """         
            if (row <= nrows - consec and col - consec >= -1):
                for i in range (0, consec - 1):
                    if state.board.board[row + i][col - i] !=  playing or \
                       state.board.board[row + i][col - i] != state.board.board[row + i + 1][col - i - 1]:
                        exists = False
                        break
                    else:
                        exists = True
                if exists: 
                    #check for empty spaces
                    freeSpace = 0
                    if row - 1 > -1 and col + 1 < ncols:
                        if state.board.board[row - 1][col + 1] == 0: 
                            freeSpace += 1
                    if row + consec < nrows and col - consec > -1:
                        if state.board.board[row + consec][col - consec] == 0:
                            freeSpace += 1
                    
                    if freeSpace == 1:
                        consecConfigs['one free space'] += 1
                    if freeSpace == 2:
                        consecConfigs['two free spaces'] += 1
    return consecConfigs

def evaluate(state): 
    threeConfigsMax = consecExists(state, 3, 1)
    threeConfigsMin = consecExists(state, 3, -1)
    twoConfigsMax = consecExists(state, 2, 1)
    twoConfigsMin = consecExists(state, 2, -1)
    
    return threeConfigsMax['one free space']*13 + threeConfigsMax['two free spaces']*20 + \
           twoConfigsMax['one free space']*3 + twoConfigsMax['two free spaces']*5 + \
           threeConfigsMin['one free space']*-13 + threeConfigsMin['two free spaces']*-20 + \
           twoConfigsMin['one free space']*-3 + twoConfigsMin['two free spaces']*-5

def actions(state):
    moves = []
    for col in range (0, ncols):
        if not state.board.is_column_full(col):
            moves.append(col)
    return moves

def result(state, action):
    newBoard = state.board.make_move(action)
    return newBoard

"""
PART A
"""
def minimax_search(state, table):
    if state in table:
        return table[state]
    elif state.board.get_game_state() != GameState.IN_PROGRESS:
        util = utility(state)
        info = {'value': util, 'action' :None}
        table[state] = info
        return info
    elif state.board.get_player_to_move_next() == Player.MAX:
        v = -99999999
        bestMove = None
        for action in actions(state):
            child_state = State()
            child_state.board = result(state, action)
            child_info = minimax_search(child_state, table)
            v2 = child_info['value']
            if v2 > v:
                v = v2
                bestMove = action
        info = {'value': v, 'action':bestMove}
        table[state] = info
        return info
    else:
        v = 99999999
        bestMove = None
        for action in actions(state):
            child_state = State()
            child_state.board = result(state, action)
            child_info = minimax_search(child_state, table)
            v2 = child_info['value']
            if v2 < v:
                v = v2
                bestMove = action
        info = {'value':v, 'action':bestMove}
        table[state] = info
        return info

"""
PART B
"""
def ab_search(state, alpha, beta, table):
    global pruned
    if state in table:
        return table[state]
    elif state.board.get_game_state() != GameState.IN_PROGRESS:
        util = utility(state)
        info = {'value': util, 'action':None}
        table[state] = info
        return info
    elif state.board.get_player_to_move_next() == Player.MAX:
        v = -float('inf')
        bestMove = None
        for action in actions(state):
            child_state = State()
            child_state.board = result(state, action)
            child_info = ab_search(child_state, alpha, beta, table)
            v2 = child_info['value']
            if v2 > v:
                v = v2
                bestMove = action
                alpha = max(alpha, v)
            if v >= beta:
                pruned = pruned + 1
                return {'value': v, 'action': bestMove}
        info = {'value': v, 'action':bestMove}
        table[state] = info
        return info
    else:
        v = float('inf')
        bestMove = None
        for action in actions(state):
            child_state = State()
            child_state.board = result(state, action)
            child_info = ab_search(child_state, alpha, beta, table)
            v2 = child_info['value']
            if v2 < v:
                v = v2
                bestMove = action
                beta = min(beta, v)
            if v <= alpha:
                pruned += 1
                return {'value':v, 'action':bestMove}
        info = {'value':v, 'action':bestMove}
        table[state] = info
        return info

"""
PART C
"""
def ab_heuristic_search(state, alpha, beta, depth, table):
    global pruned
    if state in table:
        return table[state]
    elif state.board.get_game_state() != GameState.IN_PROGRESS:
        util = utility(state)
        info = {'value': util, 'action':None}
        table[state] = info
        return info
    elif depth == cutoff:
        heuristic = evaluate(state)
        info = {'value':heuristic, 'action':None} #cut off tree here
        table[state] = info
        return info
    elif state.board.get_player_to_move_next() == Player.MAX:
        v = -float('inf')
        bestMove = None
        for action in actions(state):
            child_state = State()
            child_state.board = result(state, action)
            child_info = ab_heuristic_search(child_state, alpha, beta, depth+1, table)
            v2 = child_info['value']
            if v2 > v:
                v = v2
                bestMove = action
                alpha = max(alpha, v)
            if v >= beta:
                pruned = pruned + 1
                return {'value': v, 'action': bestMove}
        info = {'value': v, 'action':bestMove}
        table[state] = info
        return info
    else:
        v = float('inf')
        bestMove = None
        for action in actions(state):
            child_state = State()
            child_state.board = result(state, action)
            child_info = ab_heuristic_search(child_state, alpha, beta, depth+1, table)
            v2 = child_info['value']
            if v2 < v:
                v = v2
                bestMove = action
                beta = min(beta, v)
            if v <= alpha:
                pruned += 1
                return {'value':v, 'action':bestMove}
        info = {'value':v, 'action':bestMove}
        table[state] = info
        return info    
"""
MAIN
"""
part = input("Run part A, B, or C? ")
verbose = input("Include debugging info? (y/n)")
nrows = int(input("Enter the number of rows: "))
ncols = int(input("Enter the number of columns: "))
inarow = int(input("Enter number in a row to win: "))
if part == 'c' or part == 'C':
    cutoff = int(input("Number of moves to look ahead (depth): "))

#make starting state for search
initState = State()
initState.board = Board(nrows, ncols, inarow)

if part == 'A' or part == 'a':
    outcome = minimax_search(initState, table)
    print("\nTransposition table has", len(table), "states.")
    if verbose == 'y': printTable(table)
if part == 'B' or part == 'b':
    outcome = ab_search(initState, -float('inf'), float('inf'), table)
    print("\nTransposition table has", len(table), "states.")
    if verbose == 'y': printTable(table)

if part == 'B' or part == 'b': print("The tree was pruned", pruned, "times.")

if part == 'A' or part == 'a' or part == 'B' or part == 'b':
    if outcome['value'] > 0 : print("\nFirst Player has a guaranteed win with perfect play.")
    elif outcome['value'] < 0 : print("\nSecond Player has a guaranteed win with perfect play.")
    else: print("\nA tie is guaranteed win with perfect play.")

#game against computer
go = 'y'
while go == 'y':
    first = int(input("Who plays first? 1 = human, 2 = computer: "))
    players = {}
    if first == 1: players = {1: "MAX", 2: "MIN"}
    else: players = {2: "MAX", 1: "MIN"}
    
    playing = first    
    currentState = initState
    
    while currentState.board.get_game_state() == GameState.IN_PROGRESS:
        print(currentState.board.to_2d_string())
        
        if (part == 'b' or part == 'B') and currentState not in table: #suboptimal move chosen for B
            print("This is a state that was previously pruned; re-running alpha beta from here.")
            table = {}
            ab_search(currentState, -float('inf'), float('inf'), table)

        if part == 'c' or part == 'C':
            table = {}
            ab_heuristic_search(currentState, -float('inf'), float('inf'), 0, table)
            print("\nTransposition table has", len(table), "states.")
            print("The tree was pruned", pruned, "times.")
        
        print("Minimax value for this state:", str(table[currentState]['value']) + \
              ", optimal move:", table[currentState]['action'])
        
        print("It's ", players[playing], "'s turn!")
        
        if playing == 1:
            move = int(input("Enter move: "))
            currentState.board = currentState.board.make_move(move)
    
        else: 
            print("Computer chooses move: ", table[currentState]['action'])
            currentState.board = currentState.board.make_move(table[currentState]['action'])
    
        if playing == 1: playing = 2
        else: playing = 1

    print("\nGame Over!\n" + currentState.board.to_2d_string())
    if currentState.board.get_game_state() == GameState.MAX_WIN and first == 1:     
        print("The winner is MAX! (player)")
    elif currentState.board.get_game_state() == GameState.MAX_WIN and first == 2: 
        print("The winner is MAX! (computer)")
    elif currentState.board.get_game_state() == GameState.MIN_WIN and first == 1:
        print("The winner is MIN! (computer)")
    elif currentState.board.get_game_state() == GameState.MIN_WIN and first == 2:
        print("The winner is MIN! (player)")
    else:
        print("It was a tie!")
    
    go = input("Play again? (y/n):")
    
    if go == 'y':
        #reset state
        currentState = State()
        initState.board = Board(nrows, ncols, inarow)