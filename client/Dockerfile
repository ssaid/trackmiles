FROM node:19-alpine3.16

RUN mkdir -p /app
WORKDIR /app

COPY . /app

EXPOSE 3000

ENTRYPOINT ["/bin/sh", "-c" , "yarn && yarn dev"]
