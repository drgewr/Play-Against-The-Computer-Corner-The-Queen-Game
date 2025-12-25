import random

# Prints the chessboard with:
# Q : Queen's current position
# R : Winning corner (0,0)
# X : Empty squares
def chessboard(rows, cols, queen_r, queen_c):
    for r in reversed(range(rows)):
        line = f"{r}   "
        for c in range(cols):
            if (r, c) == (queen_r, queen_c):
                line += "Q  "
            elif (r, c) == (0, 0):
                line += "R  "  # winning corner
            else:
                line += "X  "
        print(line)
    print("    ", end="")
    for c in range(cols):
        print(f"{c}  ", end="")
    print()

# Checks whether a given position (r,c) is inside the chessboard boundaries
def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

# Checks whether a move is valid according to these game rules:
# Move must stay inside the board
# Must move at least 1 step, at most x steps
# Direction must be Left, Down, or Diagonal Left-Down
def is_valid_move(old_r, old_c, new_r, new_c, rows, cols, x):
    if not in_bounds(new_r, new_c, rows, cols):
        return False
    if (new_r, new_c) == (old_r, old_c):
        return False

    dr = old_r - new_r  
    dc = old_c - new_c 

    if dr < 0 or dc < 0:
        return False

    # Left
    if dr == 0 and dc > 0:
        step = dc
    # Down
    elif dc == 0 and dr > 0:
        step = dr
    # Diagonal left-down
    elif dr == dc and dr > 0:
        step = dr
    else:
        return False

    return 1 <= step <= x

# Generates all possible legal moves for the queen from its current position, considering:
# Board boundaries
# Allowed directions
# Maximum step size x
def possibleMoves(pos_r, pos_c, rows, cols, x):
    moves = []

    # Left moves
    for k in range(1, x + 1):
        nr, nc = pos_r, pos_c - k
        if in_bounds(nr, nc, rows, cols):
            moves.append((nr, nc))
        else:
            break

    # Down moves
    for k in range(1, x + 1):
        nr, nc = pos_r - k, pos_c
        if in_bounds(nr, nc, rows, cols):
            moves.append((nr, nc))
        else:
            break

    # Diagonal left-down moves
    for k in range(1, x + 1):
        nr, nc = pos_r - k, pos_c - k
        if in_bounds(nr, nc, rows, cols):
            moves.append((nr, nc))
        else:
            break

    return moves

# Handles a human player's move by:
# Takes user input
# Validates the move
# Re-prompts until a valid move is entered
def humanMove(queen_r, queen_c, rows, cols, x):
    while True:
        try:
            new_r = int(input("Enter the row: "))
            new_c = int(input("Enter the column: "))
        except ValueError:
            print("Invalid input. Please enter integers.")
            continue

        if is_valid_move(queen_r, queen_c, new_r, new_c, rows, cols, x):
            return (new_r, new_c)
        else:
            print("Invalid move. Allowed: Left, Down, or Diagonal left-down, within 1..x steps.")

# Minimax algorithm:
# value = +1 if MAX wins, -1 if MAX loses
# maximizing indicates whose turn it is
def minimax(queenPos, rows, cols, x, maximizing):
    totalNodes = 1

    if queenPos == (0, 0):
        return (-1 if maximizing else 1), None, 1

    moves = possibleMoves(queenPos[0], queenPos[1], rows, cols, x)
    if not moves:
        return (-1 if maximizing else 1), None, 1

    if maximizing:
        bestVal = -float('inf')
        bestMove = None
        for mv in moves:
            val, _, nodes = minimax(mv, rows, cols, x, False)
            totalNodes += nodes
            if val > bestVal:
                bestVal = val
                bestMove = mv
        return bestVal, bestMove, totalNodes
    else:
        bestVal = float('inf')
        bestMove = None
        for mv in moves:
            val, _, nodes = minimax(mv, rows, cols, x, True)
            totalNodes += nodes
            if val < bestVal:
                bestVal = val
                bestMove = mv
        return bestVal, bestMove, totalNodes

# Alpha-Beta pruning:
# Improves performance on larger boards (such as 7x7)
# Uses alpha and beta bounds to prune branches
def alphabeta(queenPos, rows, cols, x, maximizing, alpha, beta):
    totalNodes = 1

    if queenPos == (0, 0):
        return (-1 if maximizing else 1), None, 1

    moves = possibleMoves(queenPos[0], queenPos[1], rows, cols, x)

    if not moves:
        return (-1 if maximizing else 1), None, 1

    bestMove = None

    if maximizing:
        bestVal = -float('inf')
        for mv in moves:
            val, _, nodes = alphabeta(mv, rows, cols, x, False, alpha, beta)
            totalNodes += nodes
            if val > bestVal:
                bestVal = val
                bestMove = mv
            alpha = max(alpha, bestVal)
            if alpha >= beta:
                break
        return bestVal, bestMove, totalNodes
    else:
        bestVal = float('inf')
        for mv in moves:
            val, _, nodes = alphabeta(mv, rows, cols, x, True, alpha, beta)
            totalNodes += nodes
            if val < bestVal:
                bestVal = val
                bestMove = mv
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal, bestMove, totalNodes

# Allows the AI to choose the initial queen position
# when it starts first, using Minimax / Alpha-Beta
def pick_ai_initial_position(rows, cols, x, use_ab, ai_is_max):
    next_is_max = not ai_is_max

    bestPos = None
    bestVal = -float('inf') if ai_is_max else float('inf')
    totalNodes = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) == (0, 0):
                continue
            if use_ab:
                val, _, nodes = alphabeta((r, c), rows, cols, x, next_is_max, -float('inf'), float('inf'))
            else:
                val, _, nodes = minimax((r, c), rows, cols, x, next_is_max)

            totalNodes += nodes

            if ai_is_max:
                if val > bestVal:
                    bestVal = val
                    bestPos = (r, c)
            else:
                if val < bestVal:
                    bestVal = val
                    bestPos = (r, c)

    return bestPos, totalNodes

# Main game logic:
# Handles Human vs Human and Human vs AI modes
# Controls turn switching
# Tracks AI node counts
def ctq_game(rows, cols, x, mode):
    totalAINodes = 0
    mode1Players = ["Player1", "Player2"]  # Human vs Human mode
    mode2Players = ["You", "AI"]           # AI vs Human mode

    # Decide who starts
    if mode == 1:
        starter = random.choice(mode1Players)
        print(f"{starter} starts first.")
        start_turn = 0 if starter == "Player1" else 1
        max_player_turn_index = start_turn 
    else:
        choice = input("Do you want to start first? (y/n): ").strip().lower()
        if choice == 'y':
            print("You start first.")
            start_turn = 0
        else:
            print("AI starts first.")
            start_turn = 1
        max_player_turn_index = start_turn 

    queenPos = None

    # Initial queen placement
    if mode == 1:
        print(f"{mode1Players[start_turn]} chooses the initial queen position (not (0,0)).")
        while True:
            try:
                qr = int(input("Enter starting row of queen: "))
                qc = int(input("Enter starting column of queen: "))
            except ValueError:
                print("Invalid input. Please enter integers.")
                continue
            if in_bounds(qr, qc, rows, cols) and (qr, qc) != (0, 0):
                queenPos = (qr, qc)
                break
            print("Invalid start. Must be inside board and not (0,0).")
    else:
        if mode2Players[start_turn] == "You":
            print("You choose the initial queen position (not (0,0)).")
            while True:
                try:
                    qr = int(input("Enter starting row of queen: "))
                    qc = int(input("Enter starting column of queen: "))
                except ValueError:
                    print("Invalid input. Please enter integers.")
                    continue
                if in_bounds(qr, qc, rows, cols) and (qr, qc) != (0, 0):
                    queenPos = (qr, qc)
                    break
                print("Invalid start. Must be inside board and not (0,0).")
        else:
            use_ab = (rows >= 7 and cols >= 7)
            ai_is_max = (start_turn == max_player_turn_index) 
            queenPos, nodes = pick_ai_initial_position(rows, cols, x, use_ab, ai_is_max)
            totalAINodes += nodes
            print(f"AI chose initial position: {queenPos[0]} {queenPos[1]}")
            print(f"Nodes explored (initial placement): {nodes}")

    # Game loop: after placement, the other player moves next
    turn = 1 - start_turn

    while queenPos[0] != 0 or queenPos[1] != 0:
        chessboard(rows, cols, queenPos[0], queenPos[1])

        if mode == 1:
            current = mode1Players[turn]
            print(f"{current}'s turn.")
            move = humanMove(queenPos[0], queenPos[1], rows, cols, x)
        else:
            current = mode2Players[turn]
            if current == "You":
                print("Your turn:")
                move = humanMove(queenPos[0], queenPos[1], rows, cols, x)
            else:
                print("AI's turn:")
                use_ab = (rows >= 7 and cols >= 7)
                maximizing = (turn == max_player_turn_index)

                if use_ab:
                    _, move, nodes = alphabeta(queenPos, rows, cols, x, maximizing, -float('inf'), float('inf'))
                else:
                    _, move, nodes = minimax(queenPos, rows, cols, x, maximizing)

                totalAINodes += nodes
                print(f"Nodes explored: {nodes}")
                print(f"AI moved to: {move[0]} {move[1]}")

        queenPos = move
        turn = 1 - turn

    chessboard(rows, cols, queenPos[0], queenPos[1])
    winner_turn = 1 - turn

    if mode == 1:
        print(f"{mode1Players[winner_turn]} wins!")
    else:
        if mode2Players[winner_turn] == "You":
            print("You win!")
        else:
            print("AI wins!")
        print(f"AI visited total of {totalAINodes} nodes.")

def main():
    print("Welcome to Corner the Queen Game!")
    print("***********************************")
    print("Note: All inputs are zero-indexed! Winning corner is (0,0).")
    print("Choose a Mode:")
    print("1) Human vs Human")
    print("2) AI vs Human")

    while True:
        try:
            mode = int(input("Enter choice: "))
            if mode in (1, 2):
                break
        except ValueError:
            pass
        print("Invalid mode. Choose 1 or 2.")

    while True:
        try:
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            x = int(input("Enter max steps per move (x): "))
            if rows > 0 and cols > 0 and x > 0:
                break
        except ValueError:
            pass
        print("Invalid input. rows, cols, x must be positive integers.")

    ctq_game(rows, cols, x, mode)

if __name__ == "__main__":
    main()