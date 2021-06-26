import telebot
import keyboards
import gamefunc
import gamemanager
import telegramBotToken
from telebot.types import InlineKeyboardMarkup, Message

class EntireBot():
    bot:telebot.TeleBot
    __game = None
    __player_list = []

    start_keyboard = keyboards.StartKeyboard.makeKeyboard()
    priority_keyboard = keyboards.PriorityKeyboard.makeKeyboard()

    def __init__(self, token:str):
        self.bot = telebot.TeleBot(token)
        

    def startCommand(self, message):
        self.bot.send_message(
            message.chat.id,
            'Нажми "/newgame"'
        )  

    def messageListener(self, messages:list):
        message = messages[0]
        if not(message.chat.id in self.__player_list):
            self.__player_list.append(message.chat.id)
        if message.text == '/start':
            self.startCommand(message)
        if message.text == '/newgame':
            self.newGame(message)

    def newGame(self, message):
        self.bot.send_message(
            message.chat.id,
            'Выберете режим игры:  ',
            reply_markup=self.start_keyboard
        )
        
    def setCallBack(self):
        @self.bot.callback_query_handler(func=lambda c:True)
        def inline(c):

            if c.data == 'mode_single':
                self.__game = gamefunc.SingleGame()
                self.__game.modeDefined(c.data)   
                self.message_send(
                    c,
                    'Выберите, за кого хотите играть',
                    keyboard=self.priority_keyboard
                )
            elif c.data == 'cross':
                self.__game.characterDefined(c.message.chat.id,'X')
                self.__game.startGame()
                self.photo_send(c, 'X')
            elif c.data == 'zero':
                self.__game.characterDefined(c.message.chat.id,'O')
                self.__game.startGame()
                self.__game.moveMade(c)
                self.photo_send(c, 'O', 'pol2.jpg')
            elif (c.data in self.__game.getPointPositions()):
                self.__game.moveMade(c)


    def message_send(self, c, text, keyboard=False):
        self.bot.send_message(c.message.chat.id, text, reply_markup=keyboard)


    def photo_send(self, c, character:str, image='pol.jpg'):
        self.bot.send_photo(
            c.message.chat.id,
            photo=open(image, 'rb'),
            caption='Выберете на клавиатуре, в какую клетку на поле поставить крестик',
            reply_markup=keyboards.GameKeyboard.makeKeyboard(character)
        )

    def message_edit(self, c, **kwargs):
        # если это не сообщение перед победой, то надо отображить клавиатуру
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
   
entireBot = EntireBot(telegramBotToken.token)

if __name__ == '__main__':
    entireBot.bot.set_update_listener(entireBot.messageListener)
    entireBot.setCallBack()
    entireBot.bot.infinity_polling()