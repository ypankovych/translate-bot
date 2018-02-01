import os

import requests
import telebot

bot = telebot.TeleBot(os.environ.get('token'))
make_gist = 'https://api.github.com/gists'
input_data = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,./<>?@#$^&{}:"QWERTYUIOPASDFGHJKLZXCVBNM'
output_data = 'йцукенгшщзхъфывапролджэячсмитьбю.БЮ,"№;:?ХЪЖЭЙЦУКЕНГШЩЗФЫВАПРОЛДЯЧСМИТЬ'
trans = str.maketrans(input_data, output_data)


@bot.message_handler(commands=['paste'])
def create_gist(message):
    if message.reply_to_message and message.reply_to_message.text:
        payload = {
            "description": f"From {message.reply_to_message.from_user.first_name}",
            "public": 'true',
            "files": {
                "file1.py": {
                    "content": message.reply_to_message.text
                }
            }
        }
        gist = requests.post(make_gist, json=payload, timeout=1000).json()
        bot.reply_to(message.reply_to_message, text=gist['html_url'])


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Add to group',
                                                  url='t.me/correctmebot?startgroup=on'))
    bot.send_message(chat_id=message.chat.id,
                     text='Add me to your group and promote to admin.\nTo call me just type /wat',
                     reply_markup=markup)


@bot.message_handler(content_types=['text', 'video', 'photo', 'document'], commands=['wat'])
def text_handle(message):
    if message.reply_to_message:
        response_text = getattr(message.reply_to_message, 'text') or getattr(message.reply_to_message, 'caption')
        if response_text and any([x in input_data for x in response_text]):
            bot.reply_to(message.reply_to_message, text=response_text.translate(trans))


if __name__ == '__main__':
    bot.polling(none_stop=True)
