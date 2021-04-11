FROM ubuntu:latest

COPY . .

ENV PATH /usr/local/go/bin:$PATH
ENV REQUEST_ORIGIN http://localhost:5000

RUN apt-get update && apt-get install -y wget gcc && rm -rf /usr/local/go && wget -c https://golang.org/dl/go1.16.3.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz && go build && go test && useradd -m appuser

USER appuser

CMD ./server

EXPOSE 8080