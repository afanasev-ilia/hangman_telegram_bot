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

from main import display_hangman, get_word

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

WORD, WORD_COMPLETION, TRIES, PLAY, GUESSING_LETTER, GUESSING_WORD = (
    'word',
    'word_completion',
    'tries',
    'play',
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


def start_game(update: Update, context: CallbackContext) -> int:
    context.user_data[WORD] = get_word()
    context.user_data[WORD_COMPLETION] = [
        '_' for _ in range(len(context.user_data[WORD]))
    ]
    # guessed = False
    # guessed_letters = []
    # guessed_words = []
    context.user_data[TRIES] = 6

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" ".join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком'
                f'{context.user_data[WORD]}\n\n'
            ),
        )
    return PLAY


def play(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.upper()
    for cur in range(len(context.user_data[WORD])):
        if context.user_data[WORD][cur] == user_input:
            context.user_data[WORD][cur] = user_input
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" ".join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком'
                f'{context.user_data[WORD]}\n\n'
            ),
        )
    return PLAY


# def guessing_letter_handler(update: Update, context: CallbackContext) -> int:
#     context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=(
#                 'это guessing_letter_handler'
#             ),
#     )


# def guessing_word_handler(update: Update, context: CallbackContext) -> int:
#     context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=(
#                 'это guessing_word_handler'
#             ),
#     )


def cancel_handler(
        update: Update,
        context: CallbackContext
) -> int:
    update.message.reply_text('Спасибо, что играли в нашу игру! До встречи!')
    return ConversationHandler.END


play_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.text('Начать игру'),
            start_game,
        ),
    ],
    states={
        PLAY: [
            MessageHandler(
                Filters.all,
                play,
            ),
        ],
        # GUESSING_LETTER: [
        #     MessageHandler(
        #         Filters.all,
        #         guessing_letter_handler,
        #     ),
        # ],
        # GUESSING_WORD: [
        #     MessageHandler(
        #         Filters.all,
        #         guessing_word_handler,
        #     ),
        # ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_handler),
    ],
)


updater = (
    Updater(token=TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(play_handler)
updater.start_polling()
updater.idle()
