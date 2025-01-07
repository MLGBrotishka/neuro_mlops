from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Cоздаем переменную бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Создаём хранилище оперативной памяти
storage = MemoryStorage()

# Создаём диспетчер
dp = Dispatcher(bot, storage=storage)

