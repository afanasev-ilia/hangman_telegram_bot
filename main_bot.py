import os
import logging
# import requests

from dotenv import load_dotenv
from pathlib import Path
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    Updater,
    Filters,
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

# WORK_EMPLOYEE, ORDER, ITEM_ORDER, EXECUTION_TIME, WORK_IMAGE = (
#     'employee',
#     'order',
#     'item_order',
#     'execution_time',
#     'image',
# )

# CLEAN_EMPLOYEE, CLEAN_IMAGE = (
#     'employee',
#     'image',
# )


def start(update: Update, context: CallbackContext) -> int:
    button = ReplyKeyboardMarkup(
        [['Начать игру'],],
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!',
        reply_markup=button,
    )


# def work_report(
#     update: Update,
#     context: CallbackContext,
# ) -> int:
#     context.user_data[WORK_EMPLOYEE] = Employee.objects.get(
#         external_id=update.effective_chat.id
#     ).id
#     update.message.reply_text(
#         'Введите номер счета что бы продолжить',
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     return ORDER


# def order_handler(
#         update: Update,
#         context: CallbackContext
# ) -> int:
#     context.user_data[ORDER] = int(update.message.text)
#     update.message.reply_text(
#         'Введите порядковый номер позиции из счета',
#     )
#     return ITEM_ORDER


# def item_handler(
#         update: Update,
#         context: CallbackContext
# ) -> int:
#     context.user_data[ITEM_ORDER] = int(update.message.text)
#     update.message.reply_text('Укажите время выполнения в минутах')
#     return EXECUTION_TIME


# def time_handler(
#         update: Update,
#         context: CallbackContext
# ) -> int:
#     context.user_data[EXECUTION_TIME] = int(update.message.text)
#     update.message.reply_text('Приложите фотографию')
#     return WORK_IMAGE


# def cancel_handler(
#         update: Update,
#         context: CallbackContext
# ) -> int:
#     update.message.reply_text('Отчет не отправлен')
#     return ConversationHandler.END


# def clean_report(
#         update: Update,
#         context: CallbackContext,
# ) -> int:
#     context.user_data[CLEAN_EMPLOYEE] = Employee.objects.get(
#         external_id=update.effective_chat.id
#     ).id
#     update.message.reply_text(
#         'Приложите фотографию',
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     return CLEAN_IMAGE


# work_report_handler = ConversationHandler(
#     entry_points=[
#         MessageHandler(
#             Filters.text('Отчет о проделанной работе'),
#             work_report,
#         ),
#     ],
#     states={
#         ORDER: [
#             MessageHandler(
#                 Filters.all,
#                 order_handler,
#             ),
#         ],
#         ITEM_ORDER: [
#             MessageHandler(
#                 Filters.all,
#                 item_handler,
#             ),
#         ],
#         EXECUTION_TIME: [
#             MessageHandler(
#                 Filters.all,
#                 time_handler,
#             ),
#         ],
#         WORK_IMAGE: [
#             MessageHandler(
#                 Filters.all,
#                 work_image_handler,
#             ),
#         ],
#     },
#     fallbacks=[
#         CommandHandler('cancel', cancel_handler),
#     ],
# )


updater = (
    Updater(token=TELEGRAM_TOKEN)
)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()
updater.idle()
