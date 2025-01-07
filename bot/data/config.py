import os   # библиотека для работы с ОС
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins_id = map(int, os.getenv("ADMIN_IDS").split(","))
