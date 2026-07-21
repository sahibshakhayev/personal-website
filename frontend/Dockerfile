# --- Stage 1: Base ---
# We use 'slim' instead of 'alpine' to prevent the musl/gnu LightningCSS crashes we fixed earlier!
FROM node:20-slim AS base
WORKDIR /app
COPY package.json package-lock.json ./

# --- Stage 2: Development ---
# Target this using `build: { target: development }` in docker-compose.yml
FROM base AS development
ENV NODE_ENV=development
# We run npm install here, but remember your docker-compose volume might mask this!
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# --- Stage 3: Builder ---
FROM base AS builder
# npm ci is faster and stricter than npm install for production builds
RUN npm ci
COPY . .
RUN npm run build

# --- Stage 4: Production ---
# We use Node, not Nginx, so Next.js can run its SSR server
FROM base AS production
ENV NODE_ENV=production
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

# Copy only the compiled standalone files and public assets
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]