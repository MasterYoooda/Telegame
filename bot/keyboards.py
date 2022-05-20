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
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
                InlineKeyboardButton(text='Single', callback_data='mode_single'),
                InlineKeyboardButton(text='Multi', callback_data='mode_multi')
        )
        return keyboard


class CharSelectionKeyboard(KeyboardCreator):
    def make(*args) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
                InlineKeyboardButton(text='❌', callback_data='cross'),
                InlineKeyboardButton(text='⭕️', callback_data='zero')
        )
        return keyboard


class GameKeyboard(KeyboardCreator):     
    def make(emoji:str) -> InlineKeyboardMarkup:
        # emoji = '❌' if char == 'X' else '⭕️'
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
                *[InlineKeyboardButton(text=emoji, callback_data=str(i)) for i in range(9)]
        )
        return keyboard
