FROM python:3.11-slim

WORKDIR /usr/src/app/bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# agar aiogram3, aiohttp, python-dotenv va h.k. bo'lsa requirements.txt ga qo'shilgan bo'lsin
CMD ["python", "-m", "bot"]
