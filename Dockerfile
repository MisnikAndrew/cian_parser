FROM python:3.8
WORKDIR /app
COPY requirements.txt src /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "telegram_bot.py"]