FROM python:3.10-slim

WORKDIR /app

COPY . .
COPY wheels /wheels

RUN pip install --no-cache-dir --find-links=/wheels -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
