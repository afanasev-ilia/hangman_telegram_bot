import random

from hangman_data import stages, word_list


def get_word_by_length(min_length, max_length):
    filtered_words = [word for word in word_list if min_length <= len(word) <= max_length]
    return random.choice(filtered_words).upper()


def get_word(difficulty):
    if difficulty == 'easy':
        return get_word_by_length(3, 5)
    elif difficulty == 'medium':
        return get_word_by_length(6, 8)
    elif difficulty == 'hard':
        return get_word_by_length(9, 16)
    else:
        return random.choice(word_list).upper()
    
# def get_word():
#     return random.choice(word_list).upper()


def display_hangman(tries):
    return stages[tries]


def is_repeat(data, repeated_letters, repeated_words):
    if data in repeated_letters or data in repeated_words:
        return True
    return False


def is_valid_input(data: str) -> bool:
    for char in data:
        if not 1040 <= ord(char) <= 1103:
            return False
    return True
