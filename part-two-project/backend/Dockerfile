FROM golang:alpine3.13

WORKDIR /app

COPY . .

RUN go build

CMD ./server

EXPOSE 8080