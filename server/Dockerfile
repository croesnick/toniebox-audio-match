# ./server/Dockerfile
FROM python:3.8-buster

WORKDIR /backend

COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y ffmpeg && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "app.py"]