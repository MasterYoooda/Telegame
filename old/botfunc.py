import telebot
import os

from bot.keyboards import GameKeyboard, StartKeyboard, PriorityKeyboard
import old.gamemanager as gamemanager
import tictactoe.testimages as testimages

import telegramBotToken as telegramBotToken


class EntireBot():
    bot:telebot.TeleBot
    __clientlist = []

    start_keyboard = StartKeyboard.makeKeyboard()
    priority_keyboard = PriorityKeyboard.makeKeyboard()

    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)       

    def startCommand(self, message):
        self.bot.send_message(
            message.chat.id,
            'Нажми "/newgame"'
        ) 

    def messageListener(self, messages:list):
        message = messages[0]
        # If the client writes for the first time, we remember it
        if not (self.getCurrentClient(message.chat.id)):
            self.__clientlist.append(
                gamemanager.Client(message.chat.id, message.message_id)
            )
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
                self.photo_send(client.choose_character(c))
            if c.data in client.get_game().getPointPositions():
                game = client.get_game()
                self.checkMoveOutput(game.moveMade(c), c, client)

    # Processing the game log
    def checkMoveOutput(self, move_output: str, c, client: gamemanager.Client):
        if not(move_output) or 'выполнен!' in move_output.text:
            self.makeImage(client.getGame().getFieldMap(), client.getGame().getPointPositions())
            self.message_edit(c, character=client.getGame().getCharacter(c)) 
            return
        if 'Победил!' in move_output.text or 'Ничья!' in move_output.text:
            self.killGame(c, move_output)
        if 'занята!' in move_output.text:
            self.message_send(c, move_output)

    def message_send(self, c, text, keyboard=False):
        self.bot.send_message(c.message.chat.id, text, reply_markup=keyboard)

    def makeImage(self, fieldMap: list, point_positions: dict):
        testimages.MakeImage().image_draw(fieldMap, point_positions)
    
    # No longer in use
    def delFieldImage(self):
        try:
            os.remove('pol2.jpg')
        except:
            print(gamemanager.GameExceptions('нет файла с полем'))

    def photo_send(self, params: tuple):
        client = params[0] 
        character = params[1]
        image = params[2] if len(params) > 2 else 'pol.jpg'

        self.makeImage(client.getGame().getFieldMap(), client.getGame().getPointPositions())
        self.bot.send_photo(
            client.getChat_id(),
            photo=open(image, 'rb'),
            caption='Выберете на клавиатуре, в какую клетку на поле поставить крестик',
            reply_markup= GameKeyboard.makeKeyboard(character)
        )
        self.delFieldImage()

    def message_edit(self, c, **kwargs):
        # If not win in kwargs - showing keyboard
        keyboard = GameKeyboard.makeKeyboard(kwargs['character']) if len(kwargs) != 0 else False
        # editing the message with current map
        self.bot.edit_message_media(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            media=telebot.types.InputMediaPhoto(open('pol2.jpg', 'rb')),
            reply_markup=keyboard
        )
        self.delFieldImage()

    # Returns game-client instance or False, if id isn't found 
    def getCurrentClient(self, client_chat_id: str) -> gamemanager.Client:
        for client in self.__clientlist:
            if client.getChat_id() == client_chat_id:
                return client
        return False

    # Cleans the temporary files of the game and removes the keyboard
    def killGame(self, c, message_text: str):        
        self.message_edit(c)
        self.message_send(c, message_text)
        self.getCurrentClient(c.message.chat.id).delCurrentGame()


entireBot = EntireBot(telegramBotToken.token)

if __name__ == '__main__':
    entireBot.bot.set_update_listener(entireBot.messageListener)
    entireBot.setCallBack()
    entireBot.bot.infinity_polling()