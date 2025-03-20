# import logging
import random

from hangman_data import stages, word_list


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
            return False
    return True
