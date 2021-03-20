import telebot
import keyboards
import randomnumbers
from telebot.types import Message

bot = telebot.TeleBot("1632459413:AAGpEtpehyUJoEvHWlOE6FHWLjl1Mj3_uq8")

@bot.message_handler(commands=['start'])
def StartCommand(message):
    bot.send_message(
        message.chat.id,
        'Привет!\n'+
        'В будущем тут что-то появится\n'+ '\n'
        'А может и нет 😈\n'
        'Нажми "/newgame" и не еби себе мозг'
    )

@bot.message_handler(commands=['newgame'])
def Newgame(message):
    bot.send_message(
        message.chat.id,
        'Выберете режим игры:',
        reply_markup=keyboards.start_keyboard
    )
def Singlemode(message):
    pass


@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    if c.data == 'mode_single':
        bot.send_message(
            c.message.chat.id,
            text = str(randomnumbers.randomnumbers())+'\n'+'Ваш ход:',
            reply_markup=keyboards.game_keyboard
        )
        
        


if __name__ == '__main__':
    bot.infinity_polling()
