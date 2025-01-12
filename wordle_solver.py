from wordle import Wordle

def create_wordles(number_of_words: int):
    wordles = {}
    for index in range(number_of_words):
        wordles[index] = {'wordle': Wordle(), 'done': False}
    
    return wordles



print("Please Specifie how many words you are trying to solve please!")
number_of_words = int(input("Input number here: "))
wordles = create_wordles(number_of_words)

print("""
Rules of how to play:
      
When you input the best word into dordle, for the feed back:
for GREEN: input g
for YELLOW: input y
for GREY: input b
          
An example would be:
Please input the results for the 1st word: g b b y g
      
Please input the results for the 2nd word: b b y g b 
and then do the same for 3rd and 4th 

If the word presented was is not valid, please input skip and a new word will be provided.
""")

print("If the wordle has been solved please write 'solved' after the 'Please input the results from New York Times:' ")

stay = True

while stay:
  
    for _ in range(number_of_words + 5):
        
        less_amount = float('inf')
        chosen_wordle = None
        for wordle in wordles:

            if wordles[wordle]["done"]:
                continue
            
            words_amount = len(wordles[wordle]["wordle"].words)

            if words_amount < less_amount and not wordles[wordle]["done"]:
                less_amount = words_amount
                chosen_wordle = wordles[wordle]["wordle"]
        
        if chosen_wordle is None:
            print("There was no word found :(")
            break
        
        best_words = chosen_wordle.valid_word_prob()
        best_word = chosen_wordle.grab_best_word(best_words)


        print("Please input the word into wordle, then input the feedback afterwards")
        for index in wordles:
            words = wordles[index]["wordle"].words
            print(f"For the selected word serach of {index + 1} ther are {len(words)} words to choose from\n")
        print(f"The best word to guess is:\n{best_word}")


        for i, wordle in enumerate(wordles):

            if wordles[wordle]["done"]:
                continue

            inputs = input(f"Please input the results for the {i + 1} word: ")
            print()

            if inputs == 'skip':
                inputs, best_word = chosen_wordle.skip(best_words, best_word, i)

            if inputs == "solved":
                wordles[wordle]["done"] = True
                continue

            valid_inputs = inputs.split()

            wordles[wordle]["wordle"].ny_compare(best_word, valid_inputs)
            wordles[wordle]["wordle"].filter_words()
            wordles[wordle]["wordle"].probabilites = wordles[wordle]["wordle"].make_probabilities()

        
    print("If you would like to continue input continue, otherwise input exit")
    play_again = input()
    if play_again == 'continue':

        same = input("Continue with the same amout: [y]/n ")
        if same in {'', "y", "Y"}:
            wordles = create_wordles(number_of_words)
        else:
            print("Please Specifie how many words you are trying to solve please!")
            number_of_words = int(input("Input number here: "))
            wordles = create_wordles(number_of_words)

    else:
        stay = False
