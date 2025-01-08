import os

import torch
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.wuerstchen import DEFAULT_STAGE_C_TIMESTEPS

from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "warp-ai/wuerstchen"
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT"))
NEGATIVE_PROMPT = str(os.getenv("NEGATIVE_PROMPT"))

pipe = AutoPipelineForText2Image.from_pretrained(MODEL_ID)
pipe = pipe.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))


def gen_image(prompt):
    return pipe(
        prompt,
        height=IMAGE_HEIGHT,
        width=IMAGE_WIDTH,
        prior_timesteps=DEFAULT_STAGE_C_TIMESTEPS,
        prior_guidance_scale=4.0,
        num_images_per_prompt=1,
        negative_prompt=NEGATIVE_PROMPT
    ).images[0]
