import os
import io
import requests
import logging
from kafka import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv

from pipeline import gen_image

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

FILE_IO_TOKEN = str(os.getenv("FILE_IO_TOKEN"))
file_io_url = f"https://api.imgbb.com/1/upload?expiration=600&key={FILE_IO_TOKEN}"


def upload_image(image_name, image_bytes):
    files = {
        'image': (image_name, image_bytes, "multipart/form-data")
    }

    response = requests.post(file_io_url, files=files)
    return response.json()["data"]["url"]


PATH_TO_MEDIA = "./media/"


def start():
    if not os.path.exists(PATH_TO_MEDIA):
        os.makedirs(PATH_TO_MEDIA)
    logger.info("Started")
    producer = KafkaProducer(bootstrap_servers='broker:29090')
    consumer = KafkaConsumer('server', bootstrap_servers='broker:29090')
    for msg in consumer:
        logger.info("new message %s", msg.value)
        msg_text = msg.value.decode("utf-8")
        message_id = msg_text.split(" ", 1)[0]
        prompt = msg_text.split(" ", 1)[1]
        image = gen_image(prompt)
        byte_buffer = io.BytesIO()
        image.save(byte_buffer, format='PNG')
        image_bytes = byte_buffer.getvalue()
        image_url = upload_image(message_id+".png", image_bytes)
        image_url = bytes(image_url, encoding='utf-8')
        producer.send('client', key=msg.key, value=image_url)
        producer.flush()
        logger.info("successful handling for %s", msg.value)


if __name__ == "__main__":
    start()
