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
            field.pop(len(field) - 1)  #  удаление лишнего пробела
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


class Game():
    field:Field
    game_mode = None  # 'mode_single' or 
    players_list = {'X':Player, 'O':Player}
    current_move = 'X'  # X or O


    def startGame(self):
        self.field = Field()


    def playerTurn(self, cell_number:int, character:str):        
        if str(self.field.fieldMap[cell_number]) not in "XO":
                self.field.fieldMap[cell_number] = character
        else:
            raise gamemanager.GameExceptions('Ячейка занята!')


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


    def imageMake(self, character:str, data:str):
        if (character == 'X'):
            testimages.cross(self.field.point_positions[data])
        else:
            testimages.circle(self.field.point_positions[data])


    def moveMade(self, c):
        def getCharacter(c):
            if self.players_list['X'].token != 0 and self.players_list['X'].token.message.chat.id == c.message.chat.id:
                return 'X'
            else:
                return 'O'
    

class SingleGame(Game):
    field:Field
    game_mode = 'mode_single'
    players_list = {'X':Player, 'O':Player}


    def startGame(self):
        self.field = Field()


    def botTurn(self, character:str):
        is_right_move, turn = False, 0

        while (not is_right_move):
            turn = self.players_list[character].makeMove()
            try:
                self.playerTurn(turn, character)
            except gamemanager.GameExceptions as g_exc:
                pass
            else:
                is_right_move = True
        return str(turn)  #  возвращает текстовый ключ из словаря клеток 


    def characterDefined(self, c, token):
        self.players_list[token] = Player(c, token)
        if (self.game_mode == 'mode_single'):
            self.players_list['XO'.replace(token,'')] = GameBot('XO'.replace(token,''))


    def moveMade(self, c): #остался плохой код с сингла
         
        def getCharacter(c):
            if self.players_list['X'].token != 0 and self.players_list['X'].token.message.chat.id == c.message.chat.id:
                return 'X'
            else:
                return 'O'      
        
        def killGame(g_exc:gamemanager.GameExceptions):
            botfunc.message_edit(c, keyboard = False)
            botfunc.message_send(c, g_exc)
            os.remove("pol2.jpg")

        if self.current_move == getCharacter(c):
            try:  # проверка на пустоту ячейки
                self.playerTurn(int(c.data), getCharacter(c))
            except gamemanager.GameExceptions as g_exc:
                botfunc.message_send(c, g_exc)
                return
            else:
                self.imageMake(getCharacter(c), c.data)

        else:
            botfunc_move = self.botTurn(self.current_move)
            self.imageMake(self.current_move, botfunc_move)

        try:  # проверка на победу
            self.winCheck()
        except gamemanager.GameExceptions as g_exc:
            killGame(g_exc)
        else:
            self.current_move = 'XO'.replace(self.current_move, '')

            if self.current_move != getCharacter(c):
                self.moveMade(c) 
            else:
                #  если играем за нолик, то боту-крестику надо отправить картинку со своим ходом
                if not(self.current_move in self.field.fieldMap):
                    botfunc.photo_send(c, 'pol2.jpg')
                    return
                botfunc.message_edit(c)       

        # try:
        #     self.playerTurn(int(c.data), getCharacter(c))
        # except gamemanager.GameExceptions as g_exc:
        #     botfunc.message_send(c, g_exc)
        # else:
        #     self.imageMake(getCharacter(c), c.data)
        #     try:
        #         self.winCheck()
        #     except gamemanager.GameExceptions as g_exc:
        #         killGame(g_exc)
        #     else:
        #         bot_char = 'XO'.replace(getCharacter(c), '')
        #         botfunc_move = self.botTurn(bot_char)

        #         self.imageMake(bot_char, botfunc_move)

        #         try:
        #             self.winCheck()
        #         except gamemanager.GameExceptions as g_exc:
        #             killGame(g_exc)
        #         else:
        #             botfunc.message_edit(c)