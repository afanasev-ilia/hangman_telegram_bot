# Hangman Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22.0-blue)](https://github.com/python-telegram-bot/python-telegram-bot?tab=readme-ov-file)

Telegram-бот для игры в "Виселицу" (Hangman). Бот позволяет пользователям угадывать слова, вводя буквы или целые слова. Игра поддерживает русский алфавит и предоставляет визуальное отображение текущего состояния игры.

## Как играть

1. **Запустите бота командой `/start`.**
2. **Нажмите на кнопку "Начать игру".**
3. **Вводите буквы или слова, чтобы угадать загаданное слово.**
4. **У вас есть 7 попыток, чтобы угадать слово. После каждой неудачной попытки отображается текущее состояние виселицы.**
5. **Если вы угадаете слово, бот предложит сыграть ещё раз.**

## Примеры использования

### Запуск бота

1. **Запустите бота командой `/start`:**
   - Бот приветствует вас и предлагает начать игру.
   - Пример сообщения:
     ```
     Здравствуйте, [Ваше имя]! Давайте играть в угадайку слов!
     ```

2. **Нажмите на кнопку "Начать игру":**
   - Бот загадывает слово и показывает текущее состояние игры.
   - Пример сообщения:
     ```
     --------
     |      |
     |      
     |    
     |      
     |     
     -
     
     _ _ _ _ _
     
     Введите символ или слово целиком
     ```

### Игровой процесс

1. **Ввод буквы:**
   - Если буква есть в слове, бот покажет её позицию.
   - Пример:
     ```
     Поздравляем, вы угадали букву!
     
     --------
     |      |
     |      
     |    
     |      
     |     
     -
     
     _ А _ _ _
     
     Введите символ или слово целиком
     ```

2. **Ввод слова целиком:**
   - Если слово угадано верно, бот поздравляет с победой.
   - Пример:
     ```
     Поздравляю, вы угадали слово! Продолжим игру?
     ```

3. **Неверный ввод:**
   - Если буква или слово неверны, бот уменьшает количество попыток.
   - Пример:
     ```
     Неверно!
     
     --------
     |      |
     |      O
     |    
     |      
     |     
     -
     
     _ _ _ _ _
     
     Введите символ или слово целиком
     ```

4. **Конец игры:**
   - Если попытки закончились, бот сообщает о проигрыше и предлагает сыграть ещё раз.
   - Пример:
     ```
     --------
     |      |
     |      O
     |     \|/
     |      |
     |     / \
     -
     
     Вы проиграли!
     Правильный ответ: СЛОВО
     Хотите сыграть ещё?
     ```

### Завершение игры

1. **Завершение игры:**
   - Вы можете завершить игру в любой момент, нажав на кнопку "Завершить игру" или отправив команду `/cancel`.
   - Пример сообщения:
     ```
     Спасибо, что играли в нашу игру! До встречи!
     ```

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/yourusername/hangman-telegram-bot.git
   cd hangman-telegram-bot
   ```

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Создайте файл `.env` и добавьте ваш Telegram токен:**
   ```plaintext
   TELEGRAM_TOKEN=your_telegram_bot_token
   ```

4. **Запустите бота:**
   ```bash
   python bot.py
   ```

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## Автор

Илья Афанасьев
