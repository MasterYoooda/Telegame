import os
import botfunc
import keyboards
import gamefunc
import testimages


class Game:
    pass

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
    gamemode = mode
    botfunc.message_send(
        c,
        'Вы хотите ходить первым или вторым? Если хотите ходить первым - выберите крестики, вторым - нолики',
        keyboard=keyboards.priority_keyboard) 


def character_defined(c, token):
    gamefunc.start_game()
    botfunc.photo_send(c)


def move_made(c):
    #<- похоже надо дописать функцию перевода текстового ключа в индекс клетки
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
            botfunc.message_send(c, 'Ячейка занята')   #<- заменить на что-то более красивое


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