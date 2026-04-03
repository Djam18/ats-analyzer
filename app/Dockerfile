# ── Stage 0 : Dev ────────────────────────────────────────────────────────────
FROM node:20-alpine AS dev

WORKDIR /app

EXPOSE 3000

ENV HOST=0.0.0.0
ENV PORT=3000

# npm install + start lancés par docker-compose

# ── Stage 1 : Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Stage 2 : Production ─────────────────────────────────────────────────────
FROM node:20-alpine AS production

WORKDIR /app

COPY --from=builder /app/dist ./dist

EXPOSE 3000

ENV NODE_ENV=production

CMD ["npx", "serve", "-s", "dist", "-l", "3000"]