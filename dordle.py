from wordle import Wordle

print("Please select which word bank to use")
print("Type 'easy' or 'hard'")

words = input("Input type here: ")

left_worlde = Wordle(words)
right_wordle = Wordle(words)

print("""
Note when you input the best word into dordle, for the feed back:
for GREEN: input g
for YELLOW: input y
for GREY: input b\n
          
An example would be:
Please input the results from New York Times: b b g g Y g y b g g
""")

print("If the wordle has been solved please write 'solved' after the 'Please input the results from New York Times:' ")


stay = True
while stay:

    done_left = False
    done_right = False
  
    for _ in range(7):

        if len(left_worlde.words) <= len(right_wordle.words) and not done_left:
            left_words = left_worlde.valid_word_prob()
            best_word = left_worlde.grab_best_word(left_words)
        else:
            right_words = right_wordle.valid_word_prob()
            best_word = right_wordle.grab_best_word(right_words)
                    


        print("Please input the word into wordle, then input the feedback afterwards")
        print(f"Total Words for the left side {len(left_worlde.words)}, and the right side {len(right_wordle.words)}")
        print(f"The best word to guess is:\n{best_word}")


        inputs = input("Please input the results from New York Times: ")
        print()  

        if "solved" == inputs:
            break

        valid_inputs = inputs.split()
        if "solved" in inputs and len(inputs) != 1:
            if valid_inputs[0] == "solved":
                done_left = True
                valid_inputs.pop(0)
            else:
                done_right = True
                valid_inputs.pop(5)
        
        if not done_left:
            left_words = valid_inputs[:5] if len(valid_inputs) > 5 else valid_inputs
            left_worlde.ny_compare(best_word, left_words)     
            left_worlde.filter_words()
            left_worlde.probabilities = left_worlde.make_probabilities()

        if not done_right:
            right_words = valid_inputs[5:] if len(valid_inputs) > 5 else valid_inputs
            right_wordle.ny_compare(best_word, valid_inputs[5:])     
            right_wordle.filter_words()
            right_wordle.probabilities = right_wordle.make_probabilities()
    
    print("If you would like to continue input continue, otherwise input exit")
    play_again = input()
    if play_again == 'continue':
        left_worlde.reset(words)
        right_wordle.reset(words)
    else:
        stay = False
