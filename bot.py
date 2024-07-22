import os
import logging


from dotenv import load_dotenv
from pathlib import Path
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Filters,
    MessageHandler,
    Updater,
)

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


def wake_up(update, context):
    button = ReplyKeyboardMarkup(
        [['Начать игру'],],
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте! Давайте играть в угадайку слов!',
        reply_markup=button,
    )


def play(update: Update, context: CallbackContext) -> int:
    pass


updater = (
    Updater(token=TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, play))
updater.start_polling()
updater.idle()
