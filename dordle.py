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
Please input the results for the left word: g b b y g
      
Please input the results for the right word: b b y g b  
""")

print("If the wordle has been solved please write 'solved' after the 'Please input the results from New York Times:' ")


stay = True

while stay:

    done_left = False
    done_right = False
    leave = False
  
    for _ in range(7):
        
        less_left = len(left_worlde.words) <= len(right_wordle.words)

        if done_left:
            chosen_wordle = right_wordle
        elif not done_right and not less_left:
            chosen_wordle = right_wordle
        else:
            chosen_wordle = left_worlde
        
        best_words = chosen_wordle.valid_word_prob()
        best_word = chosen_wordle.grab_best_word(best_words)


        print("Please input the word into wordle, then input the feedback afterwards")
        print(f"Total Words for the left side {len(left_worlde.words)}, and the right side {len(right_wordle.words)}")
        print(f"The best word to guess is:\n{best_word}")


        for i in range(2):
            turn = i % 2 == 0
            text = "Please input the results for the left word:" if turn else "Please input the results for the right word:"

            if turn and done_left:
                continue

            if not turn and done_right:
                continue

            inputs = input(f"{text} ")
            print()  

            if done_left and done_right:
                leave = True
                break

            if "solved" == inputs:
                if turn:
                    done_left = True
                else:
                    done_right = True

            valid_inputs = inputs.split()
            
            if turn:
                if not done_left:
                    left_worlde.ny_compare(best_word, valid_inputs)     
                    left_worlde.filter_words()
                    left_worlde.probabilities = left_worlde.make_probabilities()
            else:
                if not done_right:
                    right_wordle.ny_compare(best_word, valid_inputs)     
                    right_wordle.filter_words()
                    right_wordle.probabilities = right_wordle.make_probabilities()

        if leave:
            break
        
    print("If you would like to continue input continue, otherwise input exit")
    play_again = input()
    if play_again == 'continue':
        left_worlde.reset(words)
        right_wordle.reset(words)
    else:
        stay = False
