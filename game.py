import numpy as np
import pygame
import sys
import math

ROWS_TOT = 7
COLS_TOT = 7

Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)

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

# Prints the board
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

# Switches the player chance
def switch_player(player):
    if player==1:
        return 2
    else:
        return 1

# Game board style
def game_board(board):
    for c in range(COLS_TOT):
        for r in range(ROWS_TOT):
            pygame.draw.rect(screen, Blue , (c*Board_size, r*Board_size+Board_size, Board_size, Board_size))
            pygame.draw.circle(screen, Black , (int(c*Board_size+Board_size/2), int(r*Board_size+Board_size+Board_size/2)), Radius)
    for c in range(COLS_TOT):
        for r in range(ROWS_TOT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, Red, (int(c*Board_size+Board_size/2), height-int(r*Board_size+Board_size/2)), Radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, Yellow, (int(c*Board_size+Board_size/2), height-int(r*Board_size+Board_size/2)), Radius)
    pygame.display.update()

board = create_board()
show_board(board)
running = True
#turn = 0 
player = 1

pygame.init()

Board_size =100
width = COLS_TOT * Board_size
height = ROWS_TOT * Board_size
size = (width,height)

Radius = int(Board_size/2 - 5)
font = pygame.font.SysFont("Times New Roman" , 80)
screen = pygame.display.set_mode(size)
game_board(board)
pygame.display.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION: 
            pygame.draw.rect(screen,Black,(0,0,width, Board_size))
            position_x = event.pos[0]
            if player == 1:
                pygame.draw.circle(screen, Red, (position_x, int(Board_size/2)), Radius)
            else:
                pygame.draw.circle(screen, Yellow, (position_x, int(Board_size/2)), Radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: 
            pygame.draw.rect(screen,Black,(0,0,width, Board_size))
            position_x = event.pos[0]
            col = int(math.floor(position_x/100))
            if check_pos(board,col):
                row = next_row(board,col)
                drop_coin(board,row,col,player)
            if check_win(board,player):
                if player == 1:
                    winner = font.render("Player 1 wins", 1 , Red)
                    screen.blit(winner,(140,10))
                elif player == 2:
                    winner = font.render("Player 2 wins", 1 , Yellow)
                    screen.blit(winner,(140,10))
                running = False
            show_board(board)
            game_board(board)
            if not running:
                pygame.time.wait(4000)
            player = switch_player(player)

        