import telebot
from telebot import types
import os
import sys

API_TOKEN = '7994265996:AAG509D3Srpg607KEAa7BnMb0NJdzldkBbQ'
bot = telebot.TeleBot(API_TOKEN)

CHANNEL_ID = '@printhelloMoscow'

SCENARIOS = {
    'scenario_1': 'file1.docx',
    'scenario_2': 'file2.docx',
    'scenario_3': 'file3.docx',
    'scenario_4': 'file4.docx',
    'scenario_5': 'file5.docx',
}

LINKS_TO_SCENARIOS = {
    'link1': 'scenario_1',
    'link2': 'scenario_2',
    'link3': 'scenario_3',
    'link4': 'scenario_4',
    'link5': 'scenario_5',
}

@bot.message_handler(commands=['start'])
def start(message):
    ref = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    if ref in LINKS_TO_SCENARIOS:
        scenario = LINKS_TO_SCENARIOS[ref]
        bot.send_message(
            message.chat.id,
            f"Привет! Чтобы получить доступ к материалам, подпишитесь на наш канал {CHANNEL_ID}."
        )
        send_subscription_check_button(message.chat.id, scenario)
    else:
        bot.send_message(message.chat.id, "Неверная ссылка или сценарий не найден.")

def send_subscription_check_button(chat_id, scenario):
    markup = types.InlineKeyboardMarkup()
    check_button = types.InlineKeyboardButton(
        text="Проверить подписку на канал",
        callback_data=f"check_subscription:{scenario}"
    )
    markup.add(check_button)
    bot.send_message(chat_id, "Подпишитесь на канал и нажмите кнопку ниже:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('check_subscription'))
def check_subscription(call):
    scenario = call.data.split(':')[1]
    user_status = bot.get_chat_member(CHANNEL_ID, call.from_user.id).status
    if user_status in ['member', 'administrator', 'creator']:
        send_file(call.message.chat.id, scenario)
    else:
        bot.send_message(
            call.message.chat.id,
            f"Вы не подписаны на канал {CHANNEL_ID}. Подпишитесь, чтобы продолжить."
        )

def send_file(chat_id, scenario):
    file_path = SCENARIOS.get(scenario)
    if file_path:
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
        send_restart_button(chat_id, scenario)
    else:
        bot.send_message(chat_id, "Файл не найден. Обратитесь к администратору.")

def send_restart_button(chat_id, scenario):
    markup = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton(
        text="Перезапустить бота",
        callback_data=f"restart_scenario:{scenario}"
    )
    markup.add(restart_button)
    bot.send_message(chat_id, "Спасибо за использование нашего бота! Хотите перезапустить его?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('restart_scenario'))
def restart_scenario(call):
    scenario = call.data.split(':')[1]
    bot.send_message(
        call.message.chat.id,
        f"Для получения материалов снова подпишитесь на канал {CHANNEL_ID}."
    )
    send_subscription_check_button(call.message.chat.id, scenario)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()