from typing import NoReturn
from controller.handler import Handler
import telebot, telegramBotToken as telegramBotToken

class Client():
    def __init__(self, chat_id:str, message_id:str) -> None:
        self._chat_id = chat_id
        self._mess_id = message_id # id of the last message in chat
        self._game= None

    def set_game(self, game) -> None:
        self._game = game

    def get_game(self, game_mode:str=None):
        return self._game

    def del_game(self) -> None:
        self._game = None

    def get_chatId(self) -> str:
        return self._chat_id

    def onChar_selected(self, chat_id:str, char_label:str) -> tuple:
        self._game.set_field()
        if char_label == 'cross':
            self._game.set_char(chat_id, 'X')
            return self, 'X'
        elif char_label == 'zero':
            self._game.set_char(chat_id, 'O')
            return self, 'O'   


class Bot():
    _client_list = []

    def __init__(self, token:str=telegramBotToken.token) -> None:
        self._bot = telebot.TeleBot(token)
        self._bot.set_update_listener(self.command_listener) 
        self.set_call_back()
        self._bot.infinity_polling()

    def command_listener(self, messages) -> NoReturn:
        message = messages[0]
        if not self.get_client(message.chat.id):
            self._client_list.append(
                Client(message.chat.id, message.message_id)
            )
        command = Handler.get_command(message.text)
        command(self._bot, message.chat.id)
        
    def set_call_back(self) -> None:
        @self._bot.callback_query_handler(func=lambda c: True)
        def inline(c):
            chat_id = c.message.chat.id
            message = c.data
            client = self.get_client(chat_id)
            Handler.message_handler(self, client, chat_id, message)

    def send_message(self, 
                     chat_id:str,
                     text:str,
                     keyboard=False) -> None:
        self._bot.send_message(chat_id,
                              text,
                              reply_markup=keyboard)

    def send_photo(self, 
                   chat_id:str,
                   image_url:str,
                   capt:str=None,
                   keyboard=None) -> None:
        self._bot.send_photo(chat_id,
                            photo=open(image_url, 'rb'),
                            caption=capt,
                            reply_markup=keyboard)

    def edit_message(self, chat_id:str, message_id:str, **kwargs) -> None:
        keyboard = None
        self._bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=telebot.types.InputMediaPhoto(open('pol2.jpg', 'rb')),
                reply_markup=keyboard)

    def get_client(self, chat_id:str) -> Client|None:
        for client in self._client_list:
            if client.get_chatId() == chat_id:
                return client    