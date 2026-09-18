FROM mcr.microsoft.com/playwright/python:v1.59.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser

WORKDIR /app

RUN chown -R appuser:appuser /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/pdf /app/instance

EXPOSE 5000

USER appuser

CMD ["python", "app.py"]