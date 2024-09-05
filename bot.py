import os
import logging


from dotenv import load_dotenv
from pathlib import Path
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
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


async def wake_up(update: Update, context: CallbackContext) -> int:
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


async def play(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    word = get_word()
    word_completion = ['_' for _ in range(len(word))]
    guessed = False
    # guessed_letters = []
    # guessed_words = []
    tries = len(word)
    while not guessed and tries > 0:
        context.bot.send_message(
            chat_id=chat.id,
            text=display_hangman(tries),
        )
        context.bot.send_message(
            chat_id=chat.id,
            text=' '.join(word_completion),
        )
        context.bot.send_message(
            chat_id=chat.id,
            text='Введите символ или слово целиком',
        )
        data = update.message.text.upper()
        break


# updater = (
#     Updater(token=TELEGRAM_TOKEN)
# )
# updater.dispatcher.add_handler(CommandHandler('start', wake_up))
# updater.dispatcher.add_handler(MessageHandler(Filters.text, play))
# updater.start_polling()
# updater.idle()

work_report_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.text('Отчет о проделанной работе'),
            work_report,
        ),
    ],
    states={
        ORDER: [
            MessageHandler(
                Filters.all,
                order_handler,
            ),
        ],
        ITEM_ORDER: [
            MessageHandler(
                Filters.all,
                item_handler,
            ),
        ],
        EXECUTION_TIME: [
            MessageHandler(
                Filters.all,
                time_handler,
            ),
        ],
        WORK_IMAGE: [
            MessageHandler(
                Filters.all,
                work_image_handler,
            ),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_handler),
    ],
)

clean_report_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.text('Отчет об уборке рабочего места'),
            clean_report,
        ),
    ],
    states={
        ORDER: [
            MessageHandler(
                Filters.all,
                order_handler,
            ),
        ],
        CLEAN_IMAGE: [
            MessageHandler(
                Filters.all,
                clean_image_handler,
            ),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_handler),
    ],
)

updater = (
    Updater(token=settings.TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(work_report_handler)
updater.dispatcher.add_handler(clean_report_handler)