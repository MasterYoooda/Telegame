from errno import ENOEXEC
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
        if self.char == self._chars['zero']:
            super().move_processor(
                    self.get_opposite_char(self.char), 
                    GameBot.move(self._field.get(), self._chars)
            )

    def move_processor(self, char:str, cell_num=0) -> Error|GameStatus|None:
        super().move_processor(char, cell_num)
        super().move_processor(
            self._bot_char,
            GameBot.move(self._field.get(), self._chars)
        )