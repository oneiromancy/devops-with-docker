FROM node:14

WORKDIR /usr/app

COPY . .

RUN npm ci && npm run build

CMD ["npm", "start"] 

EXPOSE 3000