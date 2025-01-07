FROM python

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir diffusers transformers accelerate scipy safetensors
RUN pip install --no-cache-dir kafka-python-ng
RUN pip install --no-cache-dir images-upload-cli
    
#RUN apt install nvidia-cudnn

WORKDIR /server/

COPY . .

CMD ["python3", "Server.py"]