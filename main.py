import os
import telebot

bot = telebot.TeleBot(os.environ.get('token'))
input_data = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,./:`@#$^&"'
output_data = 'йцукенгшщзхъфывапролджэячсмитьбю.жё"№;:?э'
trans = str.maketrans(input_data + input_data.upper(), output_data + output_data.upper())


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='hello')


@bot.message_handler(content_types=['text', 'video', 'photo', 'document'])
def text_handle(message):
    if message.reply_to_message and message.text.strip() == '/wat':
        response_text = getattr(message.reply_to_message, 'text') or getattr(message.reply_to_message, 'caption')
        if response_text and any([x in input_data for x in response_text.lower()]):
            bot.reply_to(message.reply_to_message, text=response_text.translate(trans))


if __name__ == '__main__':
    bot.polling(none_stop=True)
