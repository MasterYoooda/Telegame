from enum import Enum
from .client import Client
from tictactoe.game import Single, Event

class ClientController():
    def callback_handler(self, client:Client, event:Event, message:str) -> None:
        if event == Event.SINGLE_MODE:
            client.game = Single()
        if event == Event.MULTI_MODE:
            pass
        if event == Event.CROSS or event == Event.ZERO:
            client.game_char = message
        if event == Event.MOVE:
            client.move(message)