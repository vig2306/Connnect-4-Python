import numpy as np
import pygame

ROWS_TOT = 6
COLS_TOT = 7

def create_board():
    board = np.zeros((ROWS_TOT,COLS_TOT),dtype=int)
    return board
    
def check_pos(board,col):
    if(board[ROWS_TOT-1][col]==0):
        return True
    else:
        return False

def next_row(board,col):
    for row in range(ROWS_TOT):
        if board[row][col] == 0:
            return row
def drop_coin(board,row,col,coin):
    board[row][col] = coin

def show_board(board):
    print(np.flipud(board))

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

def switch_player(player):
    if player==1:
        return 2
    else:
        return 1

board = create_board()
show_board(board)
running = True
#turn = 0 
player = 1

pygame.init()
SQUARESIZE =100
width = COLS_TOT * SQUARESIZE
height = ROWS_TOT * SQUARESIZE
size = (width,height)
screen = pygame.display.set_mode(size)

while running:
    col = int(input("Enter column no to drop: "))
    #Player 1 input
    # if turn==0: 
    #     col = int(input("Enter column no to drop P1: "))
    #     coin = 1
    #Player 2 input
    # else:
    #     col = int(input("Enter column no to drop P2: "))
    #     coin = 2
    if check_pos(board,col):
        row = next_row(board,col)
        drop_coin(board,row,col,player)
    show_board(board)
    if check_win(board,player):
        print(player,"wins")
        running = False
    # turn+=1
    # turn = turn%2
    player = switch_player(player)
print("Game Over")