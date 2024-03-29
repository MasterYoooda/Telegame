from shutil import ExecError
import telebot
from typing import NoReturn

from tictactoe.field import Field
from tictactoe.game import Game
from .fieldimage import ImageController
from .exceptions import *
from storage.local import ClientBase
from bot.telegram import Command, BotController
from .clientcontroller import ClientController
from .client import Client
from tictactoe.game import Event


class Controller():
    def __init__(self, telegram_bot:telebot.TeleBot, 
                client_controller:ClientController, 
                base:ClientBase=None) -> None:
        self.base = base if base else ClientBase()
        self._image_ctrlr = ImageController(list(Game.chars_collection()))
        self._client_ctrlr = client_controller
        self._bot_ctrlr = BotController(
                telegram_bot,
                self.command_listener,
                self.keyboard_handler
        )
        print('Initialised')

    def start(self) -> NoReturn:
        """Calls for bot controller to start infinity polling"""
        self._bot_ctrlr.start()
        
    def command_listener(self, messages:list) -> NoReturn:
        message = messages[0]
        command:Command
        client:Client
        try:
            command = Command.get(message.text)
            client = self.base.get(message.chat.id)
        except NoClientInBase:
            client = self.base.add(Client(message.chat.id))
        except WrongCommandName as e:
            print(str(e))
            return
        msg_id = self._bot_ctrlr.command_handler(
                command, 
                message.chat.id,
                client.bot_last_msg
        )
        client.bot_last_msg = msg_id

    # Inline keyboard callback's handler
    def keyboard_handler(self, chat_id:str, message:str) -> None:
        client:Client
        msg_id:int=None
        try:
            client = self.base.get(chat_id)
            event = Event.get(message)
            self._client_ctrlr.callback_handler(client, event, message)
            self._image_ctrlr.image_draw(client.get_map(), Field.__call__(), event)
            msg_id = self._bot_ctrlr.keyboard_reply(
                    event, 
                    client.chat_id,
                    bot_last_msg=client.bot_last_msg,
                    emoji=client.game_char
            )
        except Error as e:
            print(e)
        except (Win, Draw) as gs:
            self._image_ctrlr.winline_draw(client.get_map(), gs.line, Field.__call__(), Event.END_GAME)
            msg_id = self._bot_ctrlr.end_game_reply(chat_id, str(gs), client.bot_last_msg)
            del client.game
            print(str(gs))
        finally:
            client.bot_last_msg = msg_id