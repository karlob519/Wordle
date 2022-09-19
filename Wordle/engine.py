import random

# Loading the data sets forr possible solutions and accepted guesses
def load_solutions():
    with open('valid_solutions.csv') as word_file:
        valid_sols = word_file.read().split()
    
    return valid_sols

def load_guesses():
    with open('valid_guesses.csv') as word_file:
        valid_gs = word_file.read().split()
    
    return valid_gs


possible_solutions = load_solutions()[1:]
valid_guesses = load_guesses()[1:]

def guesses():
    return possible_solutions + valid_guesses

#Generating a random solution
def wordle():
    x = random.randint(1, len(possible_solutions)-1)
    answer = possible_solutions[x]
    return answer
# Defining a function that returns 0 if a character is not in the solution, 1 if it is but in the wrong place 
# And 2 if it is in the right place
def score(guess: str, solution: str):
    result = []
    chars = {}
    for char in solution:
        chars[char] = solution.count(char)
    for i in range(len(solution)):
        char1, char2 = guess[i], solution[i]
        if char1 == char2:
            result.append(2)
            chars[char1] -= 1
        elif char1 not in solution:
            result.append(0)
        else:
            result.append(-50)
    for j in range(len(solution)):
        if result[j] == -50:
            char = guess[j]
            if chars[char] > 0:
                result[j] = 1
                chars[char] -= 1
            else:
                result[j] = 0
    return result


def game(n: int=6):  
    print(f'You have {n} attempts to guess the word!')    
    attempt = 0
    while attempt < n:
        effort = input('Your guess: ')
        if effort in possible_solutions or effort in valid_guesses:
            print(f'Score: {score(effort, wordle)}    Attempt: {attempt+1}')
            attempt += 1
        else:
            print('Invalid guess, try again!')

        if sum(score(effort, wordle)) == 10:
            print('Well done, you guessed the solution in {} attempts.'.format(attempt))
            break
        else:
            None
    print(wordle)
    return


