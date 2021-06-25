import gamemanager
import botfunc
import testimages
import random
import os
from abc import ABC, abstractmethod


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


class Player:
    def __init__(self, token, character):
        self.token = token 
        self.character = character


class GameBot(Player):
    def __init__(self, character:str):
        self.character = character

    def makeMove(self)->int:
        return random.randint(0,8)


class Game(ABC):
    field:Field
    game_mode = None  # 'mode_single' or 
    players_list = {'X':Player, 'O':Player}
    current_move = 'X'  # X or O

    def modeDefined(self, c, mode:str):
        self.game_mode = mode

    @abstractmethod
    def characterDefined(self, c, character:str):
        self.players_list[character] = Player(c, character)

    def startGame(self):
        self.field = Field()

    def playerTurn(self, cell_number:int, character:str):    
        # значение ячейки не содержится в "ХО", тогда  она свободна    
        if str(self.field.fieldMap[cell_number]) not in "XO":
                self.field.fieldMap[cell_number] = character
        else:
            raise gamemanager.GameExceptions('Ячейка занята!')

    @abstractmethod
    def moveMade(self, c):
        pass

    def winCheck(self):
        field = self.field.fieldMap
        winning_set = list(self.field.winning_set.keys())   

        for each in winning_set:
            if field[each[0]] == field[each[1]] == field[each[2]]:
                testimages.winline(self.field.winning_set[each])
                raise gamemanager.GameExceptions(field[each[0]] + " Победил!")
        if (len(frozenset(field)) == 2):
            raise gamemanager.GameExceptions("Ничья!")

    def imageMake(self, character:str, data:str):
        if (character == 'X'):
            testimages.cross(self.field.point_positions[data])
        else:
            testimages.circle(self.field.point_positions[data])    


class SingleGame(Game):
    field:Field
    game_mode = 'mode_single'
    players_list = {'X':Player, 'O':Player}

    def characterDefined(self, c, character:str):
            super().characterDefined(c, character)
            # если синг - автоматом создаем бота из другого игрока
            if (self.game_mode == 'mode_single'):
                botCharacter = 'XO'.replace(character,'')
                self.players_list[botCharacter] = GameBot(botCharacter)

    def botTurn(self, character:str) -> str:
        is_right_move, turn = False, 0
        # бот рандомный, поэтому надо проверять его ходы
        while (not is_right_move):
            turn = self.players_list[character].makeMove()
            try:
                self.playerTurn(turn, character)
            except gamemanager.GameExceptions as g_exc:
                pass
            else:
                is_right_move = True
        return str(turn)

    def moveMade(self, c) -> str:
        # возвращает персонажа игрока из списка игроков в классе игры       
        def getCharacter(c):
            if self.players_list['X'].token != 0 and \
                self.players_list['X'].token.message.chat.id == c.message.chat.id:
                return 'X'
            else:
                return 'O'     

        # производит очистку временных файлов игры и убирает клавиатуру в чате
        def killGame(g_exc:gamemanager.GameExceptions):            
            botfunc.entireBot.message_edit(c, keyboard = False)
            botfunc.message_send(c, g_exc)
            os.remove("pol2.jpg")
        # если сейчас ход человека
        if self.current_move == getCharacter(c):
            # попытка выполнить ход
            try:                 
                self.playerTurn(int(c.data), getCharacter(c))
            except gamemanager.GameExceptions as g_exc:
                botfunc.message_send(c, g_exc)
                return
            else:
                # если все удачно - отмечаем изменения на поле
                self.imageMake(getCharacter(c), c.data)
        # ход бота
        else:
            botfunc_move = self.botTurn(self.current_move)
            self.imageMake(self.current_move, botfunc_move)
        # проверка на победу
        try:  
            self.winCheck()
        except gamemanager.GameExceptions as g_exc:
            killGame(g_exc)
        else:
            # наступает очередь хода другого игрока
            self.current_move = 'XO'.replace(self.current_move, '')

            # если наступает очередь хода бота - вызываем ход для него
            if self.current_move != getCharacter(c):
                self.moveMade(c) 
            else:
                # если очередь человека, а он еще ни разу не ходил, 
                # то надо отправить поле с первым ходом бота
                if not(self.current_move in self.field.fieldMap):
                    botfunc.photo_send(c, 'pol2.jpg')
                    return

                botfunc.message_edit(c)       