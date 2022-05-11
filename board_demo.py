from board import Board

def consecExists(state, consec, playing):
    #Adapted from Prof. Kirlin's code
    nrows = 3
    ncols = 3
    consecConfigs = {'one free space':0, 'two free spaces': 0}
    freeSpace = 0
    exists = True
    for row in range (0, nrows):
        for col in range (0, ncols):
            #print("looking at", row, col, state.board[row][col])
            if state.board[row][col] == 0:
                    continue
                
            if (col <= ncols - consec): #checking for matches in a row
                for i in range (0, consec - 1):
                    if state.board[row][col + i] != playing or \
                       state.board[row][col + i] != state.board[row][col + i + 1]:
                        exists = False
                        break
                    else: 
                        exists = True
                if exists: 
                    #at the end of a config, check for empty spaces
                    if col + consec < ncols:
                        print("checking end of config: col", col + consec, state.board[row][col + consec])
                        if state.board[row][col + consec] == 0: 
                            freeSpace += 1
                    if col - 1 > -1:
                        print("checking beginning of config, col", col - 1, state.board[row][col - 1])
                        if state.board[row][col - 1] == 0:
                            freeSpace += 1
                    if freeSpace == 1:
                        consecConfigs['one free space'] = 1
                    if freeSpace == 2:
                        consecConfigs['two free spaces'] += 1
                        
            if (row <= nrows - consec): #checking for matches in a col
                for i in range (0, consec - 1):
                    if state.board[row + i][col] != playing or \
                       state.board[row + i][col] != state.board[row + i + 1][col]:
                        exists = False
                        break
                    else: 
                        exists = True
                if exists: 
                    #at the end of a config, check for empty spaces
                    if row + consec < nrows:
                        print("checking end of config, row", row + consec, state.board[row + consec][col])
                        if state.board[row + consec][col] == 0: 
                            freeSpace += 1
                    if row - 1 > -1:
                        print("checking beginning of config, row", row - 1, state.board[row - 1][col])
                        if state.board[row - 1][col] == 0:
                            freeSpace += 1
                    if freeSpace == 1:
                        consecConfigs['one free space'] = 1
                    if freeSpace == 2:
                        consecConfigs['two free spaces'] += 1
                        
            if (row <= nrows - consec and col <= ncols - consec): #ne diagonal
                for i in range (0, consec - 1):
                    if state.board[row + i][col + i] !=  playing or \
                       state.board[row + i][col + i] != state.board[row + i + 1][col + i + 1]:
                        exists = False
                        break
                    else: 
                        exists = True
                #if exists: 
                    #print(consec, "found in a ne diag", row, col)
                    #TODO: numExist += 1
                        
            if (row <= nrows - consec and col - consec >= -1): #nw diagonal
                for i in range (0, consec - 1):
                    if state.board[row + i][col - i] !=  playing or \
                       state.board[row + i][col - i] != state.board[row + i + 1][col - i - 1]:
                        exists = False
                        break
                    else:
                        exists = True
                #if exists: 
                    #print(consec, "found in a nw diag", row, col)
                    #numExist += 1
    return consecConfigs

def evaluate(state): 
    #print(state.board.to_2d_string())

    return consecExists(state, 3, 1) * 10 + consecExists(state, 3, -1) * -10 \
         + consecExists(state, 2, 1) * 3 + consecExists(state, 2, -1) * -3


def main():
    board = Board(6, 7, 4) # standard connect 4 size
    print("Here is the board:")
    print(board.to_2d_string())

	# MAX(X) makes a move
    board = board.make_move(3)
    print("Here is the updated board:")
    print(board.to_2d_string())

	# MIN(O) makes a move
    board = board.make_move(2)
    print("Here is the updated board:")
    print(board.to_2d_string())

	# Check	the game progress:
    print("State of the game:", board.get_game_state())

	# Demo with a smaller board:
    board = Board(3, 3, 2) # a rather silly game
    print("Here is the board:")
    print(board.to_2d_string())

    # MAX(X) makes a move
    board = board.make_move(2)
    print("Here is the updated board:")
    print(board.to_2d_string())

	# MIN(O) makes a move
    board = board.make_move(1)
    print("Here is the updated board:")
    print(board.to_2d_string())

    # MAX(X) makes a move
    board = board.make_move(2)
    print("Here is the updated board:")
    print(board.to_2d_string())

    # Check	the game progress:
    print("State of the game:", board.get_game_state())
    print(consecExists(board, 2, 1))

main()
