import random

from hangman_data import stages, word_list


def get_word():
    return random.choice(word_list).upper()


def display_hangman(tries):
    return stages[tries]


def play():
    print('Давайте играть в угадайку слов!')
    while True:
        word = get_word()
        word_completion = ['_' for _ in range(len(word))]
        guessed = False
        guessed_letters = []
        guessed_words = []
        tries = 6
        while not guessed and tries > 0:
            print(display_hangman(tries))
            print(*word_completion)
            data = input('Введите символ или слово целиком\n').upper()


if __name__ == '__main__':
    play()
