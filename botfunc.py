import telebot

import keyboards
import gamefunc
import gamemanager
import testimages

import telegramBotToken

import os
from telebot.types import InlineKeyboardMarkup, Message

class Client:
    _game: None
    _chat_id: str

    def __init__(self, chat_id: str, message_id: str):
        self._chat_id = chat_id
        self._message_id = message_id
    
    def setGame(self, game_mode: str):
        if game_mode == 'mode_single':
            self._game = gamefunc.SingleGame()
            self._game.modeDefined(game_mode)

    def getGame(self):
        return self._game

    def delGame(self):
        self._game = None

    def getChat_id(self):
        return self._chat_id


class EntireBot():
    bot:telebot.TeleBot
    # __game = None
    __gamelist = []
    __clientlist = []

    start_keyboard = keyboards.StartKeyboard.makeKeyboard()
    priority_keyboard = keyboards.PriorityKeyboard.makeKeyboard()

    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)       

    def startCommand(self, message):
        self.bot.send_message(
            message.chat.id,
            'Нажми "/newgame"'
        )  
    # метод в который приходят команды
    def messageListener(self, messages:list):
        message = messages[0]
        # если клиент пишет первый раз - запоминаем его
        if not (self.getCurrentClient(message.chat.id)):
            self.__clientlist.append(Client(message.chat.id, message.message_id))
        if message.text == '/start' or \
            message.text == '/start@Telgames_bot':
            self.startCommand(message)
        if message.text == '/newgame' or \
            message.text == '/newgame@Telgames_bot':
            self.newGame(message)

    def newGame(self, message):
        self.bot.send_message(
            message.chat.id,
            'Выберете режим игры:',
            reply_markup=self.start_keyboard
        )
        
    def setCallBack(self):
        @self.bot.callback_query_handler(func=lambda c: True)
        def inline(c):
            client = self.getCurrentClient(c.message.chat.id)
            if c.data == 'mode_single':
                client.setGame('mode_single') 
                self.message_send(
                    c,
                    'Выберите, за кого хотите играть:',
                    keyboard=self.priority_keyboard
                )
                return
            if c.data == 'cross' or c.data == 'zero':
                self.chooseCharacter(c, client)
            if c.data in client.getGame().getPointPositions():
                game = client.getGame()
                self.checkMoveOutput(game.moveMade(c), c, client)

    # проверка состояния игры
    def checkMoveOutput(self, move_output: str, c, client: Client):
        if not(move_output) or 'выполнен!' in move_output.text:
            self.makeImage(client.getGame().getFieldMap(), client.getGame().getPointPositions())
            self.message_edit(c, character=client.getGame().getCharacter(c)) 
            return
        if 'Победил!' in move_output.text or 'Ничья!' in move_output.text:
            self.killGame(c, move_output)
        if 'занята!' in move_output.text:
            self.message_send(c, move_output)

    # события при выборе персонажа
    def chooseCharacter(self, c, client: Client):
        if c.data == 'cross':
            client.getGame().characterDefined(c.message.chat.id,'X')
            client.getGame().startGame()
            self.photo_send(client, 'X')
        elif c.data == 'zero':
            client.getGame().characterDefined(c.message.chat.id,'O')
            client.getGame().startGame()
            # разрешаем себе не обрабатывать результат хода, 
            # потому что выиграть никак не получится на данном этапе
            print(client.getGame().moveMade(c))
            self.photo_send(client, 'O', 'pol2.jpg')

    def message_send(self, c, text, keyboard=False):
        self.bot.send_message(c.message.chat.id, text, reply_markup=keyboard)

    def makeImage(self, fieldMap: list, point_positions: dict):
        testimages.MakeImage().image_draw(fieldMap, point_positions)

    def delFieldImage(self):
        try:
            os.remove('pol2.jpg')
        except:
            pass
            # raise gamemanager.GameExceptions('нет файла с полем') 

    def photo_send(self, client: Client, character: str, image='pol.jpg'):
        self.makeImage(client.getGame().getFieldMap(), client.getGame().getPointPositions())

        self.bot.send_photo(
            client.getChat_id(),
            photo=open(image, 'rb'),
            caption='Выберете на клавиатуре, в какую клетку на поле поставить крестик',
            reply_markup=keyboards.GameKeyboard.makeKeyboard(character)
        )
        self.delFieldImage()

    def message_edit(self, c, **kwargs):
        # если это не сообщение перед победой, то надо отобразить клавиатуру
        if len(kwargs) != 0:
            keyboard = keyboards.GameKeyboard.makeKeyboard(kwargs['character'])
        else:
            keyboard = False

        self.bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(open('pol2.jpg', 'rb')),
            reply_markup=keyboard
        )
        self.delFieldImage()

    def getCurrentClient(self, client_chat_id: str) -> Client:
        for client in self.__clientlist:
            if client.getChat_id() == client_chat_id:
                return client
        return False

    def getCurrentGame(self, chat_id: str):
        for game in self.__gamelist:
            if chat_id == game._players_list['X'].getChat_id() or \
                chat_id == game.players_list['O'].getChat_id():
                return game
        return False

    # удаляет игру для клиента
    def delCurrentGame(self, chat_id: str):
        try:
            client = self.getCurrentClient(chat_id)
            client.delGame()
        except:
            
            print('Нет начатых игр')

    # производит очистку временных файлов игры и убирает клавиатуру в чате
    def killGame(self, c, message_text: str):        
        self.message_edit(c)
        self.message_send(c, message_text)
        self.delCurrentGame(c.message.chat.id)

entireBot = EntireBot(telegramBotToken.token)

if __name__ == '__main__':
    entireBot.bot.set_update_listener(entireBot.messageListener)
    entireBot.setCallBack()
    entireBot.bot.infinity_polling()