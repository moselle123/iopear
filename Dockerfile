FROM node:18 AS frontend_build
WORKDIR /application

COPY package.json package-lock.json vite.config.js ./
COPY vite/ ./vite
RUN npm install
RUN npm run build

FROM python:3.10 AS backend
WORKDIR /application

RUN apt-get update && \
	apt-get install -y libi2c-dev i2c-tools python3-smbus && \
	rm -rf /var/lib/apt/lists/*

COPY /backend/run.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /backend/app ./app
COPY --from=frontend_build /application/templates ./app/templates

EXPOSE 5000

CMD ["python", "run.py"]
