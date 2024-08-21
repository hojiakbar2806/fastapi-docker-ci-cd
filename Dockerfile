# Python 3.12 imajidan foydalanamiz
FROM python:3.12

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

# Gunicorn serverini ishga tushiramiz
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
