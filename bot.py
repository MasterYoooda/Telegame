import telebot

bot = telebot.TeleBot("1632459413:AAGpEtpehyUJoEvHWlOE6FHWLjl1Mj3_uq8")

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привет!\n'+
        'В будущем тут что-то появится\n'+ '\n'
        'А может и нет 😈\n'
    )

if __name__ == '__main__':
    bot.infinity_polling()
