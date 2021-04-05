import telebot
import keyboards
import testimages
import gametest
import os
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
    point_positions = {
        'one' : (110,110),
        'two' : (320,110),
        'three' : (530, 100),
        'four' : (110,320),
        'five' : (320,320),
        'six' : (530,320),
        'seven' : (110,530),
        'eight' : (320,530),
        'nine' : (530,530)
    }

    if (c.data in point_positions):
        #<- похоже надо дописать функцию перевода текстового ключа в индекс клетки
        is_wrong = gametest.player_turn(list(point_positions.keys()).index(c.data), 'X')
        #  все хорошо когда никаких ошибок не вернулось
        if (not is_wrong):
            testimages.cross(point_positions[c.data])            

            #  пришлось вынести вторую проверку для 9-го хода крестика
            is_victory = gametest.win_check()
            if (not is_victory):
                bot_move = gametest.bot_turn(list(point_positions.keys()), 'O')
                testimages.circle(point_positions[bot_move])

            is_victory = gametest.win_check()
            if (not is_victory):

                photo = open('pol2.jpg', 'rb')
                bot.edit_message_media(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    media=telebot.types.InputMediaPhoto(photo),
                    reply_markup=keyboards.game_keyboard)
            else:
                #  если это победа, а не ничья
                if ("Победил" in is_victory):
                    testimages.winline(320,25,320,615)

                photo = open('pol2.jpg', 'rb')
                bot.edit_message_media(
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id,
                    media=telebot.types.InputMediaPhoto(photo))
                bot.send_message(c.message.chat.id,
                                is_victory)

                os.remove("pol2.jpg")
                os.remove("game_data.txt")
        else: 
            bot.send_message(   #<- заменить на что-то более красивое
                c.message.chat.id,
                'Ячейка занята')    
    else:
        if c.data == 'mode_single':
            bot.send_message(
                c.message.chat.id,
                'Вы хотите ходить первым или вторым? Если хотите ходить первым - выберите крестики, вторым - нолики',
                reply_markup=keyboards.priority_keyboard
            )            
        if c.data == 'cross':
            gametest.game_manager()
            bot.send_photo(
                c.message.chat.id,
                photo = open('pol.jpg', 'rb'),
                caption = 'Выберете на клавиатуре, в какую клетку на поле поставить крестик',
                reply_markup=keyboards.game_keyboard
            )
   

if __name__ == '__main__':
    bot.infinity_polling()