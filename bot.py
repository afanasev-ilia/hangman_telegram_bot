import os
import logging

from dotenv import load_dotenv
from pathlib import Path
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from main import display_hangman, get_word, is_repeat  # , is_valid_input

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


logging.basicConfig(
    level=logging.INFO,
    filename=Path('program.log'),
    filemode='w',
    format=(
        '%(name)s - %(asctime)s - %(levelname)s - %(lineno)d - %(message)s'
    ),
)

GUESSING_LETTER, GUESSING_WORD = (
    'guessing_letter',
    'guessing_word',
)


def wake_up(update: Update, context: CallbackContext) -> int:
    button = ReplyKeyboardMarkup(
        [['Начать игру'],],
        resize_keyboard=True,
    )
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте, {}! Давайте играть в угадайку слов!'.format(name),
        reply_markup=button,
    )


def play(update: Update, context: CallbackContext) -> int:
    word = get_word()
    word_completion = ['_' for _ in range(len(word))]
    # guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(tries)}\n'
                f'{" ".join(word_completion)}\n\n'
                'Введите символ или слово целиком'
            ),
        )

    while 1 > 0:
        user_input = update.message.text.upper()
        if is_repeat(user_input, guessed_letters, guessed_words):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы уже вводили эту букву или символ!'
            )
            continue
        guessed_letters.append(user_input)
        # if len(user_input) == 1:
        #     count = 0
        #     guessed_letters.append(user_input)
        #     for cur in range(len(word)):
        #         if word[cur] == user_input:
        #             word_completion[cur] = user_input
        #             count += 1
        #     break
        # guessed = True


clean_report_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.text('игра'),
            play,
        ),
    ],
    states={
        GUESSING_LETTER: [
            MessageHandler(
                Filters.all,
                #  guessing_letter_handler,
            ),
        ],
        GUESSING_WORD: [
            MessageHandler(
                Filters.all,
                # guessing_word_handler,
            ),
        ],
    },
    # fallbacks=[
    #     CommandHandler('cancel', cancel_handler),
    # ],
)


updater = (
    Updater(token=TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, play))
updater.start_polling()
updater.idle()
