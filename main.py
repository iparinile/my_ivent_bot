import sqlite3
import telebot
import db_comm

bot = telebot.TeleBot('989390225:AAGSd5U8U4fusOyqZWw2lFukhN7YoGDpqqA')
db = sqlite3.connect('mydata.sqlite', check_same_thread=False)
cursor = db.cursor()

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.add('Показать список ивентов')
keyboard.add('Зарегестрироваться на ивенте')
keyboard.add('Отметить присутствие на ивенте')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Что ты хочешь?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Показать список ивентов':
        events = db_comm.get_event_list(cursor)
        mess = ''
        for event in events:
            mess += f'{event[0]} - {event[1]}\n'
        bot.send_message(message.chat.id, mess, reply_markup=keyboard)
    elif message.text == 'Зарегестрироваться на ивенте':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        events = db_comm.get_event_list(cursor)
        for event in events:
            keyboard1.add(telebot.types.InlineKeyboardButton(text=event[1], callback_data=f'a%{event[0]}'))
            print(event[1])
        bot.send_message(message.chat.id, "Выберите ивент", reply_markup=keyboard1)
    elif db_comm.get_state(message.chat.id, cursor) == 1:
        db_comm.set_state(message.chat.id, 2, cursor, db)
        db_comm.insert_name_of_user(message.chat.id, message.text, cursor, db)
        bot.send_message(message.chat.id, "Ты крут! Почему? Бот работает, тебя зовут " + message.text +
                         " и ты записался на event " + db_comm.get_name_event_from_user(message.chat.id, cursor) +
                         "! " + "Когда придешь на мероприятие, не забудь отметиться у меня.")
    elif message.text == 'Отметить присутствие на ивенте':
        if db_comm.get_state(message.chat.id, cursor) == 2:
            db_comm.set_state(message.chat.id, 3, cursor, db)
            bot.send_message(message.chat.id, 'Оу, да ты я смотрю целеустремленный. Взял и пришел на event ' +
                             db_comm.get_name_event_from_user(message.chat.id, cursor) +
                             ' Ну все, я отметил твое присутствие.')
        else:
            bot.send_message(message.chat.id, 'Ты не зарегестрирован ни на одно мероприятие. Для начала сделай это.')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю((( Попробуй /start или /help')


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    if call.data.split('%')[0] == "a":
        db_comm.insert_consent(call.message.chat.id, call.data.split('%')[1], cursor, db)
        db_comm.insert_name_event(call.data.split('%')[1], cursor, db)
        db_comm.set_state(call.message.chat.id, 1, cursor, db)
        bot.send_message(call.message.chat.id, 'Отлично! Ты зарегестрировался на ивент '
                         + db_comm.get_name_event_from_user(call.message.chat.id, cursor) + '.' +
                         ' Теперь напиши свое имя')


bot.polling()
