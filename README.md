# 3-Players-Tic-Tac-Toe
Implementation of a variation of tic-tac-toe which uses a 4x4 board and is played by 3 players.

GAME SETUP
1. Board: The game is played on a 4x4 grid.
2. Players: There are three players, represented as follows:
      Player 1: "o"
      Player 2: "x"
      Player 3: "□"
3. Bots: The game has a built-in bot class which can be instantiated to substitute a human player

GAME OBJECTIVE
The objective of the game is to achieve a specific pattern on the board, which constitutes a win. The winning patterns involve having three of the player's symbols in a row, column, or diagonal.

GAMEPLAY MECHANICS
1. Turns: Players take turns in a cyclical order (Player 1, Player 2, Player 3).
2. Player Actions:
        Bots: They automatically select a tile based on their logic.
        Human Player (Player 3): Selects a tile by providing input in the form of a two-digit string, where the first digit is the row and the second digit is the column (e.g.,            "11" for row 1, column 1).

BOT LOGIC
Move Selection:

Bots evaluate all available moves (empty tiles) and prioritize them based on certain criteria:
-    Winning Moves: Moves that result in a win for the bot.
-    Blocking Moves: Moves that prevent the opponent from winning in their next turn.
-    Two-in-a-Row Moves: Moves that create a two-in-a-row situation for the bot.
-    Adjacent Moves: Moves adjacent to the bot's existing tiles.
-    Free Moves: Any other available moves.
Moves are further prioritized by placing those in the center tiles (within rows and columns 1 to 2) higher in the order.

Move Execution:

Bots then use the minimax algorithm to search the game tree and stop either when the game is over, or the max depth of search has been reached, whereas they call an evaluation function to evaluate the board and return the score.

Board Evaluation:

The evaluation function combines positional and strategic evaluations:
    Positional Evaluation: It assigns higher scores to central positions, moderate scores to edge positions, and lower scores to corner positions. This incentivizes occupying          central and strategic positions on the board.
    Strategic Evaluation: It rewards or penalizes board states where the bot or opponents have potential winning configurations or blocks. This helps the bot prioritize moves that     either advance its winning chances or hinder the opponents' strategies.

WIN AND TIE CONDITIONS
Win Condition:
    A player wins if they place three of their symbols in a row, column, or diagonal.
Tie Condition:
    The game ends in a tie if all tiles are filled without any player achieving a winning pattern.

GAME FLOW
    The game starts with an empty board and Player 1 taking the first turn.
    Players take turns in the order (Player 1, Player 2, Player 3).
    After each move, the board is checked for win or tie conditions.
    The game continues until a player wins or the game ends in a tie.
    If a player wins, the game announces the first-place winner. The game continues to determine second and third places or tie scenarios for these positions.
