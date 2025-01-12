# Wordle Project

This project contains a playable Wordle game implementation and a versatile Wordle solver that can handle multiple simultaneous puzzles.

## Part 1: Wordle Game

### Prerequisites
- Python 3.x
- Pygame (for GUI version)

### Installation
1. Install required packages:
```bash
pip install pygame
```

### How to Play

#### GUI Version (wordle_game.py)
Run the graphical version with:
```bash
python wordle_game.py
```

Features:
- Interactive graphical interface
- Color-coded feedback (green, yellow, gray)
- On-screen keyboard
- Win/lose screens with confetti celebration
- Option to continue or quit after each game

Controls:
- Type letters to make your guess
- ENTER: Submit guess
- BACKSPACE: Delete letter
- SPACE/ENTER: Skip celebration animation
- Mouse: Click buttons in popup menus

## Part 2: Wordle Solver

### Description
A versatile Python-based Wordle solver that can handle multiple simultaneous Wordle puzzles. Whether you're playing regular Wordle, Dordle (2 words), Quordle (4 words), or any other variant, this solver can help you find optimal guesses.

### Usage

Run the solver with:
```bash
python wordle_solver.py
```

Features:
- Solve any number of simultaneous Wordle puzzles
- Works with variants like:
  - Wordle (1 word)
  - Dordle (2 words)
  - Quordle (4 words)
  - And any other multiple-word variants
- Provides optimal guessing strategies
- Feedback-based word filtering

How to Use:
1. Run the script
2. Enter the number of words you want to solve
3. Input feedback for each guess using:
   - 'g' for green (correct letter, correct position)
   - 'y' for yellow (correct letter, wrong position)
   - 'b' for black/gray (letter not in word)
4. Receive suggested guesses for solving all puzzles simultaneously

## Files
- `wordle_game.py`: GUI implementation of the Wordle game
- `wordle_solver.py`: Multi-puzzle Wordle solver
- `wordle.py`: Core Wordle logic and functionality