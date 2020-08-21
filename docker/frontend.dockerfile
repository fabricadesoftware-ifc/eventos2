FROM node:14-buster AS builder

ARG EVENTOS2_FRONTEND_DEBUG

WORKDIR /src
COPY frontend/ .
COPY docker/production/frontend.checks CHECKS
COPY docker/production/frontend.nginx.conf.sigil nginx.conf.sigil

RUN NODE_ENV= npm ci
RUN npm run build

RUN rm -rf node_modules && \
    npm ci --only=production


FROM node:14-alpine

WORKDIR /src
COPY --from=builder /src .

ENV HOST=0.0.0.0
CMD [ "npm", "run", "start" ]
