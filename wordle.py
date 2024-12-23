import os
import time
import random
from concurrent.futures import ProcessPoolExecutor

class Wordle():
    
    def __init__(self, words_list: str) -> None:
        self.words = self.get_words(words_list)
        self.probabilities = self.make_probabilities()
        self.letters = self._get_letters()
        self.final_guess = ['', '', '', '', '']
        self.in_word = set()

    

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
    


    def get_words(self, word_type: str) -> list[str]:
        words = []
        word_file = "all_wordle_accepted_words.txt" if word_type == 'easy' else "all_valid_words.txt"
        with open(word_file, "r") as f:
            for word in f:
                words.append(word.strip())
        
        return words



    def valid_word_prob(self) -> list[list[str, float]]:
        word_probabilities = []

        for word in self.words:
            
            chars = {}
            word_prob = 0
            for i, char in enumerate(word):

                chars[char] = chars.get(char, 0) + 1

                word_prob += self.probabilities[char][i] / chars[char]
                
            word_probabilities.append([word, word_prob])

        return sorted(word_probabilities, key=lambda item: item[1], reverse=True)



    def get_random_word(self):
        return random.choice(self.words)
    


    def compare(self, final_word: str, guess: str) -> bool:
        f_letters = {}
        for i, char in enumerate(final_word):
            if char not in f_letters:
                f_letters[char] = [i]
            else:
                f_letters[char].append(i)
        
        is_word = True
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
                else:
                    self.letters[char]['not_position'].add(i)
                    self.in_word.add(char)
                    is_word = False
            else:
                self.letters[char]['in_word'] = False
                is_word = False
        
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
                    
        return is_word



    def filter_words(self) -> None:
        new_words = []
        for word in self.words:
            
            if word == 'bluff':
                a = 5

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
        guess_range = int(len(self.words) * 0.1)
        index = random.randint(0, guess_range)
        return words[index][0]
    


    def play_wordle(self, own_word: str = None ) -> None:
        final_word = own_word if own_word is not None else self.get_random_word()
        guesses = []
        
        for i in range(6):
            best_words = self.valid_word_prob()
            best_word = self.grab_best_word(best_words)
            guesses.append(best_word)
            # best_word = guesses[i]

            if self.compare(final_word, guess=best_word):
                # print(f"You gussed the word '{final_word}' in {i + 1} gusses")
                return True
            
            self.filter_words()
            self.probabilities = self.make_probabilities()
        
        return False
    


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



    def ny_times_word_finder(self):
        print("""
Note when you input the best word into wordle, for the feed back:
for GREEN: input g
for YELLOW: input y
for GREY: input b\n""")

        for _ in range(6):
            best_words = self.valid_word_prob()
            best_word = self.grab_best_word(best_words)
            print("Please input the word into wordle, then input the feedback afterwards")
            print(f"Total Words are {len(self.words)}")
            print(f"The best word to guess is:\n{best_word}")


            inputs = input("Please input the results from New York Times: ")
            print()  
            valid_inputs = inputs.split()
            self.ny_compare(best_word, valid_inputs)     
            self.filter_words()
            self.probabilities = self.make_probabilities()




def simulate_wordle(word_type, words, run_count):
    count = 0
    a = Wordle(word_type)
    
    for _ in range(run_count):
        word = random.choice(words)
        if a.play_wordle(word):
            count += 1
        a.reset(word_type)
    
    return count



if __name__ == "__main__":
    word_type = "easy"
    # wordle = Wordle(word_type)
    # wordle.ny_times_word_finder()
    
    start_time = time.time()
    a = Wordle(word_type)
    words = a.words
    total_runs = 10_000
    num_workers = os.cpu_count()  # Adjust based on your system's cores
    runs_per_worker = total_runs // num_workers

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Divide the work across workers
        futures = [executor.submit(simulate_wordle, word_type, words, runs_per_worker) for _ in range(num_workers)]
        
        # Collect results from all workers
        total_count = sum(f.result() for f in futures)

    end_time = time.time()
    print(f"Solve Percentage is {total_count / total_runs * 100:.2f}%")
    print(f"Total time taken was {end_time - start_time} seconds")



 