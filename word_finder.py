import math
import random
from concurrent.futures import ProcessPoolExecutor

class Wordle():
    
    def __init__(self) -> None:
        self.words = self.get_words()
        self.probabilities = self.make_probabilities()
        self.letters = self._get_letters()
        self.final_guess = ['', '', '', '', '']

    

    def reset(self):
        self.words = self.get_words()
        self.probabilities = self.make_probabilities()
        self.letters = self._get_letters()
        self.final_guess = ['', '', '', '', '']



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
        with open("words.txt", "r") as f:
            for word in f:
                words.append(word.strip())
        
        return words



    def valid_word_prob(self) -> list[list[str, float]]:
        word_probabilities = []

        for word in self.words:
            
            chars = {}
            word_prob = 0
            for i, char in enumerate(word):

                if char not in chars:
                    chars[char] = 1
                else:
                    chars[char] += 1

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
                else:
                    self.letters[char]['not_position'].add(i)
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
            
            skip = False
            chars = {}
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
            
            for char in chars:
                if chars[char] > 1:

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
        divider = 14855

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
                


    def play_wordle(self, own_word: str = None ) -> None:
        final_word = own_word if own_word is not None else self.get_random_word()
        guesses = []
        
        did = False
        for i in range(5):
            best_words = self.valid_word_prob()
            # if len(best_words) > 5:
                # best_word = random.choice(best_words[:5])[0]
            # else:
                # best_word = random.choice(best_words)[0]
            best_word = best_words[0][0]
            guesses.append(best_word)

            if self.compare(final_word, guess=best_word):
                # print(f"You gussed the word '{final_word}' in {i + 1} gusses")
                return True
            
            self.filter_words()
            self.probabilities = self.make_probabilities()
        
        return False
    


def simulate_wordle_game(wordle_instance, words):
    """Simulate a single round of Wordle."""
    wins = 0
    for _ in range(125):  # Adjust to distribute workload
        word = random.choice(words)
        if wordle_instance.play_wordle(word):
            wins += 1
            print("won")
        else:
            print("lose")
        wordle_instance.reset()
    return wins



if __name__ == '__main__':
    a = Wordle()
    words = a.words

    wins = 0
    count = 0
    for word in words:

        for _ in range(10):
            if a.play_wordle(word):
                print("passed")
                wins += 1
            else:
                print("failed")

            a.reset()
            count += 1

    print(f"the total win% was {wins / countt}")

# if __name__ == '__main__':
#     a = Wordle()
#     words = a.words
#     num_processes = 8  # Number of processes (adjust based on your CPU cores)

#     with ProcessPoolExecutor(max_workers=num_processes) as executor:
#         # Divide the work among processes
#         results = executor.map(simulate_wordle_game, [a] * num_processes, [words] * num_processes)

#     # Collect results from all processes
#     total_wins = sum(results)
#     print(f"The total win% was {total_wins / 1_000}")



 