import numpy as np
import random as rand
import bot

class MyBot(bot.Bot):
    def __init__(self, turn):
        super().__init__(turn)
    
    def minimax(self, board, depth, current_player, alpha, beta, max_depth):
        if self.check_win(board, self.turn):
            return 100 - depth
        elif self.check_win(board, self.get_next_player(self.turn)):
            return depth - 100
        elif self.check_win(board, self.get_next_player(self.get_next_player(self.turn))):
            return depth - 100
        elif self.check_tie(board):
            return 0
        elif depth == max_depth:
            return self.evaluate_board(board, current_player)

        if current_player == self.turn:
            max_eval = float('-inf')
            for move in self.order_moves(board, self.get_moves(board)):
                row, col = move
                board[row][col] = self.turn
                eval = self.minimax(board, depth + 1, self.get_next_player(self.turn), alpha, beta, max_depth)
                board[row][col] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.order_moves(board, self.get_moves(board)):
                row, col = move
                board[row][col] = current_player
                eval = self.minimax(board, depth + 1, self.get_next_player(current_player), alpha, beta, max_depth)
                board[row][col] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
  
    def block_player(self, board, tile):
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
                if board[new_row][new_col] != 0 and board[new_row][new_col] != self.turn:
                    player_adjacent = board[new_row][new_col]
                    board[row][col] = player_adjacent
                    if self.check_win(board, player_adjacent):
                        return True
                    board[row][col] = 0
        return False

    def two_in_a_row(self, board, tile):
        tiles = self.get_adjacent_tiles(board, tile)

        for t in tiles:
            if t == self.turn:
                return True
        return False

    def player_adjacent(self, board, tile):
        tiles = self.get_adjacent_tiles(board, tile)

        for t in tiles:
            if t != 0 and t != self.turn and t != -1:
                return True
        return False

    def order_moves(self, board, moves):
        ordered_moves = []

        winer_moves = []
        block_player_moves = []
        two_in_a_row_moves = []
        player_adjacent_moves = []
        free_moves = []

        rand.shuffle(moves)

        for move in moves:
            row, col = move
            board[row][col] = self.turn

            if self.check_win(board, self.turn):
                winer_moves.append(move)
            elif self.block_player(board, move):
                block_player_moves.append(move)
            elif self.two_in_a_row(board, move):
                two_in_a_row_moves.append(move)
            elif self.player_adjacent(board, move):
                player_adjacent_moves.append(move)
            else:
                free_moves.append(move)

            board[row][col] = 0

        winer_moves = self.center_moves(winer_moves)
        block_player_moves = self.center_moves(block_player_moves)
        two_in_a_row_moves = self.center_moves(two_in_a_row_moves)
        player_adjacent_moves = self.center_moves(player_adjacent_moves)
        free_moves = self.center_moves(free_moves)

        ordered_moves = winer_moves + block_player_moves + two_in_a_row_moves + player_adjacent_moves + free_moves

        return ordered_moves

    def center_moves(self, moves):
        center_moves = []
        other_moves = []
        for move in moves:
            row, col = move
            if (row > 0 and col > 0) and (row < 3 and col < 3):
                center_moves.append(move)
            else:
                other_moves.append(move)

        return center_moves + other_moves

    def evaluate_board(self, board, current_player):
        score = 0
        current_player -= 1
        next_player = self.get_next_player(self.turn)
        next_next_player = self.get_next_player(next_player)

        # 3 points for each center tile, 2 points for each edge tile, 1 point for each corner tile
        for row in range(4):
            for col in range(4):
                tile = board[row][col]

                if tile == self.turn:
                    if 0 < row < 3 and 0 < col < 3:  # Center tiles
                        score += 3
                    elif (row in {0, 3} and 0 < col < 3) or (col in {0, 3} and 0 < row < 3):  # Edge tiles
                        score += 2
                    elif (row, col) in {(0, 0), (0, 3), (3, 0), (3, 3)}:  # Corner tiles
                        score += 1
                elif tile == next_player or tile == next_next_player:
                    if 0 < row < 3 and 0 < col < 3:  # Center tiles
                        score -= 3
                    elif (row in {0, 3} and 0 < col < 3) or (col in {0, 3} and 0 < row < 3):  # Edge tiles
                        score -= 2
                    elif (row, col) in {(0, 0), (0, 3), (3, 0), (3, 3)}:  # Corner tiles
                        score -= 1

        for row in range(4):
            for col in range(4):
                tile = (row, col)

                if tile == self.turn:
                    if self.two_in_a_row(board, tile) and self.block_player(board, tile):
                        score += 5
                    elif self.block_player(board, tile):
                        score += 3
                    elif self.two_in_a_row(board, tile):
                        score += 2
                elif tile == next_player or tile == next_next_player:
                    if self.two_in_a_row(board, tile) and self.block_player(board, tile):
                        score -= 5
                    elif self.block_player(board, tile):
                        score -= 3
                    elif self.two_in_a_row(board, tile):
                        score -= 2

        return score

    def best_move(self, board, max_depth=3):
        best_value = float('-inf')
        best_move = None
        for move in self.order_moves(board, self.get_moves(board)):
            row, col = move
            board[row][col] = self.turn
            move_value = self.minimax(board, 0, self.get_next_player(self.turn), float('-inf'), float('inf'), max_depth)
            board[row][col] = 0
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move

    def play(self, board, max_depth):
        move = self.best_move(board, max_depth)
        row, col = move
        board[row][col] = self.turn
        self.last_move = (row, col)
        return board
