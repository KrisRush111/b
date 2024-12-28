import openai
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

# Настройка Flask
app = Flask(__name__)

# Настройка ключей
openai.api_key = "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"  # Замените на ваш OpenAI API ключ
TELEGRAM_BOT_TOKEN = "7733946360:AAHqUY5clqyxkHT10rDc8lB7ssoDQzHhj4k"  # Замените на ваш Telegram Bot Token

# Настройка приложения Telegram-бота
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Функция для генерации Python-кода через OpenAI
def generate_python_code(task_description):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Или "gpt-4" для лучшего результата
            messages=[
                {"role": "system", "content": "Ты помощник, который пишет Python-код."},
                {"role": "user", "content": f"Напиши Python-код для следующей задачи: {task_description}"}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        # Возвращаем сгенерированный код
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при генерации кода: {e}"

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Я бот, который может решать задачи и писать Python-код. Опиши свою задачу, и я попробую помочь!"
    )

# Обработчик сообщений с задачами
async def respond(update: Update, context):
    user_input = update.message.text

    # Генерация кода на Python
    bot_reply = generate_python_code(user_input)
    await update.message.reply_text(f"Вот сгенерированный код для вашей задачи:\n\n{bot_reply}")

# Настройка Flask вебхука
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

if __name__ == "__main__":
    # Установка вебхука для Telegram
    webhook_url = f"https://<your-server-url>/{TELEGRAM_BOT_TOKEN}"  # Замените <your-server-url> на ваш URL
    application.bot.set_webhook(url=webhook_url)

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Запуск Flask-сервера
    app.run(port=5000)
