import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


start_keyboard = InlineKeyboardMarkup()
start_keyboard.add(
    InlineKeyboardButton("Игра с компьютером",callback_data='mode_single'),
    InlineKeyboardButton("Игра с другим игроком",callback_data='mode_multi')
)


priority_keyboard = InlineKeyboardMarkup()
priority_keyboard.add(
    InlineKeyboardButton('"Крестики"',callback_data='cross'),
    InlineKeyboardButton('"Нолики"',callback_data='zero')
)


game_keyboard = InlineKeyboardMarkup()
game_keyboard.add(
    InlineKeyboardButton('❌',callback_data='0'),
    InlineKeyboardButton('❌',callback_data='1'),
    InlineKeyboardButton('❌',callback_data='2'),
    InlineKeyboardButton('❌',callback_data='3'),
    InlineKeyboardButton('❌',callback_data='4'),
    InlineKeyboardButton('❌',callback_data='5'),
    InlineKeyboardButton('❌',callback_data='6'),
    InlineKeyboardButton('❌',callback_data='7'),
    InlineKeyboardButton('❌',callback_data='8')
)
