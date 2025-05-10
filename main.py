import telebot
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я автоэксперт-бот. Задай мне вопрос про машины — например, 'что такое радиатор?'"
    )

@bot.message_handler(func=lambda message: True)
def handle_question(message):
    chat_id = message.chat.id
    user_question = message.text

    prompt = (
        f"Ты опытный автоэксперт. Объясни, что такое '{user_question}' — просто, чётко, без лишней информации. "
        f"Если вопрос общий — дай полезный ответ. Не говори про базы данных или ошибки двигателя, если это не в тему. "
        f"Говори на том же языке, что и вопрос."
    )

    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=300,
            temperature=0.6
        )

        gpt_answer = response.choices[0].text.strip()
        bot.send_message(chat_id, gpt_answer)

    except Exception as e:
        print("Ошибка:", e)
        bot.send_message(chat_id, "Произошла ошибка. Проверь API ключ и попробуй снова.")

bot.polling()
