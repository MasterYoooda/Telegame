from itertools import count
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from abc import ABC, abstractmethod


class KeyboardCreator(ABC):
    """Base keyboard creator class"""
    @abstractmethod
    def make(self) -> InlineKeyboardMarkup:
        """Generating an InlineKeyboardMarkup object"""


class GameSelectionKeyboard(KeyboardCreator):
    def make(*args) -> InlineKeyboardMarkup:
        start_keyboard = InlineKeyboardMarkup()
        start_keyboard.add(
                InlineKeyboardButton(text='Single', callback_data='mode_single'),
                InlineKeyboardButton(text='Multi', callback_data='mode_multi')
        )
        return start_keyboard


class CharSelectionKeyboard(KeyboardCreator):
    def make(*args) -> InlineKeyboardMarkup:
        priority_keyboard = InlineKeyboardMarkup()
        priority_keyboard.add(
                InlineKeyboardButton(text='❌',callback_data='cross'),
                InlineKeyboardButton(text='⭕️',callback_data='zero')
        )
        return priority_keyboard


class GameKeyboard(KeyboardCreator):     
    def make(emoji:str) -> InlineKeyboardMarkup:
        # emoji = '❌' if char == 'X' else '⭕️'
        game_keyboard = InlineKeyboardMarkup()
        game_keyboard.add(
                *[InlineKeyboardButton(text=emoji,callback_data=str(i)) for i in range(9)]
        )
        return game_keyboard
