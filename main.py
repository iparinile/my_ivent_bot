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
    bot.send_message(message.chat.id, 'Привет! Как тебя зовут?')
    db_comm.add_user(message.chat.id, cursor, db)
    db_comm.set_state(message.chat.id, 1, cursor, db)


@bot.message_handler(commands=["help"])
def help_user(message):
    bot.send_message(message.chat.id, 'Рассказать что я умею?\n'
                                      'Я могу помочь посмотреть доступные ивенты, зарегестрироваться на один из них, '
                                      'а также отметить свое присутствие.\n'
                                      'Для этого просто нажми /start и используй кнопки.')


keyboard_admin = telebot.types.ReplyKeyboardMarkup(True)
keyboard_admin.add('Добавить ивент')
keyboard_admin.add('Собрать статистику по ивентам')


@bot.message_handler(commands=["admin"])
def dad_in_the_building(message):
    db_comm.add_user(message.chat.id, cursor, db)
    db_comm.set_state(message.chat.id, 777, cursor, db)
    bot.send_message(message.chat.id, 'Оу, да у нас dad in the building!\n'
                                      'Ниже появятся кнопки управления мной.', reply_markup=keyboard_admin)


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
        bot.send_message(message.chat.id, "Выбери ивент", reply_markup=keyboard1)
    elif db_comm.get_state(message.chat.id, cursor) == 1:
        db_comm.set_state(message.chat.id, 2, cursor, db)
        db_comm.insert_name_of_user(message.chat.id, message.text, cursor, db)
        bot.send_message(message.chat.id, 'Отлично!', reply_markup=keyboard)
    elif message.text == 'Отметить присутствие на ивенте':
        if db_comm.get_state_from_main(message.chat.id, cursor) == 1:
            keyboard2 = telebot.types.InlineKeyboardMarkup()
            events = db_comm.get_event_list_from_main(message.chat.id, cursor)
            for event in events:
                keyboard2.add(telebot.types.InlineKeyboardButton(text=event[0], callback_data=f'b%{event[1]}'))
            bot.send_message(message.chat.id, "Выбери ивент", reply_markup=keyboard2)
        else:
            bot.send_message(message.chat.id, 'Ты не зарегестрирован(а) ни на одно мероприятие. Для начала сделай это.')
    elif message.text == 'Добавить ивент' and db_comm.get_state(message.chat.id, cursor) == 777:
        bot.send_message(message.chat.id, 'Хорошо, введи имя ивента.')
        db_comm.set_state(message.chat.id, 778, cursor, db)
    elif db_comm.get_state(message.chat.id, cursor) == 778:
        db_comm.add_event(message.text, cursor, db)
        db_comm.set_state(message.chat.id, 777, cursor, db)
        bot.send_message(message.chat.id, 'Ты успешно добавил(а) ивент!')
    elif message.text == 'Собрать статистику по ивентам' and db_comm.get_state(message.chat.id, cursor) == 777:
        stat = telebot.types.InlineKeyboardMarkup()
        events = db_comm.get_event_list(cursor)
        for event in events:
            stat.add(telebot.types.InlineKeyboardButton(text=event[1], callback_data=f'c%{event[0]}'))
        bot.send_message(message.chat.id, 'Выберите ивент, по которому вывести статистику', reply_markup=stat)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю((( Попробуй /start или /help')


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    if call.data.split('%')[0] == "a":
        if db_comm.something(call.message.chat.id, call.data.split('%')[1], cursor) is None:
            db_comm.add_user_to_main(call.message.chat.id, call.data.split('%')[1], cursor, db)
            bot.send_message(call.message.chat.id, 'Отлично! Ты зарегестрировался(ась) на ивент.')
        else:
            bot.send_message(call.message.chat.id, 'Сори, но вы уже зарегестрировались на это мероприятие!')
    elif call.data.split('%')[0] == "b":
        db_comm.check_in(call.message.chat.id, call.data.split('%')[1], cursor, db)
        bot.send_message(call.message.chat.id, 'Оу, да ты целеустремленный, офигеть, пришел на event! Ну хорошо,'
                                               'я тебя отметил, развлекайся!')
    elif call.data.split('%')[0] == "c":
        a = db_comm.get_event_to_statistics(call.data.split('%')[1], cursor)
        come = 0
        not_come = 0
        for i in range(len(a)):
            if a[i][0] == 1:
                not_come += 1
            else:
                come += 1
        bot.send_message(call.message.chat.id, 'На мероприятие ' + db_comm.get_name_event(call.data.split('%')[1],
                                                                                          cursor) + '\n' +
                         'Записалось - ' + str(not_come) + '\n'
                         'Пришло - ' + str(come))


bot.polling()
