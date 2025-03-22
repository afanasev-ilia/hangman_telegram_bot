import os
import logging

from dotenv import load_dotenv
from pathlib import Path
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from hangman_utils import display_hangman, get_word, is_repeat, is_valid_input

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

(
    WORD,
    WORD_COMPLETION,
    TRIES,
    PLAY,
    REPEATED_LETTERS,
    REPEATED_WORDS,
    GUESSED,
) = range(7)


async def wake_up(update: Update, context: CallbackContext) -> int:
    button = ReplyKeyboardMarkup(
        [['Начать игру'],],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    name = update.message.chat.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте, {}!\nДавайте играть в угадайку слов!'.format(name),
        reply_markup=button,
    )


async def start_game(update: Update, context: CallbackContext) -> int:
    context.user_data[WORD] = get_word()
    context.user_data[WORD_COMPLETION] = [
        '_' for _ in range(len(context.user_data[WORD]))
    ]
    context.user_data[REPEATED_LETTERS] = []
    context.user_data[REPEATED_WORDS] = []
    context.user_data[TRIES] = 7
    context.user_data[GUESSED] = False

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" " .join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком\n'
                f'{context.user_data[WORD]}'
            ),
        )
    return PLAY


async def play(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.upper()
    word = context.user_data[WORD]
    word_completion = context.user_data[WORD_COMPLETION]
    tries = context.user_data[TRIES]
    repeated_letters = context.user_data[REPEATED_LETTERS]
    repeated_words = context.user_data[REPEATED_WORDS]

    if not is_valid_input(user_input):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Допустимы только буквы русского алфавита!',
        )
        return PLAY

    if tries == 1:
        button = ReplyKeyboardMarkup(
            [['Начать игру'],],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES] - 1)}\n'
                'Вы проиграли!\n'
                f'Правильный ответ {word}\n'
                'Хотите сыграть ещё?'
            ),
            reply_markup=button,
        )
        return ConversationHandler.END

    if len(user_input) == 1:
        if is_repeat(user_input, repeated_letters, repeated_words):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы уже вводили букву "{}"!'.format(user_input),
            )
            return PLAY
        repeated_letters.append(user_input)
        context.user_data[REPEATED_LETTERS] = repeated_letters
        count = 0
        for cur in range(len(word)):
            if word[cur] == user_input:
                word_completion[cur] = user_input
                count += 1
        if count == 0:
            tries -= 1
            context.user_data[TRIES] = tries
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Буквы "{}" нет в этом слове!'.format(user_input),
            )
        elif ''.join(word_completion) == word:
            context.user_data[WORD_COMPLETION] = word_completion
            button = ReplyKeyboardMarkup(
                [['Начать игру'],],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    '🎉 Поздравляю, Вы угадали слово! 🎉\n'
                    'Продолжим игру?'
                ),
                reply_markup=button,
            )
            return ConversationHandler.END
        else:
            context.user_data[WORD_COMPLETION] = word_completion
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Поздравляем, вы угадали букву!',
            )
    else:
        if is_repeat(user_input, repeated_letters, repeated_words):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы уже вводили это слово!',
            )
            return PLAY

        if len(user_input) != len(word):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Длина слова должна быть {len(word)} букв!',
            )
            return PLAY

        repeated_words.append(user_input)
        context.user_data[REPEATED_WORDS] = repeated_words

        if user_input == word:
            context.user_data[WORD_COMPLETION] = list(word)
            button = ReplyKeyboardMarkup(
                [['Начать игру'],],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    '🎉 Поздравляю, Вы угадали слово! 🎉\n'
                    'Продолжим игру?'
                ),
                reply_markup=button,
            )
            return ConversationHandler.END
        else:
            tries -= 1
            context.user_data[TRIES] = tries
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='❌ Увы, это неверное слово!',
            )

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" ".join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком\n'
                f'{context.user_data[WORD]}'
            ),
        )

    return PLAY


async def cancel_handler(
        update: Update,
        context: CallbackContext
) -> int:
    await update.message.reply_text('Спасибо, что играли в нашу игру!\nДо встречи!')
    return ConversationHandler.END


# play_handler = ConversationHandler(
#     entry_points=[
#         MessageHandler(
#             filters.Regex('Начать игру'),
#             start_game,
#         ),
#     ],
#     states={
#         PLAY: [
#             MessageHandler(
#                 filters.TEXT & ~filters.COMMAND,
#                 play,
#             ),
#             CommandHandler('cancel', cancel_handler),
#         ],
#     },
#     fallbacks=[
#         CommandHandler('cancel', cancel_handler),
#     ],
# )


# updater = (
#     Updater(token=TELEGRAM_TOKEN)
# )
# updater.dispatcher.add_handler(CommandHandler('start', wake_up))
# updater.dispatcher.add_handler(play_handler)
# updater.start_polling()
# updater.idle()

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    play_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex('Начать игру'),
                start_game,
            ),
        ],
        states={
            PLAY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    play,
                ),
                CommandHandler('cancel', cancel_handler),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start", start)],
    #     states={
    #         GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
    #         PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
    #         LOCATION: [
    #             MessageHandler(filters.LOCATION, location),
    #             CommandHandler("skip", skip_location),
    #         ],
    #         BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )

    application.add_handler(CommandHandler('start', wake_up))
    application.add_handler(play_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
