from tictactoe.field import Field
from .gamebot import GameBot
from abc import ABC, abstractmethod
from controller.exceptions import *
from enum import Enum, auto, unique

@unique
class Event(Enum):
    SINGLE_MODE = 'mode_single'
    MULTI_MODE = 'mode_multie'
    CROSS = 'cross'
    ZERO = 'zero'
    # string of possible move indexes
    MOVE = ''.join(list(Field.__call__()))

    @classmethod
    def get(self, text:str) -> Enum:
        for e in self:
            if e.value == text or text in e.value:
                return e
        raise NonExistentEvent(text)


class Game(ABC):
    _field:Field = None
    # client game char
    _char:str = None
    # An indicator, whose turn
    _chars = {'cross':'❌', 'zero':'⭕️'}
    _char_in_turn = _chars['cross']

    def __init__(self) -> None:
        self._field:Field = Field()
        # char of the client
        self._char = None

    @property
    def field(self) -> list:
        return self._field.get()

    @field.setter
    def field(self, field:Field):
        self._field = field

    @property
    def char(self) -> str:
        return self._char

    @char.setter
    @abstractmethod
    def char(self, char_name:str) -> CharIsOccupied|None:
        if self._char is not None:
            raise CharIsOccupied(char_name)
        self._char = self._chars[char_name]

    def chars_collection() -> list:
        return Game._chars.values()

    def get_opposite_char(self, char:str):
        return ''.join(list(self._chars.values())).replace(char,'')

    @abstractmethod
    def move_processor(self, char:str, cell_num:int) -> Error|GameStatus|None:
        if self._char_in_turn != char:
            raise TurnQueueError()
        self.update_map(char, cell_num)
        self.check_win()
        self._char_in_turn = self.get_opposite_char(char)

    def update_map(self, char:str, cell_num:int) -> CellIsOccupied|None:
        if str(self._field.get()[cell_num]) not in ''.join(list(self._chars.values())):
            self._field.update_map(cell_num, char)
        else:
            raise CellIsOccupied()

    def check_win(self) -> Win|Draw|None:
        self._field.field_status()


class Single(Game):
    _game_mode = 'single'
    _bot_char:str =  None

    @property
    def char(self) -> str:
        return self._char

    @char.setter
    def char(self, char: str) -> None:
        Game.char.fset(self, char)
        self._bot_char = self.get_opposite_char(self._char)
        # bot_char = 'XO'.replace(char,'')
        # self.set_char(bot_char)

    # def bot_move(self, char:str) -> str:
    #     is_moved, turn = False, 0
    #     # Bot tries to make a turn until it selects a free cell
    #     while not is_moved:
    #         turn = self._players[char].make_move()
    #         try:
    #             self.update_map(turn, char)
    #         except:
    #             pass
    #         else:
    #             is_moved = True
    #     return str(turn)

    # def get_char(self, chat_id:str) -> str:
    #     if self._players['X'].get_chatId() != 0 and \
    #             self._players['X'].get_chatId() == chat_id:
    #         return 'X'
    #     else:
    #         return 'O'

    def move_processor(self, char:str, cell_num=0) -> Error|GameStatus|None:
        super().move_processor(char, cell_num)
        super().move_processor(
                self._bot_char,
                GameBot.move(self._field.get(), self._chars)
        )
        # if self._char_in_turn == char:
        #     try:
        #         self.update_map(cell_num, char)
        #     except CellIsOccupied as er:
        #         raise er
        # else:
        #     self.bot_move(self._char_in_turn)
        # win = self.check_win()
        # if win:
        #     return win       
        # # Change a turn of the move
        # self._char_in_turn = 'XO'.replace(self._char_in_turn, '')
        # # If it's the bot's turn - calls for it
        # if self._char_in_turn != self.get_char(chat_id):
        #     move = self.move_processor(chat_id, cell_num)
        #     if move:
        #         return move
        # else:
        #     # if there're no moves of the real man(O) yet, there's no message to edit
        #     if not self._char_in_turn in self._field.get_field():
        #         return
        # return 'Ход выполнен!'