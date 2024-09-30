FROM node:20-slim  AS build

WORKDIR /app
RUN corepack enable

COPY package.json .
RUN pnpm install

COPY . .
RUN pnpm run build

FROM node:20-slim  AS runtime
COPY --from=build /app/dist /app
EXPOSE 3000
RUN npm install -g serve
CMD [ "serve", "-s", "/app" ]
