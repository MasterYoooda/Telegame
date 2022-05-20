class Error(Exception):
    """Base error class"""
    pass


class GameStatus(Exception):
    """Game status base class"""
    line:list=None


class CellIsOccupied(Error):
    """Called when trying to write to an occupaied cell"""    
    def __str__(self) -> str:
        return "Cell is occupied!"


class CharIsOccupied(Error):
    """Called when player trying to select already 
    occupied in game char
    """
    def __init__(self, char:str) -> None:
        self.char = char
        super().__init__(char)

    def __str__(self) -> str:
        return f'{self.char} is occuppied!'


class TurnQueueError(Error):
    """Called when trying to make a move in wrong queue"""
    def __str__(self) -> str:
        return "Trying ot make a move out of turn!"


class WrongCommandName(Error):
    """Called when trying to process non-existent command"""
    def __init__(self, command:str) -> None:
        self.command = command
        super().__init__(command)

    def __str__(self) -> str:
        return f'Wrong command: {self.command}'


class NonExistentEvent(Error):
    """Called when trying to process non-existed event for keyboard"""
    def __init__(self, text:str) -> None:
        self.text = text
        super().__init__(text)

    def __str__(self) -> str:
        return f'Wront Event Name: {self.text}'


class NoClientInBase(Error):
    """Called when storage hasn't client with requested chat_id"""
    def __init__(self, chat_id:str) -> None:
        self.chat_id = chat_id
        super().__init__(chat_id)

    def __str__(self):
        return f'No Client with chat_id:{self.chat_id}'


class Win(GameStatus):
    """Called when the game has it's winner
    
    Attributes: 
        char: player character
        status: player game status
    """
    def __init__(self, char:str, line:list, status="won!") -> None:
        self.char = char
        self.line = line
        self.status = status
        super().__init__(char, line, status)

    def __str__(self) -> str:
        return f'{self.char} {self.status}'


class Draw(GameStatus):
    """Called when the game is a draw"""
    def __str__(self) -> str:
        return "Draw!"