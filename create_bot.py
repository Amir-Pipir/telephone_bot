from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage

TOKEN = ''

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
