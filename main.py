import random
import datetime
import sys
import time


def initialize_words():
    with open('words.txt', 'r') as word_list:
        return word_list.read().splitlines()

def check_word(word_list):
    with open('today.txt', "r") as temp:
        last_date = temp.readline()
        current_date = str(datetime.date.today()) + "\n"
        if last_date != current_date:
            new_word = random.choice(word_list)
            new_data = [current_date, "false\n", new_word]
            with open('today.txt', 'w') as old_data:
                old_data.writelines(new_data)
            return new_word
        else:
            if temp.readline() == "true\n":
                print("You have already finished today's Wordle.")
                tomorrow = datetime.datetime.now() + datetime.timedelta(1)
                midnight = datetime.datetime(year=tomorrow.year, month=tomorrow.month,
                                             day=tomorrow.day, hour=0, minute=0, second=0)
                print(
                    f'A new Wordle comes in {datetime.timedelta(seconds=(midnight - datetime.datetime.now()).seconds)}.')
                sys.exit(0)
            else:
                return temp.readline().replace("\n", "")


if __name__ == '__main__':
    word_list = initialize_words()
    word = check_word(word_list)
    found = False
    for i in range(6):
        guess = ""
        while len(guess) != 5 or guess not in word_list:
            print(f'{i + 1}: ', end='')
            guess = input().lower()
        occurences = list(word)
        if guess == word:
            found = True
        for j, c in enumerate(guess):
            if c == occurences[j]:
                occurences[j] = -1
                print(
                    f'\u001b[1m\u001b[48;5;34m{c}\u001b[0m', end='', flush=True)
            elif c in occurences:
                occurences[occurences.index(c)] = -1
                print(
                    f'\u001b[1m\u001b[48;5;142m{c}\u001b[0m', end='', flush=True)
            else:
                print(
                    f'\u001b[1m\u001b[48;5;237m{c}\u001b[0m', end='', flush=True)
            time.sleep(0.25)
        print()
        if found:
            print(f'You win in {i + 1} {"attempts" if i > 0 else "attempt"}!')
            break
    else:
        print(f'You lose! The word was {word}.')

    with open('today.txt', 'r',) as temp:
        new_data = temp.readlines()
    new_data[1] = "true\n"
    with open('today.txt', 'w') as old_data:
        old_data.writelines(new_data)

    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    midnight = datetime.datetime(year=tomorrow.year, month=tomorrow.month,
                                 day=tomorrow.day, hour=0, minute=0, second=0)
    print(
        f'A new Wordle comes in {datetime.timedelta(seconds=(midnight - datetime.datetime.now()).seconds)}.')
