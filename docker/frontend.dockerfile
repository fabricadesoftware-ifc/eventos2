FROM node:14-buster AS builder

WORKDIR /src
COPY frontend/ .
COPY docker/frontend.checks CHECKS

RUN NODE_ENV= npm ci
RUN npm run build

RUN rm -rf node_modules && \
    npm ci --only=production


FROM node:14-alpine

WORKDIR /src
COPY --from=builder /src .

ENV HOST=0.0.0.0
CMD [ "npm", "run", "start" ]
