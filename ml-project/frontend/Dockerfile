FROM node:stretch-slim

WORKDIR /usr/src/app

COPY . .

RUN npm ci && npm run build && npm install -g serve

CMD ["serve", "-s", "-l", "3000", "build"]