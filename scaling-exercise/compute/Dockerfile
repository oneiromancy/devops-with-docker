FROM node:14

WORKDIR /usr/app

COPY . .

RUN npm ci

CMD ["node", "./index.js"] 

EXPOSE 3000