import numpy as np
import random as rand
import mybot

# Function for the game logic
def game(board):
    turn = 1
    game_over = False
    first_place = 0
    max_depth = 3
    last_move = None

    while not game_over:
        print(f"\n{players[turn]} Turn")

        if turn == 2:
            board = bot2.play(board, max_depth)
            last_move = bot2.last_move
        elif turn == 3:
            board = bot3.play(board, max_depth)
            last_move = bot3.last_move
            max_depth += 2
        else:
            selected = input("Select a tile (row and column, e.g., '11'): ")
            try:
                row = int(selected[0])
                col = int(selected[1])
                if row not in range(4) or col not in range(4):
                    raise ValueError("Invalid tile selected.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column as two digits between 0 and 3.")
                continue

            if board[row][col] != 0:
                print("Tile already occupied")
                continue
            board[row][col] = turn
            last_move = (row, col)

        # Check for game over
        if (check_win(board, turn) and first_place == 0):
            print(f"\n{players[turn]} won 1st place!")
            first_place = turn
        elif (check_tie(board) and first_place == 0):
            print("\nIt's a tie!")
            game_over = True
        elif (check_win(board, turn) and first_place != 0):
            print(f"\n{players[turn]} won 2nd place!")
            print(f"\n{players[turn % 3 + 1]} won 3rd place!")
            game_over = True
        elif (check_tie(board) and first_place != 0):
            print(f"\n{players[turn]} and {players[turn % 3 + 1]} tied for 2nd place!")
            game_over = True

        print_board(board, last_move)

        if game_over:
            print("\nGame over.")
            break

        turn = turn % 3 + 1  # Cycle between 1, 2, and 3
        if turn == first_place:
            turn = turn % 3 + 1

def check_win(board, player):
    size = len(board)
    
    # Check horizontal and vertical lines
    for i in range(size):
        for j in range(size - 2):
            if all(board[i][j+k] == player for k in range(3)):  # Horizontal
                return True
            if all(board[j+k][i] == player for k in range(3)):  # Vertical
                return True

    # Check main diagonals
    for i in range(size - 2):
        for j in range(size - 2):
            if all(board[i+k][j+k] == player for k in range(3)):  # Main diagonal
                return True

    # Check anti-diagonals
    for i in range(size - 2):
        for j in range(2, size):
            if all(board[i+k][j-k] == player for k in range(3)):  # Anti-diagonal
                return True

    return False

def check_tie(board):
    return not np.any(board == 0)

def print_board(board, last_move):
    printable_board = [[" " for _ in range(4)] for _ in range(4)]

    for row in range(len(board)):
        for col in range(len(board[row])):
            tile = board[row][col]
            if tile != 0:
                if last_move == (row, col):
                    printable_board[row][col] = f"\033[91m{players[tile]}\033[0m"  # Red color for the last move
                else:
                    printable_board[row][col] = players[tile]

    for row in printable_board:
        print("| " + " | ".join(row) + " |")
        print("-" * 16)

board = np.zeros((4,4))
players = {0: " ", 1: "o", 2: "x", 3: "□"}

bot2 = mybot.MyBot(2)
bot3 = mybot.MyBot(3)

game(board)
