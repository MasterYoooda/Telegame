import telebot
import keyboards
import randomnumbers
import testimages
from telebot.types import Message

bot = telebot.TeleBot("1632459413:AAGpEtpehyUJoEvHWlOE6FHWLjl1Mj3_uq8")

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
    if c.data == 'mode_single':
        bot.send_message(
            c.message.chat.id,
            'Вы хотите ходить первым или вторым? Если хотите ходить первым - выберите крестики, вторым - нолики',
            reply_markup=keyboards.priority_keyboard
        )
    if c.data == 'cross':
        bot.send_photo(
            c.message.chat.id,
            photo = open('pol.jpg', 'rb'),
            caption = 'Выберете на клавиатуре, в какую клетку на поле поставить крестик',
            reply_markup=keyboards.game_keyboard
        )
    if c.data == 'one':
        testimages.cross(110,110)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
            reply_markup=keyboards.game_keyboard
        )
    if c.data == 'two':
        testimages.cross(320,110)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'three':
        testimages.cross(530,110)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'four':
        testimages.cross(110,320)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'five':
        testimages.cross(320,320)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'six':
        testimages.cross(530,320)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'seven':
        testimages.cross(110,530)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'eight':
        testimages.cross(320,530)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )
    if c.data == 'nine':
        testimages.cross(530,530)
        photo = open('pol2.jpg', 'rb')
        bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(photo)
        )

if __name__ == '__main__':
    bot.infinity_polling()
