import os
import botfunc
import keyboards
import gamefunc
import testimages


class GameExceptions(Exception):
    def __init__(self, text):
        self.text = text
