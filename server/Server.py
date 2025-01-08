import os
import requests
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.wuerstchen import DEFAULT_STAGE_C_TIMESTEPS
import torch
from kafka import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

FILE_IO_TOKEN = str(os.getenv("FILE_IO_TOKEN"))
file_io_url = f"https://api.imgbb.com/1/upload?expiration=600&key={FILE_IO_TOKEN}"


def upload_image(image_name):
    with open(image_name, 'rb') as file:
        files = {
            'image': (image_name, file, "multipart/form-data")
        }

        response = requests.post(file_io_url, files=files)
    return response.json()["data"]["url"]


path_to_upper = '.'
path_to_media = "/media/"

model_id = "warp-ai/wuerstchen"

pipe = AutoPipelineForText2Image.from_pretrained(model_id)
pipe = pipe.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

producer = KafkaProducer(bootstrap_servers='broker:29090')
consumer = KafkaConsumer('server', bootstrap_servers='broker:29090')
for msg in consumer:
    print(msg)
    print(msg.key)
    print(msg.value)
    msg_text = msg.value.decode("utf-8")
    id_to_send = msg.key.decode("utf-8")
    message_id = msg_text.split(" ", 1)[0]
    prompt = msg_text.split(" ", 1)[1]
    image = pipe(
        prompt,
        height=256,
        width=256,
        prior_timesteps=DEFAULT_STAGE_C_TIMESTEPS,
        prior_guidance_scale=4.0,
        num_images_per_prompt=1
    ).images[0]
    print("gen image success!")
    image_name = path_to_upper + path_to_media + id_to_send + "-" + message_id + ".png"
    if not os.path.exists(path_to_upper + path_to_media):
        os.makedirs(path_to_upper + path_to_media)
    image.save(image_name)
    print("image save as " + image_name, flush=True)

    image_url = upload_image(image_name)

    image_url = bytes(image_url, encoding='utf-8')
    producer.send('client', key=msg.key, value=image_url)
    producer.flush()
