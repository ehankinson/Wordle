# Project Title: Wordle Solver

## Description
The Wordle Solver project is a Python-based application designed to play and solve the popular word-guessing game, Wordle. The solver uses a probabilistic approach to determine the best possible guess based on letter frequency and positional probabilities. It can simulate solving the Wordle puzzle or assist users in finding the optimal guesses based on feedback from actual gameplay.

## Installation Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wordle-solver.git
   cd wordle-solver
   ```

2. **Ensure Python 3.x is installed** on your system.

3. **Dependencies**: The following modules are used but are part of the standard Python library:
   - `os`
   - `time`
   - `random`
   - `concurrent.futures` (part of the `concurrent` library)

   So no external packages are required.

4. **Word List Files**:
   - The project relies on the text files `all_wordle_accepted_words.txt` and `all_valid_words.txt` to function correctly.
   - Ensure these files are in the same directory as the script.

## Usage

### Simulate Solving Wordle
To run simulations to calculate the solving percentage:

1. Run the script directly in your terminal:
   ```bash
   python wordle_solver.py
   ```
2. Adjust `total_runs` to the number of simulations you'd like to perform for better statistical results.

### Interactive Solver for New York Times Wordle
To use the interactive tool to solve the Wordle from The New York Times:

1. Uncomment the following lines in the `if __name__ == "__main__":` block:
   ```python
   wordle = Wordle(word_type)
   wordle.ny_times_word_finder()
   ```
2. Follow the on-screen instructions to get the best word recommendations and input feedback.

### Example Usage in Another Script
You can integrate the `Wordle` class into your own projects or scripts:

```python
from wordle import Wordle

wordle_solver = Wordle("easy")
wordle_solver.ny_times_word_finder()
```

## Contributing

If you would like to contribute to this project:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Open a Pull Request.