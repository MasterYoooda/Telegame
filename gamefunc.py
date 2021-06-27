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
        '2' : (530, 110),
        '3' : (110,320),
        '4' : (320,320),
        '5' : (530,320),
        '6' : (110,530),
        '7' : (320,530),
        '8' : (530,530)
    }
    winning_set = {
        (0,1,2) : (25,110,615,110),
        (3,4,5) : (25,320,615,320),
        (6,7,8) : (25,530,615,530),
        (0,3,6) : (110,25,110,615),
        (1,4,7) : (320,25,320,615),
        (2,5,8) : (530,25,530,615),
        (0,4,8) : (25,25,615,615),
        (2,4,6) : (615,25,25,615)
    }

    def __init__(self):
        self.fieldMap = list(range(0,9))
        #self.fileManager('write')


class Player:
    def __init__(self, chat_id: str, character: str):
        self._chat_id = chat_id 
        self._character = character

    def getChat_id(self) -> str:
        return self._chat_id

    def getCharacter(self) -> str:
        return self._character


class GameBot(Player):
    def __init__(self, character: str):
        self._character = character
        self._chat_id = 0

    def makeMove(self) -> int:
        return random.randint(0,8)


class Game(ABC):
    _field:Field
    _game_mode = None  # 'mode_single' or 
    _players_list = {'X':Player, 'O':Player}
    _current_move = 'X'  # X or O

    def getPointPositions(self):
        return self._field.point_positions

    def getFieldMap(self) -> list:
        return self._field.fieldMap

    def modeDefined(self, mode: str):
        self._game_mode = mode

    @abstractmethod
    def characterDefined(self, chat_id: str, character: str):
        self._players_list[character] = Player(chat_id, character)

    def startGame(self):
        self._field = Field()

    def playerTurn(self, cell_number: int, character: str):    
        # значение ячейки не содержится в "ХО", тогда  она свободна    
        if str(self.getFieldMap()[cell_number]) not in "XO":
                self.getFieldMap()[cell_number] = character
        else:
            raise gamemanager.GameExceptions('Ячейка занята!')

    @abstractmethod
    def moveMade(self):
        pass

    def winCheck(self):
        field = self.getFieldMap()
        winning_set = list(self._field.winning_set.keys())   
        for each in winning_set:
            if field[each[0]] == field[each[1]] == field[each[2]]:
                testimages.MakeImage().winline_draw(self.getFieldMap(), 
                                                    self._field.winning_set[each],
                                                    self.getPointPositions())
                # testimages.winline(self._field.winning_set[each])
                raise gamemanager.GameExceptions(field[each[0]] + " Победил!")
        if (len(frozenset(field)) == 2):
            raise gamemanager.GameExceptions("Ничья!")

    # def makeImage(self):
    #     testimages.MakeImage.image_draw(self.getFieldMap(), self.getPointPositions())   

    # def imageMake(self, character:str, data:str):
    #     if (character == 'X'):
    #         testimages.cross(self._field.point_positions[data])
    #     else:
    #         testimages.circle(self._field.point_positions[data])    


class SingleGame(Game):
    _game_mode = 'mode_single'

    def characterDefined(self, chat_id: str, character: str):
            super().characterDefined(chat_id, character)
            # если синг - автоматом создаем бота из другого игрока
            if (self._game_mode == 'mode_single'):
                botCharacter = 'XO'.replace(character,'')
                self._players_list[botCharacter] = GameBot(botCharacter)

    def botTurn(self, character: str) -> str:
        is_right_move, turn = False, 0
        # бот рандомный, поэтому надо проверять его ходы
        while (not is_right_move):
            turn = self._players_list[character].makeMove()
            try:
                self.playerTurn(turn, character)
            except gamemanager.GameExceptions as g_exc:
                pass
            else:
                is_right_move = True
        return str(turn)

    # Позвращает персонажа игрока из списка игроков в классе игры       
    def getCharacter(self, c):
        # token == 0 только у бота
        if self._players_list['X'].getChat_id() != 0 and \
            self._players_list['X'].getChat_id() == c.message.chat.id:
            return 'X'
        else:
            return 'O'   

    # Получение хода и попытка его выполнить
    def moveMade(self, c):
        # если сейчас ход человека
        if self._current_move == self.getCharacter(c):
            # попытка выполнить ход
            try:                 
                self.playerTurn(int(c.data), self.getCharacter(c))
            except gamemanager.GameExceptions as g_exc:
                return g_exc
            else:
                pass
                # если все удачно - отмечаем изменения на поле
                # self.imageMake(self.getCharacter(c), c.data)
        # ход бота
        else:
            bot_move = self.botTurn(self._current_move)
            # self.imageMake(self._current_move, bot_move) 
        # проверка на победу
        try:  
            self.winCheck()
        except gamemanager.GameExceptions as g_exc:
            text = g_exc
            return text
        else:
            # наступает очередь хода другого игрока
            self._current_move = 'XO'.replace(self._current_move, '')
            # если наступает очередь хода бота - вызываем ход для него
            if self._current_move != self.getCharacter(c):
                move_output = self.moveMade(c) 
                if move_output:
                    return move_output
            else:
                # если ходов человека(О) еще нет - нет сообщения для редактирования
                if not(self._current_move in self.getFieldMap()):
                    return
            return gamemanager.GameExceptions('Ход выполнен!')    