from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage

TOKEN = '6322604539:AAHgdvMA9xtEhoj4Qnr7U8efb3wJLGc1BzU'

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
