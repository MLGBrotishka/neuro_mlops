FROM python

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -U "aiogram==2.14.2"
RUN pip install --no-cache-dir python-dotenv
RUN pip install --no-cache-dir kafka-python-ng

WORKDIR /bot/

COPY . .

CMD ["python3", "app.py"]