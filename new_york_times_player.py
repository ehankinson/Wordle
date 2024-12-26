from wordle import *



################################################################
#               Selecting which word bank to use               #
################################################################

print("Please select which word bank to use")
print("Type 'easy' or 'hard'")

words = input("Input type here: ")

if words not in ['easy', 'hard']:
    print("Incorrect type")
else:
    wordle = Wordle(words)
    print("""
Note when you input the best word into wordle, for the feed back:
for GREEN: input g
for YELLOW: input y
for GREY: input b\n
          
An example would be:
Please input the results from New York Times: b b g g Y
""")
    
    print("If the wordle has been solved please write 'solved' after the 'Please input the results from New York Times:' ")

    

    stay = True
    while stay:

        for _ in range(6):
            best_words = wordle.valid_word_prob()
            best_word = wordle.grab_best_word(best_words)
            print("Please input the word into wordle, then input the feedback afterwards")
            print(f"Total Words are {len(wordle.words)}")
            print(f"The best word to guess is:\n{best_word}")


            inputs = input("Please input the results from New York Times: ")
            print()  

            if inputs == 'solved':
                break

            valid_inputs = inputs.split()
            wordle.ny_compare(best_word, valid_inputs)     
            wordle.filter_words()
            wordle.probabilities = wordle.make_probabilities()
        
        print("If you would like to continue input continue, otherwise input exit")
        play_again = input()
        if play_again == 'continue':
            wordle.reset(words)
        else:
            stay = False