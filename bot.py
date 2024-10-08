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

WORD, WORD_COMPLETION, TRIES, GUESSING_LETTER, GUESSING_WORD = (
    'word',
    'word_completion',
    'tries',
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
    context.user_data[WORD] = get_word()
    context.user_data[WORD_COMPLETION] = ['_' for _ in range(len(context.user_data[WORD]))]
    # guessed = False
    # guessed_letters = []
    # guessed_words = []
    context.user_data[TRIES] = 2

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" ".join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком'
            ),
        )
    user_input = update.message.text.upper()
    if len(user_input) == 1:
        return GUESSING_LETTER
    return GUESSING_WORD
        # count = 0
        # guessed_letters.append(user_input)
        # for cur in range(len(word)):
        #     if word[cur] == user_input:
        #         word_completion[cur] = user_input
        #         count += 1

    # while 1 > 0:
    #     user_input = update.message.text.upper()
    #     if is_repeat(user_input, guessed_letters, guessed_words):
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id,
    #             text='Вы уже вводили эту букву или символ!'
    #         )
    #         continue
    #     guessed_letters.append(user_input)


def guessing_letter_handler(update: Update, context: CallbackContext) -> int:
    print('это guessing_letter_handler')

 
def guessing_word_handler(update: Update, context: CallbackContext) -> int:
    print('это guessing_word_handler')


def cancel_handler(
        update: Update,
        context: CallbackContext
) -> int:
    update.message.reply_text('Спасибо, что играли в нашу игру! До встречи!')
    return ConversationHandler.END


play_handler = ConversationHandler(
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
                guessing_letter_handler,
            ),
        ],
        GUESSING_WORD: [
            MessageHandler(
                Filters.all,
                guessing_word_handler,
            ),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_handler),
    ],
)


updater = (
    Updater(token=TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, play))
updater.start_polling()
updater.idle()
