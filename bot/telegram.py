from enum import Enum, auto, unique
from re import A
from tictactoe.game import Event
from typing import NoReturn
from .keyboards import GameSelectionKeyboard, CharSelectionKeyboard, GameKeyboard
from controller.exceptions import *
import telebot, os


@unique
class Command(Enum):
    START = {
        'text':'/start',
        'description':''
    }
    NEWGAME = {
        'text':'/newgame',
        'description':''
    }

    @classmethod
    def get(self, cmd:str) -> Enum:
        for command in self:
            if command.value['text']== cmd:
                return command
        raise WrongCommandName(cmd)
        

class BotController(telebot.TeleBot):
    def __init__(self, bot:telebot.TeleBot, listener, callback_handler,) -> None:
        self._callback_handler = callback_handler
        self._bot = bot
        self._bot.set_update_listener(listener)
        self.set_call_back()
    
    # The actual start of the bot
    def start(self) -> NoReturn:
        self._bot.infinity_polling()

    def set_call_back(self) -> None:
        @self._bot.callback_query_handler(func=lambda call: True)
        def inline(call):
            chat_id = call.message.chat.id
            message = call.data
            self._callback_handler(chat_id, message)

    def command_handler(self, cmd:Command, chat_id:str, bot_last_msg:int=None) -> int|None:
        self.delete_message(chat_id, bot_last_msg)
        if cmd == Command.START:
            return self.start_reply(chat_id)
        elif cmd == Command.NEWGAME:
            return self.newgame_reply(chat_id)

    def start_reply(self, chat_id:str) -> int:
        return self._bot.send_message(
                chat_id, 
                'Click on "/newgame"'
        ).message_id

    def newgame_reply(self,
                    chat_id:str, 
                    keyboard=None) -> int:
        kbrd = keyboard if keyboard is not None else GameSelectionKeyboard.make()
        return self._bot.send_message(chat_id,
                'Choose a game mode',
                reply_markup=kbrd
        ).message_id

    def keyboard_reply(self,
                    event:Event,
                    chat_id:str,
                    bot_last_msg:int=None,
                    emoji:str=None) -> int|None:
        self.delete_message(chat_id, bot_last_msg)
        if event in [Event.SINGLE_MODE, Event.MULTI_MODE]:
            return self._bot.send_message(
                    chat_id,
                    'Choose your Char',
                    reply_markup=CharSelectionKeyboard.make()
            ).message_id
        if event == Event.CROSS:
            return self._bot.send_photo(
                    chat_id,
                    photo=open('storage/pol.jpg', 'rb'),
                    reply_markup=GameKeyboard.make(emoji)
            ).message_id
        if event in [Event.ZERO, Event.MOVE]:
            msg_id = self._bot.send_photo(
                    chat_id,
                    photo=open('storage/pol2.jpg', 'rb'),
                    reply_markup=GameKeyboard.make(emoji)
            ).message_id
            os.remove('storage/pol2.jpg')
            return msg_id

    def delete_message(self, chat_id:str, message_id:int) -> None:
        if message_id is None: return
        self._bot.delete_message(chat_id, message_id)
            


"""Unused entities
# class Client():
#     def __init__(self, chat_id:str, message_id:str) -> None:
#         self._chat_id = chat_id
#         self._mess_id = message_id # id of the last message in chat
#         self._game= None

#     def set_game(self, game) -> None:
#         self._game = game

#     def get_game(self, game_mode:str=None):
#         return self._game

#     def del_game(self) -> None:
#         self._game = None

#     def get_chatId(self) -> str:
#         return self._chat_id

#     def onChar_selected(self, chat_id:str, char_label:str) -> tuple:
#         self._game.set_field()
#         if char_label == 'cross':
#             self._game.set_char(chat_id, 'X')
#             return self, 'X'
#         elif char_label == 'zero':
#             self._game.set_char(chat_id, 'O')
#             return self, 'O'   


# class BotHandler():
#     _bot:telebot.TeleBot = None

#     def __init__(self, bot) -> None:
#         self._bot = bot

#     def onstart(self, chat_id:str):
#         self._bot.send_message(chat_id, 'Click on "/newgame"')

#     def onnew_game(self, chat_id:str,
#                     keyboard:telebot.types.InlineKeyboardMarkup):
#         self._bot.send_message(chat_id,
#                         'Выберите режим игры:',
#                         reply_markup=keyboard)

#     def ongame_mode_selected(self):
#         pass

#     def onchar_selected(self):
#         pass
"""

""" old Code
    # def command_listener(self, messages) -> NoReturn:
    #     message = messages[0]
    #     if not self.get_client(message.chat.id):
    #         self._client_list.append(
    #             Client(message.chat.id, message.message_id)
    #         )
    #     command = Controller.get_command(message.text)
    #     command(self._bot, message.chat.id)
        
    # def set_call_back(self) -> None:
    #     @self._bot.callback_query_handler(func=lambda c: True)
    #     def inline(c):
    #         chat_id = c.message.chat.id
    #         message = c.data
    #         client = self.get_client(chat_id)
    #         Controller.message_handler(self, client, chat_id, message)

    # def send_message(self, 
    #                  chat_id:str,
    #                  text:str,
    #                  keyboard=False) -> None:
    #     self._bot.send_message(chat_id,
    #                           text,
    #                           reply_markup=keyboard)

    # def send_photo(self, 
    #                chat_id:str,
    #                image_url:str,
    #                capt:str=None,
    #                keyboard=None) -> None:
    #     self._bot.send_photo(chat_id,
    #                         photo=open(image_url, 'rb'),
    #                         caption=capt,
    #                         reply_markup=keyboard)

    # def edit_message(self, chat_id:str, message_id:str, **kwargs) -> None:
    #     keyboard = None
    #     self._bot.edit_message_media(
    #             chat_id=chat_id,
    #             message_id=message_id,
    #             media=telebot.types.InputMediaPhoto(open('pol2.jpg', 'rb')),
    #             reply_markup=keyboard)

    # def get_client(self, chat_id:str) -> Client|None:
    #     for client in self._client_list:
    #         if client.get_chatId() == chat_id:
    #             return client
"""