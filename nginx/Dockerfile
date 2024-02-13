ARG NODE_VERSION=20.10.0
ARG NGINX_VERSION=1.25.3

FROM node:${NODE_VERSION}-alpine as build

WORKDIR /app
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./

RUN npm install
COPY ./frontend .
RUN npm run build

FROM nginx:${NGINX_VERSION}
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
