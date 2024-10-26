FROM python:3.10-slim
WORKDIR /iopear
COPY . /iopear

RUN npm install
RUN pyhton3 install -r requirements.txt
EXPOSE 3000
