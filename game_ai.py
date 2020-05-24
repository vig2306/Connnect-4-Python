import numpy as np
import random
import pygame
import sys
import math
import os

ROWS_TOT = 7
COLS_TOT = 7

BLUE = (29,59,181)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_COIN = 1
AI_COIN = 2

WINDOW_LENGTH = 4

def play_again():
    os.system("python play_again.py")

# Creates board board
def create_board():
    board = np.zeros((ROWS_TOT,COLS_TOT),dtype=int)
    return board

# Checks availability of the vacant place
def check_pos(board,col):
    if(board[ROWS_TOT-1][col]==0):
        return True
    else:
        return False

# Returns the position for the next coin to be placed
def next_row(board,col):
    for row in range(ROWS_TOT):
        if board[row][col] == 0:
            return row

# Places the coin in the required position 
def drop_coin(board,row,col,coin):
    board[row][col] = coin

#print board on console
def show_board(board):
    print(np.flipud(board))

# Checks winning criteria
def check_win(board,coin):
    #Vertical Winning Condition
    for c in range(COLS_TOT):
        for r in range(ROWS_TOT-3):
            if(board[r][c] == coin and board[r+1][c]==coin and board[r+2][c]==coin and board[r+3][c]==coin):
                return True
    #Horizontal Winning Condition
    for r in range(ROWS_TOT):
        for c in range(COLS_TOT-3):
            if(board[r][c] == coin and board[r][c+1]==coin and board[r][c+2]==coin and board[r][c+3]==coin):
                return True
    #Diagonal Winning Condition from Bottom left [board is flipped later]
    for r in range(ROWS_TOT-3):
        for c in range(COLS_TOT-3):
            if(board[r][c] == coin and board[r+1][c+1]==coin and board[r+2][c+2]==coin and board[r+3][c+3]==coin):
                return True
    #Diagonal Winning Condition from Bottom Right [board is flipped later]
    for r in range(3,ROWS_TOT):
        for c in range(COLS_TOT-3):
            if(board[r][c] == coin and board[r-1][c+1]==coin and board[r-2][c+2]==coin and board[r-3][c+3]==coin):          
                return True

def evaluate_window(window, coin):
	score = 0
	opp_coin = PLAYER_COIN
	if coin == PLAYER_COIN:
		opp_coin = AI_COIN

	if window.count(coin) == 4:
		score += 100
	elif window.count(coin) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(coin) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_coin) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, coin):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLS_TOT//2])]
	center_count = center_array.count(coin)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROWS_TOT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLS_TOT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, coin)

	## Score Vertical
	for c in range(COLS_TOT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS_TOT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, coin)

	## Score posiive sloped diagonal
	for r in range(ROWS_TOT-3):
		for c in range(COLS_TOT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, coin)

	for r in range(ROWS_TOT-3):
		for c in range(COLS_TOT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, coin)

	return score

def is_terminal_node(board):
	return check_win(board, PLAYER_COIN) or check_win(board, AI_COIN) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if check_win(board, AI_COIN):
				return (None, 100000000000000)
			elif check_win(board, PLAYER_COIN):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_COIN))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = next_row(board, col)
			b_copy = board.copy()
			drop_coin(b_copy, row, col, AI_COIN)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = next_row(board, col)
			b_copy = board.copy()
			drop_coin(b_copy, row, col, PLAYER_COIN)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLS_TOT):
		if check_pos(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, coin):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = next_row(board, col)
		temp_board = board.copy()
		drop_coin(temp_board, row, col, coin)
		score = score_position(temp_board, coin)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

# Game board style
def game_board(board):
    for c in range(COLS_TOT):
        for r in range(ROWS_TOT):
            pygame.draw.rect(screen, BLUE , (c*Board_size, r*Board_size+Board_size, Board_size, Board_size))
            pygame.draw.circle(screen, BLACK , (int(c*Board_size+Board_size/2), int(r*Board_size+Board_size+Board_size/2)), Radius)
    for c in range(COLS_TOT):
        for r in range(ROWS_TOT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*Board_size+Board_size/2), height-int(r*Board_size+Board_size/2)), Radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*Board_size+Board_size/2), height-int(r*Board_size+Board_size/2)), Radius)
    pygame.display.update()


board = create_board()
show_board(board)
running = True
#turn = 0 
pygame.init()

Board_size =100
width = COLS_TOT * Board_size
height = ROWS_TOT * Board_size
size = (width,height)
Radius = int(Board_size/2 - 5)
font = pygame.font.SysFont("Times New Roman" , 80)
names= pygame.font.SysFont("Times New Roman" , 30)
screen = pygame.display.set_mode(size)
game_board(board)
pygame.display.update()

turn = random.randint(PLAYER, AI)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width, Board_size))
            player1= names.render("Player", 1, RED)
            screen.blit(player1,(20,10))
            player2= names.render("AI", 1, YELLOW)
            screen.blit(player2,(580,10))

            position_x = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (position_x, int(Board_size/2)), Radius)
            else:
                pygame.draw.circle(screen, YELLOW, (position_x, int(Board_size/2)), Radius)
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width, Board_size))
            player1= names.render("Player", 1, RED)
            screen.blit(player1,(20,10))
            player2= names.render("AI", 1, YELLOW)
            screen.blit(player2,(580,10))
			#print(event.pos)
			#Player 1 PLays
            if turn ==PLAYER:
                position_x = event.pos[0]
                col = int(math.floor(position_x/Board_size))
                if check_pos(board,col):
                    row = next_row(board,col)
                    drop_coin(board,row,col,PLAYER_COIN)

                    if check_win(board,PLAYER_COIN):
                        label=font.render("Player wins",1,RED)
                        screen.blit(label, (140,10))
                        running=False
                    turn += 1
                    turn = turn % 2
                    show_board(board)
                    game_board(board)

	# AI plays PLayer 2
    if turn == AI and running:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        
        if check_pos(board,col):
			#pygame.time.wait(500)
            row = next_row(board,col)
            drop_coin(board,row,col,AI_COIN)

            if check_win(board,AI_COIN):
                label=font.render("AI Wins",1,YELLOW)
                screen.blit(label,(140,10))
                running=False
            
            show_board(board)
            game_board(board)

            turn+=1
            turn=turn%2
    if running==False:
        pygame.time.wait(1500)
        pygame.quit()
        play_again()
