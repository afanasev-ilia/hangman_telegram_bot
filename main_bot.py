import logging
# import requests
# import base64

# from django.conf import settings
from pathlib import Path
# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
# from telegram.ext import (
#     CommandHandler,
#     CallbackContext,
#     ConversationHandler,
#     MessageHandler,
#     Updater,
#     Filters,
# )

# from report.models import Employee


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


# def start(update: Update, context: CallbackContext) -> int:
#     Employee.objects.get_or_create(external_id=update.effective_chat.id)
#     button = ReplyKeyboardMarkup(
#         [['Отчет о проделанной работе'], ['Отчет об уборке рабочего места']],
#         resize_keyboard=True,
#     )
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='Здравствуйте! Пожалуйста, выберите тип отчета',
#         reply_markup=button,
#     )


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


# def image_encode(update: Update) -> bytes:
#     Path(f'media/temp/{update.message.chat.id}').mkdir(
#         parents=True, exist_ok=True
#     )
#     file = update.message.photo[-1].get_file()
#     file.download(f'media/temp/{update.message.chat.id}/downloaded_file.jpg')
#     with open(
#         f'media/temp/{update.message.chat.id}/downloaded_file.jpg', 'rb'
#     ) as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#         return encoded_string


# def work_image_handler(update: Update, context: CallbackContext) -> int:
#     encoded_string = image_encode(update)
#     context.user_data[WORK_IMAGE] = (
#         'data:image/png;base64,' + encoded_string.decode()
#     )

#     requests.post(settings.WORK_ENDPOINT, json=context.user_data)
#     button = ReplyKeyboardMarkup(
#         [['Отчет о проделанной работе'], ['Отчет об уборке рабочего места']],
#         resize_keyboard=True,
#     )
#     update.message.reply_text('Спасибо! Отчет отправлен!',
#                               reply_markup=button,)
#     return ConversationHandler.END


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


# def clean_image_handler(update: Update, context: CallbackContext) -> int:
#     encoded_string = image_encode(update)
#     context.user_data[CLEAN_IMAGE] = (
#         'data:image/png;base64,' + encoded_string.decode()
#     )

#     requests.post(settings.CLEAN_ENDPOINT, json=context.user_data)
#     button = ReplyKeyboardMarkup(
#         [['Отчет о проделанной работе'], ['Отчет об уборке рабочего места']],
#         resize_keyboard=True,
#     )
#     update.message.reply_text('Спасибо! Отчет отправлен!',
#                               reply_markup=button,)
#     return ConversationHandler.END


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

# clean_report_handler = ConversationHandler(
#     entry_points=[
#         MessageHandler(
#             Filters.text('Отчет об уборке рабочего места'),
#             clean_report,
#         ),
#     ],
#     states={
#         ORDER: [
#             MessageHandler(
#                 Filters.all,
#                 order_handler,
#             ),
#         ],
#         CLEAN_IMAGE: [
#             MessageHandler(
#                 Filters.all,
#                 clean_image_handler,
#             ),
#         ],
#     },
#     fallbacks=[
#         CommandHandler('cancel', cancel_handler),
#     ],
# )

# updater = (
#     Updater(token=settings.TELEGRAM_TOKEN)
# )
# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(work_report_handler)
# updater.dispatcher.add_handler(clean_report_handler)
