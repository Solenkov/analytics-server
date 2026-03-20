FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV DB_HOST=analytics-db
ENV DB_PORT=5432
ENV DB_NAME=bfh_analytics
ENV DB_USER=analytics
ENV DB_PASSWORD=analytics_pass

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
