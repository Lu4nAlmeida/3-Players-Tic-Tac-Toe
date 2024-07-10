import numpy as np
import random as rand

# Class used to create your own bot logic
# It comes with in-bult methods to speed up the process of making a bot from scratch
class Bot:
    def __init__(self, turn):
        self.turn = turn
        self.last_move = None

    def __repr__(self):
        return f"Bot {self.turn}, player {players[self.turn]}"

    def get_next_player(self, current_player):
        return (current_player % 3) + 1

    # Returns a list with 8 elements each representing a tile around the tile being looked
    # returns -1 as an element if the tile is out of bounds
    def get_adjacent_tiles(self, board, tile):
        adjacent_tiles = []
        row, col = tile
        size = len(board)
        directions = [
            (0, 1), (0, -1),  # horizontal
            (1, 0), (-1, 0),  # vertical
            (1, 1), (-1, -1),  # main diagonal
            (-1, 1), (1, -1)  # anti-diagonal
        ]

        for d in directions:
            new_row = row + d[0]
            new_col = col + d[1]
            empty_tiles = 0
            if 0 <= new_row < size and 0 <= new_col < size:
                adjacent_tiles.append(board[new_row][new_col])
            else:
                adjacent_tiles.append(-1)
        return adjacent_tiles

    # Returns a list with all the possible moves in a given position
    # Moves are in order from top left corner to bottom right, use argument shuffle=True to shuffle them
    def get_moves(self, board, shuffle=False):
        free_tiles = np.where(board == 0)
        if free_tiles[0].size == 0:
            return []  # No available moves
        available_moves = list(zip(free_tiles[0], free_tiles[1]))
        if shuffle:
            rand.shuffle(available_moves)
        return available_moves
    
    def check_win(self, board, player):
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

    def check_tie(self, board):
        return not np.any(board == 0)
    
    def evaluate_board(self, board, current_player):
        eval = 0
        # Costumize your own board evaluation function...
        return eval

    # Updates the board after given a move to play, returns board
    def play(self, board, move):
        row, col = move
        board[row][col] = self.turn
        self.last_move = (row, col)
        return board
