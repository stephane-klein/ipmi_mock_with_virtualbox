FROM golang:1.10

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y bash-completion

# Makefile completion
RUN apt-get install -y bash-completion && \
    echo ". /etc/bash_completion" >> /root/.bashrc

RUN mkdir /code/
WORKDIR /code/
ENV GOPATH=/code/
ENV GOBIN=/usr/local/bin/

RUN go get -v -u github.com/spf13/cobra/cobra && \
    go get -v -u github.com/mitchellh/gox

ENV GOBIN=/code/bin/
ENV PATH=/code/bin/:$PATH
