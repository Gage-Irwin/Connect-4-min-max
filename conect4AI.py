import numpy as np
import random
import math
import time

board_rows = 6
board_coulmns = 7

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def valid_move(board, column):
    return board[board_rows-1][column] == 0

def get_next_row(board, column):
    for r in range(board_rows):
        if board[r][column] == 0:
            return r

def print_board(board):
    print(np.flip(board,0))

def connect_4_check(board, piece):
    for c in range(board_coulmns-3):
        for r in range(board_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(board_coulmns):
        for r in range(board_rows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(board_coulmns-3):
        for r in range(board_rows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(board_coulmns-3):
        for r in range(3, board_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True  

def evaluate_board_state(board_state, piece):
    score = 0
    opp_piece = 1
    if piece == 1:
        opp_piece = 2           
    if board_state.count(piece) == 3 and board_state.count(0) == 1:
        score += 5
    elif board_state.count(piece) == 2 and board_state.count(0) == 2:
        score += 2
    if board_state.count(opp_piece) == 3 and board_state.count(0) == 1:
        score += -4
    elif board_state.count(opp_piece) == 2 and board_state.count(0) == 2:
        score += -1          
    return score       

def evaluate_score(board, piece):
    score = 0
    # center
    center_array = [int(i) for i in list(board[:, board_coulmns//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # horizontal
    for r in range(board_rows):
        row_array = [int(i) for i in list(board[r,:])]  
        for c in range(board_coulmns-3):
            board_state = row_array[c:c+4]
            score += evaluate_board_state(board_state, piece)
    # vertical
    for r in range(board_coulmns):
        col_array = [int(i) for i in list(board[:,c])]  
        for r in range(board_rows-3):
            board_state = col_array[r:r+4]
            score += evaluate_board_state(board_state, piece)
    # diagonals
    for r in range(board_rows-3):
        for c in range(board_coulmns-3):
            board_state = [board[r+i][c+i] for i in range(4)]            
            score += evaluate_board_state(board_state, piece)
    for r in range(board_rows-3):
        for c in range(board_coulmns-3):
            board_state = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_board_state(board_state, piece)

    return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = []
    for c in range(board_coulmns):
        if valid_move(board, c):
            valid_locations.append(c)    
    if depth == 0 or connect_4_check(board, 1) or connect_4_check(board, 2) or len(valid_locations) == 0:
        if connect_4_check(board, 1) or connect_4_check(board, 2) or len(valid_locations) == 0:
            if connect_4_check(board, 2):
                return (None, math.inf)
            elif connect_4_check(board, 1):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, evaluate_score(board, 2))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_row(board, col)
            temp_copy = board.copy()
            drop_piece(temp_copy, row, col, 2)
            new_score = minimax(temp_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break                
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_row(board, col)
            temp_copy = board.copy()
            drop_piece(temp_copy, row, col, 1)
            new_score = minimax(temp_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break                
        return column, value       



input_select = input("Player vs AI: 1\nAI vs AI: 2\n>")
board = np.zeros((board_rows, board_coulmns))
game_over = False
turn = random.randint(0, 1)
print_board(board)
if input_select == '1':
    while not game_over:
        valid_input = False
        if turn == 0:
            t0 = time.time()
            # Player logic
            while not valid_input:
                selection = input("Player 1 select where to drop your piece:")
                if selection != '0' and selection != '1' and selection != '2' and selection != '3' and selection != '4' and selection != '5' and selection != '6':
                    print(selection + " Is not a valid input!")
                else:
                    column = int(selection)
                    if valid_move(board, column):
                        print("You Played " + selection)
                        valid_input = True
                        row = get_next_row(board, column)
                        drop_piece(board, row, column, 1)
                        if connect_4_check(board, 1):
                            print("Player 1 Wins!")
                            game_over = True                
                    else:
                        print(selection + " Is not a valid input!")
            t1 = time.time()
            print(t1-t0)                     
        else:
            t0 = time.time()
            # AI logic
            while not valid_input:
                    # column = random.randint(0, board_coulmns-1)
                    column, minimax_score = minimax(board, 6,-math.inf, math.inf, True)
                    selection = str(column)
                    print("AI played " + selection)
                    if valid_move(board, column):
                        print(selection)
                        valid_input = True
                        row = get_next_row(board, column)
                        drop_piece(board, row, column, 2)
                        if connect_4_check(board, 2):
                            print("AI Wins!")
                            game_over = True                
                    else:
                        print(selection + " Is not a valid input!")
            t1 = time.time()
            print(t1-t0)                    

        print_board(board)
        turn += 1
        turn = turn % 2
elif input_select == '2':            
    t0 = time.time()
    while not game_over:
        valid_input = False
        if turn == 0:
            # Player logic
            while not valid_input:
                # column = random.randint(0, board_coulmns-1)
                column, minimax_score = minimax(board, 7,-math.inf, math.inf, True)
                selection = str(column)
                print("AI 1 played " + selection)
                if valid_move(board, column):
                    print(selection)
                    valid_input = True
                    row = get_next_row(board, column)
                    drop_piece(board, row, column, 1)
                    if connect_4_check(board, 1):
                        print("AI 1 Wins!")
                        game_over = True                
                else:
                    print(selection + " Is not a valid input!")
        else:
            # AI logic
            while not valid_input:
                    # column = random.randint(0, board_coulmns-1)
                    column, minimax_score = minimax(board, 7,-math.inf, math.inf, True)
                    selection = str(column)
                    print("AI 2 played " + selection)
                    if valid_move(board, column):
                        print(selection)
                        valid_input = True
                        row = get_next_row(board, column)
                        drop_piece(board, row, column, 2)
                        if connect_4_check(board, 2):
                            print("AI 2 Wins!")
                            game_over = True                
                    else:
                        print(selection + " Is not a valid input!")


        print_board(board)
        turn += 1
        turn = turn % 2 
    t1 = time.time()
    print(t1-t0)
else:
    print("bad input")     