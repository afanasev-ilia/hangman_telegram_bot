import logging
import random

from hangman_data import stages, word_list

logging.basicConfig(
    filename='hangman.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)


def get_word():
    return random.choice(word_list).upper()


def display_hangman(tries):
    return stages[tries]


def is_repeat(data, repeated_letters, repeated_words):
    if data in repeated_letters or data in repeated_words:
        return True
    return False


def is_valid_input(data: str) -> bool:
    for char in data:
        if not 1040 <= ord(char) <= 1103:
            print('Допустимы только буквы русского алфавита!')
            return False
    return True


def play():
    logging.info('Starting game')
    while True:
        try:
            word = get_word()
            logging.info(f'Selected word: {word}')
            word_completion = ['_' for _ in range(len(word))]
            guessed = False
            guessed_letters = []
            guessed_words = []
            tries = 6
            while not guessed and tries > 0:
                print(display_hangman(tries))
                print(*word_completion)
                data = input('Введите символ или слово целиком\n').upper()
                logging.info(f'User input: {data}')
                if not is_valid_input(data):
                    continue
                if len(data) == 1:
                    count = 0
                    if is_repeat(data, guessed_letters, guessed_words):
                        logging.warning('User input is a repeat')
                        print('Вы уже вводили эту букву!')
                        continue
                    guessed_letters.append(data)
                    for cur in range(len(word)):
                        if word[cur] == data:
                            word_completion[cur] = data
                            count += 1
                    if count == 0:
                        logging.warning('User input is incorrect')
                        print('Неверно!')
                        tries -= 1
                    elif ''.join(word_completion) == word:
                        logging.info('User guessed the word')
                        print('Поздравляем, вы угадали слово! Вы победили!')
                        guessed = True
                    else:
                        logging.info('User guessed a letter')
                        print('Поздравляем, вы угадали букву!')
                else:
                    if is_repeat(data, guessed_letters, guessed_words):
                        logging.warning('User input is a repeat')
                        print('Вы уже вводили это слово!')
                        continue
                    guessed_words.append(data)
                    if data == word:
                        logging.info('User guessed the word')
                        print('Поздравляем, вы угадали слово! Вы победили!')
                        guessed = True
                    else:
                        logging.warning('User input is incorrect')
                        print('Неверно!')
                        tries -= 1
            if not guessed:
                logging.info('User lost the game')
                print(display_hangman(tries))
                print('Вы проиграли!')
                print(f'Правильный ответ {word}')
            answer = input('Хотите сыграть ещё?\n 1 - да, 2 - нет\n')
            logging.info(f'User answer: {answer}')
            if answer == '2':
                break
        except Exception as e:
            logging.error(f'Error occurred: {e}')
            print(f'Произошла ошибка: {e}')
    logging.info('Game ended')
    print('Спасибо, что играли в нашу игру! До встречи!')


if __name__ == '__main__':
    play()
