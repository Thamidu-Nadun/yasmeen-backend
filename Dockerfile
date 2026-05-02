FROM mcr.microsoft.com/playwright/python:v1.59.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/pdf /app/instance

EXPOSE 5000

CMD ["python", "app.py"]