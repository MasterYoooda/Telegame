from keyboards import GameKeyboard, StartKeyboard, PriorityKeyboard
import testimages
import telegramBotToken
from game import Single

class Handler():

    def __init__(self, bot) -> None:
        self._bot = bot
        
    def onStart_command(bot, chat_id:str) -> None:
        bot.send_message(chat_id, 'Нажми "/newgame"')

    def onNew_game(bot, chat_id:str) -> None:
        bot.send_message(chat_id,
                        'Выберите режим игры:',
                        reply_markup=StartKeyboard.make())

    def get_command(command:str):
        if command == '/start' or \
                command == '/start@Telgames_bot':
            return Handler.onStart_command
        elif command == '/newgame' or \
                command == '/newgame@Telgames_bot':
            return Handler.onNew_game
        else:
            raise ValueError(command)

    def message_handler(bot, client, chat_id:str, message:str):
        if message == 'mode_single':
            game = Single()
            client.set_game(game)
            bot.send_message(chat_id,
                             'Выберете, за кого играть',
                             PriorityKeyboard.make()
                            )
        if message == 'cross' or message == 'zero':
            pass
             