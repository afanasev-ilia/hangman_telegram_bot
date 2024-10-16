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

from main import display_hangman, get_word, is_repeat, is_valid_input

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
        one_time_keyboard=True,
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
    repeated_letters = []
    # guessed_words = []
    context.user_data[TRIES] = 6

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" ".join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком\n'
                f'{context.user_data[WORD]}'
            ),
        )
    return PLAY


def play(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.upper()
    word = context.user_data[WORD]
    word_completion = context.user_data[WORD_COMPLETION]
    tries = context.user_data[TRIES]

    if not is_valid_input(user_input):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Допустимы только буквы русского алфавита!',
        )
        return PLAY

    if tries == 1:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES] - 1)}\n'
                'Вы проиграли!\n'
                f'Правильный ответ {word}'
            ),
        )
        return ConversationHandler.END

    if len(user_input) == 1:
        count = 0
        for cur in range(len(word)):
            if word[cur] == user_input:
                word_completion[cur] = user_input
                count += 1
        if count == 0:
            tries -= 1
            context.user_data[TRIES] = tries
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Неверно!',
            )
        elif ''.join(word_completion) == word:
            context.user_data[WORD_COMPLETION] = word_completion
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Поздравляем, вы угадали слово! Вы победили!',
            )
            return ConversationHandler.END
        else:
            context.user_data[WORD_COMPLETION] = word_completion
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Поздравляем, вы угадали букву!',
            )
    else:
        if user_input == word:
            context.user_data[WORD_COMPLETION] = list(word)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Поздравляем, вы угадали слово! Вы победили!',
            )
            return ConversationHandler.END
        else:
            tries -= 1
            context.user_data[TRIES] = tries
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Неверно!',
            )

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f'{display_hangman(context.user_data[TRIES])}\n'
                f'{" ".join(context.user_data[WORD_COMPLETION])}\n\n'
                'Введите символ или слово целиком\n'
                f'{context.user_data[WORD]}'
            ),
        )

    return PLAY


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
