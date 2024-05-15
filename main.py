import random

from hangman_data import stages, word_list


def get_word():
    return random.choice(word_list).upper()


def display_hangman(tries):
    return stages[tries]


def play():
    word = get_word()

    # print(display_hangman(tries))


if __name__ == '__main__':
    play()
