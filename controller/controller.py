from cgi import print_directory
import telebot
from typing import NoReturn
from controller.exceptions import NoClientInBase, WrongCommandName
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
        self._client_ctrlr = client_controller
        self._bot_ctrlr = BotController(
                telegram_bot,
                self.command_listener,
                self.keyboard_handler
        )
        print('Initialised')

    def start(self) -> NoReturn:
        """Calls for bot controller to start infinity polling"""
        print('started')
        self._bot_ctrlr.start()
        
    def command_listener(self, messages:list) -> NoReturn:
        message = messages[0]
        command:Command
        try:
            command = Command.get(message.text)
            client = self.base.get(message.chat.id)
        except NoClientInBase:
            self.base.add(Client(message.chat.id, message.message_id))
        except WrongCommandName as e:
            print(str(e))
            return
        self._bot_ctrlr.command_handler(command, message.chat.id)

    # Inline keyboard callback's handler
    def keyboard_handler(self, chat_id:str, message:str) -> None:
        try:
            client = self.base.get(chat_id)
            event = Event.get(message)
            self._client_ctrlr.callback_handler(client, event, message)
            self._bot_ctrlr.keyboard_reply(
                    event, 
                    client.get_chat_id(),
                    client.get_game_char()
            )
        except Exception as e:
            print(str(e))