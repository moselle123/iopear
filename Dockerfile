FROM node:18 AS frontend_build
WORKDIR /app

COPY package.json package-lock.json vite.config.js ./
COPY vite/ ./vite
RUN npm install
RUN npm run build

FROM python:3.10 AS backend
WORKDIR /app

RUN apt-get update && \
    apt-get install -y libi2c-dev i2c-tools python3-smbus && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY /backend .
COPY --from=frontend_build /app/templates /app/templates

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
