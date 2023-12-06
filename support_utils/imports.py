from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from handlers.ca_action import lang_setter

TOKEN = "6828509461:AAHg8Y2VRY3AjwOm8aa8nE0MD_Qg29v3iCA"
# language = lang_setter()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()