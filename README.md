# Play Against The Computer: Corner The Queen Game

## Project Overview

This project implements the Corner The Queen game, a two-player, turn-based board game played on an m × n chessboard.  
Players take turns moving a single queen with the goal of being the **first to reach the lower-left corner of the board.

## Board Representation

- Q → Queen’s current position  
- R → Winning corner (0, 0)
- X → Empty square  

In addition, rows are printed in reverse order to visually resemble a chessboard.

<img width="285" height="196" alt="Ekran Resmi 2025-12-25 19 28 45" src="https://github.com/user-attachments/assets/ca300267-7103-4d5e-bb40-31e598f67b14" />

The project supports both **Human vs Human** and **Human vs AI** gameplay, where the AI uses **Minimax** and **Alpha–Beta Pruning** to make optimal decisions.

## Game Rules
- The game is played on an m × n chessboard.
- There is one queen on the board.
- The winning square is the lower-left corner (0, 0), marked as R on the board.
- Players take turns moving the queen.
- The queen can move only:
  - Left
  - Down
  - Diagonally Left-Down
- Each move must:
  - Be at least 1 step
  - Be at most x steps
  - Stay within the board boundaries
- The queen **cannot** be initially placed in the winning corner (0, 0).
- The game ends immediately when the queen reaches (0, 0).

## Game Modes

### 1. Human vs Human
- Two human players play against each other.
- The starting player is selected randomly.
- The starting player chooses the initial position of the queen.

### 2. Human vs AI
- The human player chooses whether to start first or second.
- If the human starts, the human chooses the initial queen position.
- If the AI starts, the AI chooses the initial queen position using Minimax / Alpha-Beta search.

To enable AI to discover the squares, I used both Minimax and Alpha–Beta Pruning Algorithms where appropriate. Their logic as follows:

### Minimax Algorithm
  - Used for smaller board sizes.
  - Explores the game tree until a terminal state.
  - Terminal states are evaluated as:
    - +1 → MAX player wins
    - -1 → MIN player wins

### Alpha–Beta Pruning Algorithm
  - Automatically used for larger boards (e.g., 7×7 and above).
  - Reduces the number of explored nodes by pruning unpromising branches.
  - Produces the same optimal result as Minimax but more efficiently.

Node Count Measurement:
- The program counts the number of nodes explored during AI decision-making.
- At the end of the game, the total number of AI-explored nodes is printed.
- This helps demonstrate the computational cost of Minimax and the effectiveness of Alpha–Beta pruning.

## Input Format
- All inputs are zero-indexed.
- Positions are entered as (row, column)
- Invalid moves (illegal direction, out of bounds, exceeding x steps) are rejected and re-prompted.


## How to Run

1. Clone the repository:
 ```
 git clone <repository-url>
 cd corner-the-queen
 ```
2.	Run the program:
 ```python main.py```

## Notes
- Minimax Algorithm explores the entire game tree and can become expensive for large boards, instead AI uses Alpha–Beta Pruning Algorithm.
- Alpha–Beta Pruning Algorithm significantly reduces computation but node counts may still be high.

## References
- Corner The Queen – Game Explanation - https://www.youtube.com/watch?v=AYOB-6wyK_I
- Corner The Queen (UC Davis) - https://web.cs.ucdavis.edu/~okreylos/TAship/Fall1999/CornerTheQueen.html
- Wythoff’s Game (Mathematical Background) - https://math.rice.edu/~michael/teaching/2012Fall/Wythoff.pdf
- Game Theory & Strategy Video - https://www.youtube.com/watch?v=MratE0dzrHc


