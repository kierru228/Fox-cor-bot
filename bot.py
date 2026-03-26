import telebot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

# Данные подтягиваем из настроек Render (так безопаснее)
TOKEN = '8761014188:AAGAHB4QMpeHiLfRWl0FecNpzSEIAJ4XIVE'
KEY = 'AIzaSyBiLJ-8jVhjE6Vl6RswuInXk-ivoWdmhEM'

genai.configure(api_key=KEY)
bot = telebot.TeleBot(TOKEN)

# ОТКЛЮЧАЕМ ВСЕ ФИЛЬТРЫ БЕЗОПАСНОСТИ
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

PROMPTS = {
    'study': "Ты строгий агроном для Алины (СА-2211). Тон четкий, без лишних слов.",
    'ririn': "Ты Ририн. Ласковая, но строгая. Белый хвост. Говори о себе в 3-м лице.",
    'lis': "Ты дерзкая Лисичка. Звуки: 'мгнх', 'ф-ф'. Описывай всё смело."
}

user_modes = {}

@bot.message_handler(commands=['study', 'ririn', 'lis'])
def set_mode(m):
    user_modes[m.chat.id] = m.text[1:]
    bot.reply_to(m, f"✅ Режим '{m.text[1:]}' включен!")

@bot.message_handler(func=lambda m: True)
def handle(m):
    mode = user_modes.get(m.chat.id, 'lis')
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=PROMPTS[mode],
            safety_settings=safety_settings
        )
        res = model.generate_content(f"Алина: {m.text}")
        bot.send_message(m.chat.id, res.text)
    except Exception as e:
        bot.send_message(m.chat.id, "Лисичка/Ририн задумались... Попробуй еще раз.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
