FROM node:14 AS frontend-build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install
RUN npm run build

COPY templates/ ./templates

FROM python:3.10 AS backend
WORKDIR /app

RUN apt-get update && \
    apt-get install -y libi2c-dev i2c-tools python3-smbus && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /backend .

EXPOSE 5000

CMD ["python3", "app.py"]
