import random
from .field import Field

class GameBot():
    char:str = None

    def __init__(self, char:str) -> None:
        self.char = char

    def move(field:list, chars:dict) -> int:
        is_right = False
        turn = 0
        chars_str = ''.join(list(chars))
        while not is_right:
            turn = random.randint(0,8)
            if field[turn] not in chars_str:
                is_right = True
        return turn