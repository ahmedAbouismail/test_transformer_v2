FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    ENV=development

EXPOSE 8000

CMD ["uvicorn", "app.api.v1.endpoints.text_structuring:router", "--reload", "--host", "0.0.0.0", "--port", "8000"]
