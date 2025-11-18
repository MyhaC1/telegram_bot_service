FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

RUN useradd -m botuser
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app

RUN chown -R botuser:botuser /app
USER botuser

ENV PYTHONUNBUFFERED=1
EXPOSE 8002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
