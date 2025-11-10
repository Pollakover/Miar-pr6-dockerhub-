FROM python:3.10-slim

WORKDIR /app

# Копируем requirements.txt из корня репозитория
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем папку notification_service (включая вложенную папку app)
COPY ./notification_service /app/

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]