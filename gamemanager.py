import gamefunc


class GameExceptions(Exception):
    def __init__(self, text):
        self.text = text


class Client:
    def __init__(self, chat_id: str, message_id: str):
        self._chat_id = chat_id
        self._message_id = message_id
        self._game = None
    
    def setGame(self, game_mode: str):
        if game_mode == 'mode_single':
            self._game = gamefunc.SingleGame(game_mode)
            # self._game.modeDefined(game_mode)

    def getGame(self):
        return self._game

    def delGame(self):
        self._game = None

    def getChat_id(self):
        return self._chat_id

    # Character selection events
    def chooseCharacter(self, c):
        if c.data == 'cross':
            self.getGame().characterDefined(c.message.chat.id,'X')
            self.getGame().startGame()
            return self, 'X'
        elif c.data == 'zero':
            self.getGame().characterDefined(c.message.chat.id,'O')
            self.getGame().startGame()
            # print(self.getGame().moveMade(c))
            return self, 'O', 'pol2.jpg'

    def getCurrentGame(self, chat_id: str):
        for game in self.__gamelist:
            if chat_id == game._players_list['X'].getChat_id() or \
                chat_id == game.players_list['O'].getChat_id():
                return game
        return False

    # Deletes all games for the client
    def delCurrentGame(self):
        try:
            self.delGame()
        except:
            print('Нет начатых игр')