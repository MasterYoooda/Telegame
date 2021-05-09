import os
import botfunc
import keyboards
import gamefunc
import testimages


class GameExceptions(Exception):
    def __init__(self, text):
        self.text = text


point_positions = {
        '0' : (110,110),
        '1' : (320,110),
        '2' : (530, 100),
        '3' : (110,320),
        '4' : (320,320),
        '5' : (530,320),
        '6' : (110,530),
        '7' : (320,530),
        '8' : (530,530)
}


def mode_defined(c, mode):
    #gamemode = mode
    botfunc.game.game_mode = mode
    botfunc.message_send(
        c,
        'Выберите, за кого хотите играть',
        keyboard=keyboards.priority_keyboard) 


def character_defined(c, token):
    #gamefunc.start_game()

    #  very ugly code :'(
    botfunc.game.players_list[token] = gamefunc.Player(c, token)
    if (botfunc.game.game_mode == 'mode_single'):
        botfunc.game.players_list['XO'.replace(token,'')] = gamefunc.GameBot('XO'.replace(token,''))
    botfunc.game.startGame()

    botfunc.photo_send(c)


def getCharacter(c):
    pl_list = botfunc.game.players_list
    return 'X' if pl_list['X'].token != 0 and pl_list['X'].token.message.chat.id == c.message.chat.id else 'O'


def move_made(c):
    try:
        botfunc.game.playerTurn(int(c.data), getCharacter(c))
    except GameExceptions as g_exc:
        botfunc.message_send(c, g_exc)
    else:
        if (getCharacter(c) == 'X'):
            testimages.cross(botfunc.game.field.point_positions[c.data])
        else:
            testimages.circle(botfunc.game.field.point_positions[c.data])

        is_victory = gamefunc.win_check()
        if (not is_victory):
            bot_char = 'XO'.replace(getCharacter(c), '')
            botfunc_move = botfunc.game.botTurn(bot_char)
            if (bot_char == 'O'):
                testimages.circle(point_positions[botfunc_move])
            else:
                testimages.cross(botfunc.game.field.point_positions[botfunc_move])

        is_victory = gamefunc.win_check()
        if (not is_victory):
            botfunc.message_edit(c)
        else:
            #  если это победа, а не ничья
            #if ("Победил" in is_victory):
            #    testimages.winline(320,25,320,615)

            botfunc.message_edit(c, keyboard = False)
            botfunc.message_send(c, is_victory)

            os.remove("pol2.jpg")
            #os.remove("game_data.txt")


    '''#<- похоже надо дописать функцию перевода текстового ключа в индекс клетки
    is_wrong = gamefunc.player_turn(list(point_positions.keys()).index(c.data), 'X')
    #  все хорошо когда никаких ошибок не вернулось
    if (not is_wrong):
        testimages.cross(point_positions[c.data])            

        #  пришлось вынести вторую проверку для 9-го хода крестика
        is_victory = gamefunc.win_check()
        if (not is_victory):
            botfunc_move = gamefunc.bot_turn(list(point_positions.keys()), 'O')
            testimages.circle(point_positions[botfunc_move])

        is_victory = gamefunc.win_check()
        if (not is_victory):
            botfunc.message_edit(c)
        else:
            #  если это победа, а не ничья
            if ("Победил" in is_victory):
                testimages.winline(320,25,320,615)

            botfunc.message_edit(c, keyboard = False)
            botfunc.message_send(c, is_victory)

            os.remove("pol2.jpg")
            os.remove("game_data.txt")
    else: 
        botfunc.message_send(c, 'Ячейка занята')   #<- заменить на что-то более красивое '''


def file_manager(op, data = 0):
    if (op == "write"):
        file = open("game_data.txt", 'w')

        for d in data:
            file.write(str(d) + " ")

        file.close()

    if (op == "read"):
        file = open("game_data.txt", 'r')
        field = file.readline().split(' ')
        field.pop(len(field) - 1)#  удаление лишнего пробела
        file.close()
        return field   
    return 0