from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from abc import ABC, abstractmethod

class KeyboardCreator(ABC):
    @abstractmethod
    def makeKeyboard(self) -> InlineKeyboardMarkup:
        pass


class StartKeyboard(KeyboardCreator):
    def makeKeyboard() -> InlineKeyboardMarkup:
        start_keyboard = InlineKeyboardMarkup()
        start_keyboard.add(
            InlineKeyboardButton("Игра с компьютером",callback_data='mode_single'),
            InlineKeyboardButton("Игра с другим игроком",callback_data='mode_multi')
        )
        return start_keyboard


class PriorityKeyboard(KeyboardCreator):
    def makeKeyboard() -> InlineKeyboardMarkup:
        priority_keyboard = InlineKeyboardMarkup()
        priority_keyboard.add(
            InlineKeyboardButton('"Крестики"',callback_data='cross'),
            InlineKeyboardButton('"Нолики"',callback_data='zero')
        )
        return priority_keyboard


class GameKeyboard(KeyboardCreator):
    def makeKeyboard(character:str) -> InlineKeyboardMarkup:
        emoji = '❌' if character == 'X' else '⭕️'
        game_keyboard = InlineKeyboardMarkup()
        game_keyboard.add(
            InlineKeyboardButton(emoji,callback_data='0'),
            InlineKeyboardButton(emoji,callback_data='1'),
            InlineKeyboardButton(emoji,callback_data='2'),
            InlineKeyboardButton(emoji,callback_data='3'),
            InlineKeyboardButton(emoji,callback_data='4'),
            InlineKeyboardButton(emoji,callback_data='5'),
            InlineKeyboardButton(emoji,callback_data='6'),
            InlineKeyboardButton(emoji,callback_data='7'),
            InlineKeyboardButton(emoji,callback_data='8')
        )
        return game_keyboard
