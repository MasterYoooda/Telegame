import telebot
import keyboards
import gamemanager
import telegramBotToken
from telebot.types import Message


bot = telebot.TeleBot(telegramBotToken.token)


@bot.message_handler(commands=['start'])
def StartCommand(message):
    bot.send_message(
        message.chat.id,
        'Привет!\n'+
        'В будущем тут что-то появится\n'+ '\n'
        'А может и нет 😈\n' + '\n'
        'Нажми "/newgame" и не еби себе мозг'
    )


@bot.message_handler(commands=['newgame'])
def Newgame(message):
    bot.send_message(
        message.chat.id,
        'Выберете режим игры:  ',
        reply_markup=keyboards.start_keyboard
    )
    

@bot.callback_query_handler(func=lambda c:True)
def inline(c):

    if (c.data in gamemanager.point_positions):
        gamemanager.move_made(c)
            
    else:
        if c.data == 'mode_single':
            gamemanager.mode_defined(c, c.data)           
        if c.data == 'cross':
            gamemanager.character_defined(c, 'X')


def message_send(c, text, keyboard = False):
    bot.send_message(c.message.chat.id, text, reply_markup=keyboard)


def photo_send(c):
    bot.send_photo(
        c.message.chat.id,
        photo = open('pol.jpg', 'rb'),
        caption = 'Выберете на клавиатуре, в какую клетку на поле поставить крестик',
        reply_markup=keyboards.game_keyboard
    )


def message_edit(c, keyboard = keyboards.game_keyboard):
    bot.edit_message_media(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        media=telebot.types.InputMediaPhoto(open('pol2.jpg', 'rb')),
        reply_markup=keyboard)
   

if __name__ == '__main__':
    bot.infinity_polling()