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
    InlineKeyboardButton('❌',callback_data='one'),
    InlineKeyboardButton('❌',callback_data='two'),
    InlineKeyboardButton('❌',callback_data='three'),
    InlineKeyboardButton('❌',callback_data='four'),
    InlineKeyboardButton('❌',callback_data='five'),
    InlineKeyboardButton('❌',callback_data='six'),
    InlineKeyboardButton('❌',callback_data='seven'),
    InlineKeyboardButton('❌',callback_data='eight'),
    InlineKeyboardButton('❌',callback_data='nine')
)
