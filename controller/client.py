from tictactoe.game import Game

class Client():
    _chat_id:str = None
    _mess_id:str = None
    _game:Game = None
    
    def __init__(self, chat_id:str, message_id:str, game:Game=None) -> None:
        self._chat_id = chat_id
        self._mess_id = message_id
        self._game:Game = game

    def set_game(self, game:Game) -> None:
        self._game = game

    def get_game(self, game_mode=None) -> Game:
        return self._game

    def del_game(self) -> None:
        self._game = None

    def get_chat_id(self) -> str:
        return self._chat_id

    def set_game_char(self, char:str) -> None:
        self._game.set_char(char)

    def get_game_char(self) -> str:
        return self._game.get_char()

    def get_map(self) -> list:
        return self._game.get_field_map()

    def move(self, message:str) -> None:
        char = self.get_game_char()
        self._game.move_processor(char, message)