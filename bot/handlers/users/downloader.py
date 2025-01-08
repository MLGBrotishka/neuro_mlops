from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, InputFile
from states import txt2img

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


@dp.message_handler(Command('txt2img'))
async def txt2img_(message: Message):
    await message.answer('Введите описание изображения')
    await txt2img.state1.set()


@dp.message_handler(state=txt2img.state1)
async def state1(message: Message, state: FSMContext):
    text = message.text
    message_id = message.message_id
    chat_id = message.from_user.id
    producer = AIOKafkaProducer(bootstrap_servers='broker:29090')
    consumer = AIOKafkaConsumer('client', bootstrap_servers='broker:29090')
    await producer.start()
    await consumer.start()
    key = bytes(str(chat_id), encoding='utf-8')
    value_send = str(message_id) + ' ' + text
    value_send = bytes(value_send, encoding='utf-8')
    await producer.send_and_wait('server', key=key, value=value_send)
    await state.finish()
    await message.answer('Ваш запрос обрабатывается')
    async for message in consumer:
        if message.key == key:
            path_to_file = message.value.decode("utf-8")
            break
    await dp.bot.send_photo(chat_id=chat_id, photo=path_to_file)
    await producer.stop()
    await consumer.stop()
