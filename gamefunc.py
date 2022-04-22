import testimages, game.field as field
from messages import GameMessage
import random
from abc import ABC, abstractmethod


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
    _current_move = 'X'  # X or O

    def __init__(self, game_mode):
        self._field:field.Field = None
        self._game_mode = game_mode  # 'mode_single' or 
        self._players_list = {'X':Player, 'O':Player}

    def getPointPositions(self):
        return self._field.point_positions

    def getFieldMap(self) -> list:
        return self._field.get_field()

    # def modeDefined(self, mode: str):
    #     self._game_mode = mode

    @abstractmethod
    def characterDefined(self, chat_id: str, character: str):
        self._players_list[character] = Player(chat_id, character)

    def startGame(self):
        self._field = field.Field()

    def playerTurn(self, cell_number: int, character: str):    
        # The cell value isn't contained in "XO", then it's free   
        if str(self.getFieldMap()[cell_number]) not in "XO":
                self.getFieldMap()[cell_number] = character
        else:
            raise GameMessage('Ячейка занята!')

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
                raise GameMessage(field[each[0]] + " Победил!")
        if (len(frozenset(field)) == 2):
            raise GameMessage("Ничья!") 


class SingleGame(Game):
    # def __init__(self):
    #     super.__init__()
    #     self._game_mode = 'mode_single'

    def characterDefined(self, chat_id: str, character: str):
            super().characterDefined(chat_id, character)
            # If it's a single-game - creating a bot as a second player
            if (self._game_mode == 'mode_single'):
                botCharacter = 'XO'.replace(character,'')
                self._players_list[botCharacter] = GameBot(botCharacter)

    def botTurn(self, character: str) -> str:
        is_right_move, turn = False, 0
        # Bot tries to make a turn until it selects a free cell
        while (not is_right_move):
            turn = self._players_list[character].makeMove()
            try:
                self.playerTurn(turn, character)
            except GameMessage as g_exc:
                pass
            else:
                is_right_move = True
        return str(turn)

    #  Return player's character
    def getCharacter(self, c):
        # chat_id == 0 - NPC
        if self._players_list['X'].getChat_id() != 0 and \
            self._players_list['X'].getChat_id() == c.message.chat.id:
            return 'X'
        else:
            return 'O'   

    # Getting a move and trying to execute it
    def moveMade(self, c):
        # if it's a real man's turn
        if self._current_move == self.getCharacter(c):
            # attempt to execute a turn
            try:                 
                self.playerTurn(int(c.data), self.getCharacter(c))
            except GameMessage as g_exc:
                return g_exc
            else:
                pass
        # the Bot's turn
        else:
            bot_move = self.botTurn(self._current_move)
            # self.imageMake(self._current_move, bot_move) 
        # Check for win
        try:  
            self.winCheck()
        except GameMessage as g_exc:
            text = g_exc
            return text
        else:
            # Change a turn of the move
            self._current_move = 'XO'.replace(self._current_move, '')
            # If it's the bot's turn - calls for it
            if self._current_move != self.getCharacter(c):
                move_output = self.moveMade(c) 
                if move_output:
                    return move_output
            else:
                # if there're no moves of the real man(O) yet, there's no message to edit
                if not(self._current_move in self.getFieldMap()):
                    return
            return GameMessage('Ход выполнен!')    


class MultiGame(Game):
    pass