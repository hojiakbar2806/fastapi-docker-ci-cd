# Python 3.12 imajidan foydalanamiz
FROM python:3.12-slim

# Muhit o'zgaruvchilarini sozlash
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV DEBUG=False

# /app papkasini yaratamiz
RUN mkdir /app  

# Ishchi papkani sozlash
WORKDIR /app

# Talab qilinadigan paketlarni o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Manba fayllarini nusxalaymiz
COPY . .

# Alembic migratsiyalarini bajarish
RUN alembic upgrade head

# Gunicorn serverini ishga tushiramiz
CMD ["gunicorn", "main:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker"]
