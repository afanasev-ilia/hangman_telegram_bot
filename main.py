import random

from hangman_data import stages, word_list


def get_word():
    return random.choice(word_list).upper()


def display_hangman(tries):
    return stages[tries]


def is_repeat(data, guessed_letters, guessed_words):
    if data in guessed_letters or data in guessed_words:
        return True
    return False


def is_valid_input(data):
    if not data.isalnum():
        return False
    return True


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
            if len(data) == 1:
                count = 0
                if is_repeat(data, guessed_letters, guessed_words):
                    print('Вы уже вводили эту букву!')
                    continue
                guessed_letters.append(data)
                for cur in range(len(word)):
                    if word[cur] == data:
                        word_completion[cur] = data
                        count += 1
                if count == 0:
                    print('Неверно!')
                    tries -= 1
                elif ''.join(word_completion) == word:
                    print('Поздравляем, вы угадали слово! Вы победили!')
                    guessed = True
                else:
                    print('Поздравляем, вы угадали букву!')
            else:
                guessed_words.append(data)
                if data == word:
                    print('Поздравляем, вы угадали слово! Вы победили!')
                    guessed = True
                else:
                    print('Неверно!')
                    tries -= 1
        if not guessed:
            print(display_hangman(tries))
            print('Вы проиграли!')
            print(f'Правильный ответ {word}')
        answer = input('Хотите сыграть ещё?\n 1 - да, 2 - нет\n')
        if answer == '2':
            break
    print('Спасибо, что играли в нашу игру! До встречи!')


if __name__ == '__main__':
    play()
