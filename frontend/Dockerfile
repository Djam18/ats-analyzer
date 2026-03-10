# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Stage 2: Production ───────────────────────────────────────────────────────
FROM node:20-alpine AS production

WORKDIR /app

COPY --from=builder /app/.output ./

EXPOSE 3000

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

CMD ["node", "server/index.mjs"]
