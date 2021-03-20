import telebot
import gametest


bot = telebot.TeleBot("1632459413:AAGpEtpehyUJoEvHWlOE6FHWLjl1Mj3_uq8")
user_Id = 0
isGameStart = False


@bot.message_handler(content_types=['text'])
def GetTextMessages(message, event = None):
    if (event == 'cell_number'):
        bot.register_next_step_handler(message, lambda message: GetPlayerTurn(message))

    if message.text == "sq" and not isGameStart:        
        global user_Id
        user_Id = message.from_user.id
        SendMessage("Сообщение получено")
        gametest.GameManager()


@bot.message_handler(commands=['start'])
def StartCommand(message):
    bot.send_message(
        message.chat.id,
        'Привет!\n'+
        'В будущем тут что-то появится\n'+ '\n'
        'А может и нет 😈\n'
    )


def GetPlayerTurn(message):
    player_input = -1
    while player_input == -1:
        if (message.text.isdigit() and int(message.text) < 10 and int(message.text) > 0):
            player_input = int(message.text)
        else:
            SendMessage("Не число")
            GetTextMessages(message, 'cell_number')
    return player_input


def SendMessage(text):
    bot.send_message(user_Id, text)


if __name__ == '__main__':
    bot.infinity_polling()
