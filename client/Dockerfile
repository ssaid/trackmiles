FROM node:19-alpine3.16

# ENV NODE_ENV development
# Crear un directorio para la aplicación
RUN mkdir -p /app
WORKDIR /app

# Copiar el código fuente de la aplicación
COPY . /app

# Instalar las dependencias
EXPOSE 3000

RUN yarn

CMD ["yarn", "dev"]
