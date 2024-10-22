from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

BOT_TOKEN = "7550581791:AAGZPIcotSYM1_3kPJQe-h1I2kQClUzf5SE"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)