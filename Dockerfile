FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY static/ /app/static/
COPY templates/ /app/templates/

EXPOSE 5000

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ARG SERPAPI_API_KEY
ENV SERPAPI_API_KEY=$SERPAPI_API_KEY
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
