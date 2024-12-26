# Wordle Solver

## Description
This project is a Python-based Wordle solver that helps users find the best guesses for the popular word puzzle game, Wordle. It includes functionality for both single and dual Wordle games (Dordle) and provides feedback-based word filtering to optimize guesses.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/wordle-solver.git
   cd wordle-solver
   ```

2. **Install Dependencies:**
   Ensure you have Python installed. Then, install the required packages:
   ```bash
   pip install matplotlib
   ```

3. **Prepare Word Lists:**
   Ensure the word lists (`all_valid_words.txt` and `all_wordle_accepted_words.txt`) are in the `words` directory.

## Usage

### Single Wordle Game
Run the `new_york_times_player.py` script to start a single Wordle game:
```bash
python new_york_times_player.py
```
Follow the prompts to input feedback for each guess.

### Dordle Game
Run the `dordle.py` script to start a dual Wordle game:
```bash
python dordle.py
```
Follow the prompts to input feedback for each guess on both Wordle boards.

### Simulate Wordle Games
To simulate multiple Wordle games and generate a histogram of results, run:
```bash
python wordle.py
```
This will create a `wordle_histogram.png` file showing the distribution of attempts.