FROM node:stretch-slim

WORKDIR /app

COPY . .

RUN npm install && npm run build && npm install -g serve

CMD ["npx", "serve", "-s", "-l", "5000", "build"]

EXPOSE 5000