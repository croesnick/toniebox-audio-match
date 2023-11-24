# ./server/Dockerfile
FROM python:3.8-buster as base

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

################ START NEW IMAGE: DEBUG #######################
FROM base as debug

CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000

################ START NEW IMAGE: PROD #######################
FROM base as prod

CMD flask run -h 0.0.0.0 -p 5000