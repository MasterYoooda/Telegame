from tictactoe.game import Game

class Client():
    _chat_id:str = None
    _bot_last_msg:int = None
    _game:Game = None
    
    def __init__(self, chat_id:str, game:Game=None) -> None:
        self._chat_id = chat_id
        self._game:Game = game

    @property
    def game(self, game_mode=None) -> Game:
        return self._game

    @game.setter
    def game(self, game:Game) -> None:
        self._game = game

    @game.deleter
    def game(self) -> None:
        self._game = None

    @property
    def chat_id(self) -> str:
        return self._chat_id

    @property
    def bot_last_msg(self) -> int:
        return self._bot_last_msg

    @bot_last_msg.setter
    def bot_last_msg(self, id:int) -> None:
        self._bot_last_msg = id

    @property
    def game_char(self) -> str:
        return self._game.char

    @game_char.setter
    def game_char(self, char_name:str) -> None:
        self._game.char = char_name

    def get_map(self) -> list:
        return self._game.field

    def move(self, message:str) -> None:
        char = self.get_game_char()
        self._game.move_processor(char, int(message))