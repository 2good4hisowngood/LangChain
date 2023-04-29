FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
CMD ["sh", "-c", "python app.py"]