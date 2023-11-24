from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from handlers.ca_action import lang_setter

TOKEN = "6584358137:AAGktKClTebUEPl6t8Q6POFS7sbmlDwhcH4"
# language = lang_setter()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()