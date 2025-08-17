FROM python:3.11-slim

WORKDIR /usr/src/app/bot

# faqat requirementsni avval ko'chirib install qilamiz (cache uchun)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# endi qolgan kodni ko'chiramiz
COPY . .

CMD ["python", "-m", "bot"]
