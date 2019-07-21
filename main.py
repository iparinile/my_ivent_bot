import data
import config
import telebot

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = data.get_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id,
                         "Кажется, кто-то обещал отправить своё имя, но так и не сделал этого :( Жду...")
    elif state == config.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id,
                         "Кажется, кто-то обещал отправить свой возраст, но так и не сделал этого :( Жду...")
    elif state == config.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id,
                         "Кажется, кто-то обещал отправить картинку, но так и не сделал этого :( Жду...")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, "Привет! Как я могу к тебе обращаться?")
        data.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Что ж, начнём по-новой. Как тебя зовут?")
    data.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(func=lambda message: data.get_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    bot.send_message(message.chat.id, "Отличное имя, запомню! Теперь укажи, пожалуйста, свой возраст.")
    data.set_state(message.chat.id, config.States.S_ENTER_AGE.value)


@bot.message_handler(func=lambda message: data.get_state(message.chat.id) == config.States.S_ENTER_AGE.value)
def user_entering_age(message):
    # А вот тут сделаем проверку
    if not message.text.isdigit():
        # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
        bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
        return
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "Какой-то странный возраст. Не верю! Отвечай честно.")
        return
    else:
        # Возраст введён корректно, можно идти дальше
        bot.send_message(message.chat.id, "Когда-то и мне было столько лет...эх... Впрочем, не будем отвлекаться. "
                                          "Отправь мне какую-нибудь фотографию.")
        data.set_state(message.chat.id, config.States.S_SEND_PIC.value)


@bot.message_handler(content_types=["photo"],
                     func=lambda message: data.get_state(message.chat.id) == config.States.S_SEND_PIC.value)
def user_sending_photo(message):
    # То, что это фотография, мы уже проверили в хэндлере, никаких дополнительных действий не нужно.
    bot.send_message(message.chat.id, "Отлично! Больше от тебя ничего не требуется. Если захочешь пообщаться снова - "
                     "отправь команду /start.")
    data.set_state(message.chat.id, config.States.S_START.value)


if __name__ == "__main__":
    bot.polling(none_stop=True)
