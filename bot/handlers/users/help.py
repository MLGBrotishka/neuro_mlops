from aiogram import types
from loader import dp

@dp.message_handler(text='/help')
async def command_start(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}! \n'
                         f'Этот бот создаст для тебя картинку по твоему описанию.\n'
                         f'Для этого воспользуйся командой /txt2img.\n '
                         f'Помни, что делать свой запрос нужно на английском языке')

    print('Из help ', message.from_user.id)