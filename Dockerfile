FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "api.app:app", "--no-access-log", "--host", "0.0.0.0", "--port", "8080", "--workers", "2", "--proxy-headers"]
