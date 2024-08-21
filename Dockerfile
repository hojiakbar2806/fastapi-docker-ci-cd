FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV DEBUG=False

RUN mkdir /app  

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker
