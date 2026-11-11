FROM node:20-alpine AS build
WORKDIR /app
ARG VITE_WINDY_MAP_API_KEY=""
ENV VITE_WINDY_MAP_API_KEY=${VITE_WINDY_MAP_API_KEY}
COPY viz/frontend/package*.json ./
RUN npm ci
COPY viz/frontend/ ./
RUN npm run build -- --outDir dist

FROM nginx:1.27-alpine AS runtime
COPY infra/docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -qO- http://127.0.0.1/ >/dev/null
EXPOSE 80
