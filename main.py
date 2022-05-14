import telebot, telegramBotToken as t
from controller.controller import Controller
from controller.clientcontroller import ClientController
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
os.path.join(BASE_DIR)

bot = telebot.TeleBot(t.token)
client_controller = ClientController()
main_controller = Controller(bot, client_controller)
main_controller.start()