import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

start_keyboard = InlineKeyboardMarkup()
start_keyboard.add(
    InlineKeyboardButton("Игра с компьютером",callback_data='mode_single'),
    InlineKeyboardButton("Игра с другим игроком",callback_data='mode_multi')
)
game_keyboard = InlineKeyboardMarkup()
game_keyboard.add(
    InlineKeyboardButton('0',callback_data='zero'),
    InlineKeyboardButton('1',callback_data='one'),
    InlineKeyboardButton('2',callback_data='two'),
    InlineKeyboardButton('3',callback_data='three'),
    InlineKeyboardButton('4',callback_data='four'),
    InlineKeyboardButton('5',callback_data='five'),
    InlineKeyboardButton('6',callback_data='six'),
    InlineKeyboardButton('7',callback_data='seven'),
    InlineKeyboardButton('8',callback_data='eight'),
    InlineKeyboardButton('9',callback_data='nine')
)
