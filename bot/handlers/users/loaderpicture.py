from aiogram import Bot, Dispatcher, executor, types
from loader import dp


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Напишите что-нибудь')