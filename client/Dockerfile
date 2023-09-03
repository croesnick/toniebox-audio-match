# ./client/Dockerfile
FROM node:14.7-stretch

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "serve"]