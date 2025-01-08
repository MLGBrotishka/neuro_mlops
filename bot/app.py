import logging

from aiogram import executor
from handlers import dp
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)

    logger.info("Bot started")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
