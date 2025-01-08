import logging
from aiogram import types
from loader import dp

logger = logging.getLogger(__name__)


@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}! \n'
                         f'Бот активирован')

    logger.info("start command for %s", message.from_user.id)
