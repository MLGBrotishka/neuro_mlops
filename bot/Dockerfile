FROM python

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -U aiogram \
    pip install --no-cache-dir python-dotenv \
    pip install --no-cache-dir kafka-python

WORKDIR /bot/

COPY . .

CMD ["python3", "app.py"]