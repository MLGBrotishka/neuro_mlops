import os
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from kafka import KafkaProducer, KafkaConsumer
#path_to_upper = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
path_to_upper = '.'
path_to_media = "/media/"

model_id = "stabilityai/stable-diffusion-2-1-base"

scheduler = EulerDiscreteScheduler.from_pretrained(pretrained_model_name_or_path = model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
pipe = pipe.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

producer = KafkaProducer(bootstrap_servers='broker:29090')
consumer = KafkaConsumer('server',bootstrap_servers='broker:29090')
for msg in consumer:
    print(msg)
    print(msg.key)
    print(msg.value)
    msg_text = msg.value.decode("utf-8")
    id_to_send = msg.key.decode("utf-8")
    message_id = msg_text.split(" ", 1)[0]
    prompt = msg_text.split(" ", 1)[1]
    image = pipe(prompt).images[0]
    image_name =path_to_upper + path_to_media + id_to_send + "-" + message_id + ".png"
    if not os.path.exists(path_to_upper + path_to_media): 
        os.makedirs(path_to_upper + path_to_media) 
    image.save(image_name)
    comand = "images-upload-cli -h filecoffee " + image_name
    stream = os.popen(comand)
    output = stream.read()
    print(output)
    image_name = bytes(output, encoding='utf-8')
    producer.send('client',key=msg.key,value=image_name)
    producer.flush()