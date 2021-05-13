import os
import botfunc
import keyboards
import gamefunc
import testimages


class GameExceptions(Exception):
    def __init__(self, text):
        self.text = text


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

        '''try:
            botfunc.game.winCheck()
        except GameExceptions as g_exc:
            botfunc.message_edit(c, keyboard=False)
            botfunc.message_send(c, g_exc)
        else:
            bot_char = 'XO'.replace(getCharacter(C), '')
            botfunc_move = botfunc.game.botTurn(bot_char)
            if (bot_char == 'O'):
                testimages.circle(botfunc.game.field.point_positions[botfunc_move])
            else:
                testimages.cross(botfunc.game.field.point_positions[botfunc_move])
                try:
                    botfunc.game.winCheck()'''

        is_victory = gamefunc.win_check()
        if (not is_victory):
            bot_char = 'XO'.replace(getCharacter(c), '')
            botfunc_move = botfunc.game.botTurn(bot_char)
            if (bot_char == 'O'):
                testimages.circle(botfunc.game.field.point_positions[botfunc_move])
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
