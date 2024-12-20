# 1. stage: build
FROM node:20.13.1 as builder

WORKDIR /workspace

COPY package.json package-lock.json ./
RUN npm install

COPY .env .eslintrc.cjs .prettierrc.json index.html jsconfig.json tsconfig.json vite.config.js vue.config.js ./
COPY public ./public
COPY src ./src
RUN npm run build

# 2. stage: runtime ------------------------------------------------------------
FROM nginx:1.27.0

WORKDIR /opt/app
EXPOSE 8000

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /workspace/dist /opt/app/
