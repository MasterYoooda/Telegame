import gamemanager
import botfunc
import testimages
import random
import os


class Field:
    fieldMap:list
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
    winning_set = {
        (0,1,2) : (25,25,615,25),
        (3,4,5) : (25,320,615,320),
        (6,7,8) : (25,615,615,615),
        (0,3,6) : (25,25,25,615),
        (1,4,7) : (320,25,320,615),
        (2,5,8) : (615,25,615,615),
        (0,4,8) : (25,25,615,615),
        (2,4,6) : (615,25,25,615)
    }


    def __init__(self):
        self.fieldMap = list(range(0,9))
        #self.fileManager('write')


    def fileManager(self, op):
        if (op == "write"):
            file = open("game_data.txt", 'w')

            for d in self.fieldMap:
                file.write(str(d) + " ")
            file.close()

        if (op == "read"):
            file = open("game_data.txt", 'r')
            field = file.readline().split(' ')
            field.pop(len(field) - 1)#  удаление лишнего пробела
            file.close()
            return field   
        return 0


class Player:
    token = None
    character = ''

    def __init__(self, token, character):
        self.token = token 
        self.character = character


class GameBot(Player):
    token = 0

    def __init__(self, character:str):
        self.character = character


    def makeMove(self):
        #  well, this is temporary
        return random.randint(0,8)
    

class Game:
    field:Field
    game_mode = None
    players_list = {'X':Player, 'O':Player}


    def startGame(self):
        self.field = Field()


    def playerTurn(self, cell_number:int, character:str):        
        if str(self.field.fieldMap[cell_number]) not in "XO":
                self.field.fieldMap[cell_number] = character
                #self.field.fileManager("write")
        else:
            raise gamemanager.GameExceptions('Ячейка занята!')


    def botTurn(self, character:str):
        is_rightmove, turn = False, 0

        while (not is_rightmove):
            turn = self.players_list[character].makeMove()
            try:
                self.playerTurn(turn, character)
            except gamemanager.GameExceptions as g_exc:
                pass
            else:
                is_rightmove = True
        return str(turn)  #  возвращает текстовый ключ из словаря клеток 


    def winCheck(self):
        field = self.field.fieldMap
        winning_set = list(self.field.winning_set.keys())   

        for each in winning_set:
            if field[each[0]] == field[each[1]] == field[each[2]]:
                testimages.winline(self.field.winning_set[each])
                raise gamemanager.GameExceptions(field[each[0]] + " Победил!")

        if (len(frozenset(field)) == 2):
            raise gamemanager.GameExceptions("Ничья!")


    def modeDefined(self, c, mode):
        self.game_mode = mode


    def characterDefined(self, c, token):
        self.players_list[token] = Player(c, token)
        if (self.game_mode == 'mode_single'):
            self.players_list['XO'.replace(token,'')] = GameBot('XO'.replace(token,''))


    def moveMade(self, c): #осталась плохая алгоритмика с сингла
        def getCharacter(c):
            if self.players_list['X'].token != 0 and self.players_list['X'].token.message.chat.id == c.message.chat.id:
                return 'X'
            else:
                return 'O'

        try:
            self.playerTurn(int(c.data), getCharacter(c))
        except gamemanager.GameExceptions as g_exc:
            botfunc.message_send(c, g_exc)
        else:
            if (getCharacter(c) == 'X'):
                testimages.cross(self.field.point_positions[c.data])
            else:
                testimages.circle(self.field.point_positions[c.data])

            try:
                self.winCheck()
            except gamemanager.GameExceptions as g_exc:
                botfunc.message_edit(c, keyboard=False)
                botfunc.message_send(c, g_exc)
            else:
                bot_char = 'XO'.replace(getCharacter(c), '')
                botfunc_move = self.botTurn(bot_char)

                if (bot_char == 'O'):
                    testimages.circle(self.field.point_positions[botfunc_move])
                else:
                    testimages.cross(self.field.point_positions[botfunc_move])

                try:
                    self.winCheck()
                except gamemanager.GameExceptions as g_exc:
                    botfunc.message_edit(c, keyboard = False)
                    botfunc.message_send(c, g_exc)
                    os.remove("pol2.jpg")
                else:
                    botfunc.message_edit(c)