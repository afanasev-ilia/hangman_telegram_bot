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
    # guessed_letters = []
    # guessed_words = []
    # tries = len(word)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Game started! Guess the word:',
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=' '.join(word_completion),
    )



# play_handler = ConversationHandler(
#     entry_points=[
#         MessageHandler(
#             Filters.text('Начать игру'),
#             play,
#         ),
#     ],
#     states={
#         # PLAYING: [
#         #     MessageHandler(
#         #         Filters.text,
#         #         order_handler,
#         #     ),
#         # ],
#         # ITEM_ORDER: [
#         #     MessageHandler(
#         #         Filters.all,
#         #         item_handler,
#         #     ),
#         # ],
#     },
#     fallbacks=[
#     #     CommandHandler('cancel', cancel_handler),
#     ],
# )

updater = (
    Updater(token=TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, play))
updater.start_polling()
updater.idle()
