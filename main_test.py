import telebot

bot = telebot.TeleBot('989390225:AAGSd5U8U4fusOyqZWw2lFukhN7YoGDpqqA')


@bot.message_handler(content_types=['text'])
def text(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, 'ну круто')


bot.polling()
