import os
import copy
import time
import random
import matplotlib.pyplot as plt
import math
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor

class Wordle():
    
    def __init__(self) -> None:
        self.words = self.get_words()
        self.probabilities = self.make_probabilities()
        self.letters = self._get_letters()
        self.final_guess = ['', '', '', '', '']
        self.in_word = set()
        self.word_score_cache = {}

    

    def reset(self, word_type: str):
        self.words = self.get_words(word_type)
        self.probabilities = self.make_probabilities()
        self.letters = self._get_letters()
        self.final_guess = ['', '', '', '', '']
        self.in_word = set()



    def _get_letters(self) -> dict:
        return {
            'a': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'b': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'c': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'd': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'e': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'f': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'g': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'h': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'i': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'j': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'k': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'l': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'm': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'n': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'o': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'p': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'q': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'r': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            's': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            't': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'u': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'v': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'w': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'x': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'y': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()},
            'z': {'in_word': None, 'double': True, 'triple': True, 'position': set(), 'not_position': set()}
        }
    


    def get_words(self) -> list[str]:
        words = []
        # with open("words/all_valid_words.txt", "r") as f:
        with open("words/all_wordle_accepted_words.txt", "r") as f:
            for word in f:
                words.append(word.strip())
        
        return words



    def valid_word_prob(self) -> list[list[str, float]]:
        """Get sorted list of words with their scores"""
        word_scores = []
        for word in self.words:
            score = self.calculate_word_score(word)
            word_scores.append([word, score])
        
        return sorted(word_scores, key=lambda x: x[1], reverse=True)



    def get_random_word(self):
        return random.choice(self.words)
    


    def compare(self, f_letters: dict, guess: str) -> list[str]:
        letters = []
        g_letters = {}
        for i, char in enumerate(guess):
            if char not in g_letters:
                g_letters[char] = [i]
            else:
                g_letters[char].append(i)
            
            if char in f_letters:
                self.letters[char]['in_word'] = True
                if i in f_letters[char]:
                    self.letters[char]['position'].add(i)
                    self.final_guess[i] = char
                    self.in_word.add(char)
                    letters.append('g')
                else:
                    self.letters[char]['not_position'].add(i)
                    self.in_word.add(char)
                    letters.append('y')
            else:
                self.letters[char]['in_word'] = False
                letters.append('b')
        
        for char in g_letters:
            if char in f_letters:
                length = len(g_letters[char])
                f_length = len(f_letters[char])
                if length == 2:
                    if length > f_length: # the final word only has 1 of these letters
                        self.letters[char]['triple'] = False
                        self.letters[char]['double'] = False
                elif length == 3:
                    if length > f_length: # we can't have triple in the word
                        self.letters[char]['triple'] = False
                    else: # if the final word has 3 and the choosen word also has 3 doulbe can't happen
                        self.letters[char]['double'] = False
                        
                # we dont need to check 3 f_length since 2 will do all the proper checks
                    
        return letters



    def final_guess_letters(self, final_word: str) -> dict[str]:
        f_letters = {}
        for i, char in enumerate(final_word):
            if char not in f_letters:
                f_letters[char] = [i]
            else:
                f_letters[char].append(i)
        
        return f_letters



    def filter_words(self) -> None:
        new_words = []
        for word in self.words:

            chars = {}
            skip = False
            for i, char in enumerate(word):
                
                if char not in chars:
                    chars[char] = 1
                else:
                    chars[char] += 1

                if self.final_guess[i] == '':

                    if self.letters[char]['in_word'] is False:
                        skip = True
                        break
                        
                    elif self.letters[char]['in_word'] is True:
                        pos = self.letters[char]['position']
                        if len(pos) == 0:
                            if i in self.letters[char]['not_position']:
                                skip = True
                                break
                                
                else:
                    if self.final_guess[i] != char:
                        skip = True
                        break
            
            if skip:
                continue

            if not self.in_word.issubset(chars.keys()):
                continue

            for char in chars:
                if self.letters[char]['in_word'] and chars[char] > 1:

                    if chars[char] == 2 and not self.letters[char]['double']:
                        skip = True
                        break
                    
                    if chars[char] == 3 and not self.letters[char]['triple']:
                        skip = True
                        break
                        

            if not skip:
                new_words.append(word)

        self.words = new_words               



    def make_probabilities(self) -> dict[str, float]:
        probs = {}
        divider = len(self.words)

        for word in self.words:

            for i, char in enumerate(word):
                if char not in probs:
                    probs[char] = {}
                
                if i not in probs[char]:
                    probs[char][i] = 1
                else:
                    probs[char][i] += 1

        for char in probs:
            for index in probs[char]:
                probs[char][index] = probs[char][index] / divider

        return probs
                


    def grab_best_word(self, words: list) -> str:
        # guess_range = int(len(self.words) * 0.1)
        # index = random.randint(0, guess_range)
        return words[0][0]
    


    def play_wordle(self, own_word: str = None ) -> None:
        final_word = own_word if own_word is not None else self.get_random_word()
        guesses = []
        
        for i in range(6):
            best_words = self.valid_word_prob()
            best_word = self.grab_best_word(best_words)

            guesses.append(best_word)

            if self.compare(final_word, guess=best_word):
                return [True, i]
            
            self.filter_words()
            self.probabilities = self.make_probabilities()
        
        return [False, i]
    


    def ny_compare(self, guseed_word: str, feedback: list[str]) -> None:
        index = 0
        chars = {}
        char_info = {}

        for char, info in zip(guseed_word, feedback):
            key = char if char not in char_info else f"{char}{chars[char]}"
            char_info[key] = {'passed': None}

            if info == 'b':
                self.letters[char]['in_word'] = False
                char_info[char] = {'passed': False}

            elif info == 'g':
                self.letters[char]['in_word'] = True
                self.letters[char]['position'].add(index)
                self.final_guess[index] = char
                self.in_word.add(char)
                char_info[key] = {'passed': True}
            else:
                self.letters[char]['in_word'] = True
                self.letters[char]['not_position'].add(index)
                char_info[key] = {'passed': True}
                self.in_word.add(char)
            
            index += 1
            chars[char] = chars.get(char, 0) + 1
        
        for char in chars:
            if chars[char] == 1:
                continue

            keys = char_info.keys()
            checks = [key for key in keys if char in key]

            if chars[char] == 2:
                for check in checks:
                    if not char_info[check]['passed']:
                        self.letters[char]['double'] = False
                        self.letters[char]['triple'] = False
                        break
            
            elif chars[char] == 3:
                failed_count = 0
                for check in checks:
                    if not char_info[check]['passed']:
                        failed_count += 1
                
                if failed_count == 1:
                    self.letters[char]['triple'] = False
                elif failed_count == 2:
                    self.letters[char]['double'] = False
                    self.letters[char]['triple'] = False



    def skip(self, best_words: list[str], word_picked: str, index: int):
        while True:
            index = None
            for i, word in enumerate(best_words):
                if word[0] == word_picked:
                    index = i
                    break
                
            best_words.pop(index)
            word_picked = self.grab_best_word(best_words)
            print(f"The best word to guess is:\n{word_picked}")
            inputs = input(f"Please input the results for the {index + 1} word: ")
            print()
            
            if inputs != 'skip':
                return inputs, word_picked



    def calculate_word_score(self, word: str) -> float:
        """Calculate a word's score based on multiple factors:
        1. Letter frequency in possible words
        2. Position-specific letter probability
        3. Information gain potential
        4. Pattern uniqueness
        """
        if word in self.word_score_cache:
            return self.word_score_cache[word]

        # Basic letter probability score
        letter_score = self._calculate_letter_score(word)
        
        # Pattern diversity score (how well it splits remaining possibilities)
        pattern_score = self._calculate_pattern_score(word)
        
        # Position score (value of letters in specific positions)
        position_score = self._calculate_position_score(word)
        
        # Combine scores with weights
        total_score = (
            0.4 * letter_score +
            0.4 * pattern_score +
            0.2 * position_score
        )
        
        self.word_score_cache[word] = total_score
        return total_score

    def _calculate_letter_score(self, word: str) -> float:
        """Calculate score based on letter frequencies"""
        chars = Counter(word)
        score = 0
        for char, count in chars.items():
            if self.letters[char]['in_word'] is None:  # Unknown letter
                score += sum(self.probabilities[char].values()) / count
        return score

    def _calculate_pattern_score(self, word: str) -> float:
        """Calculate how well this word would split the remaining possibilities"""
        if len(self.words) <= 1:
            return 0
        
        pattern_counts = defaultdict(int)
        total_patterns = 0
        
        # Sample a subset of remaining words for performance
        sample_size = min(100, len(self.words))
        sample_words = random.sample(self.words, sample_size)
        
        for possible_word in sample_words:
            pattern = self._get_feedback_pattern(word, possible_word)
            pattern_counts[pattern] += 1
            total_patterns += 1
        
        # Calculate entropy (information gain)
        entropy = 0
        for count in pattern_counts.values():
            prob = count / total_patterns
            entropy -= prob * math.log2(prob)
        
        return entropy

    def _calculate_position_score(self, word: str) -> float:
        """Calculate score based on position-specific letter probabilities"""
        score = 0
        for i, char in enumerate(word):
            if i in self.letters[char]['position']:
                score += 1
            elif i in self.letters[char]['not_position']:
                score -= 0.5
        return score

    def _get_feedback_pattern(self, guess: str, answer: str) -> str:
        """Generate a pattern string for how guess matches answer"""
        pattern = ['b'] * 5
        answer_chars = Counter(answer)
        
        # First pass: mark correct positions
        for i, (g, a) in enumerate(zip(guess, answer)):
            if g == a:
                pattern[i] = 'g'
                answer_chars[g] -= 1
        
        # Second pass: mark yellow positions
        for i, (g, a) in enumerate(zip(guess, answer)):
            if pattern[i] == 'b' and g in answer_chars and answer_chars[g] > 0:
                pattern[i] = 'y'
                answer_chars[g] -= 1
            
        return ''.join(pattern)



def simulate_wordle(number_of_wordles: int, run_count: int):
    results = {}
    for index in range(number_of_wordles + 5):
        results[index + 1] = 0 
    results['failed'] = 0
        
    for _ in range(run_count):
    
        wordles = {}
        for index in range(number_of_wordles):
            wordle = Wordle()
            final_word = wordle.get_random_word()
            f_letters = wordle.final_guess_letters(final_word)
            wordles[index] = {'wordle': wordle, 'done': False, 'f_letters': f_letters}
        
        completed = 0
    
        for time in range(number_of_wordles + 5):
            
            less_amount = float('inf')
            chosen_wordle = None
            for wordle in wordles:
                
                if wordles[wordle]["done"]:
                    continue

                words_amount = len(wordles[wordle]["wordle"].words)

                if words_amount < less_amount and not wordles[wordle]["done"]:
                    less_amount = words_amount
                    chosen_wordle = wordles[wordle]["wordle"]
                
            best_words = chosen_wordle.valid_word_prob()
            best_word = chosen_wordle.grab_best_word(best_words)

            for wordle in wordles:

                if wordles[wordle]["done"]:
                    continue

                inputs = wordles[wordle]["wordle"].compare(wordles[wordle]["f_letters"], best_word)
                inputs_set = set(inputs)
                if len(inputs_set) == 1 and 'g' in inputs_set:
                    wordles[wordle]["done"] = True
                    completed += 1
                    continue

                wordles[wordle]["wordle"].filter_words()
                wordles[wordle]["wordle"].probabilites = wordles[wordle]["wordle"].make_probabilities()

            if completed == number_of_wordles:
                break
            
        if completed == number_of_wordles:
            results[time + 1] += 1
        else:
            results['failed'] += 1

    return results



def aggregate_results(partial_results):
    total_results = Counter()
    for result in partial_results:
        total_results.update(result)
    return total_results



def plot_histogram(results, output_file='wordle_histogram.png'):
    labels = list(map(str, results.keys()))
    values = list(results.values())
    
    plt.bar(labels, values)
    plt.xlabel('Attempts to Guess the Word / Failed')
    plt.ylabel('Frequency')
    plt.title('Wordle Results Distribution')
    
    plt.savefig(output_file)  # Save the plot to a file
    plt.close()  # Close the plot to free resources



if __name__ == "__main__":
    number_of_wordles = 16
    total_runs = 1_000
    num_workers = os.cpu_count()
    runs_per_worker = total_runs // num_workers

    # results = simulate_wordle(number_of_wordles, runs_per_worker)

    start_time = time.time()
    results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(simulate_wordle, number_of_wordles, runs_per_worker) for _ in range(num_workers)]
    
        for future in futures:
            results.append(future.result())
    
    end_time = time.time()
    print(f"The total time taken was {end_time - start_time} seconds")

    aggregated_results = aggregate_results(results)

    wins = 0
    for key, val in aggregated_results.items():
        if key == 'failed':
            continue

        wins += val

    print(f"The WIN% is {(wins / total_runs) * 100 :.2f}")

    plot_histogram(aggregated_results, f"wordle_histogram_{number_of_wordles}.png")