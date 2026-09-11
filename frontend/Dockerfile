FROM node:20-alpine AS base
RUN npm install -g pnpm@9.15.4
RUN adduser -D -u 1001 appuser
WORKDIR /app

FROM base AS deps
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install

FROM base AS development
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Save a backup of node_modules so the entrypoint can restore
# them when the named volume is empty (bind mount overrides image data).
RUN cp -a node_modules /opt/node_modules_cache
RUN chmod +x docker-entrypoint.sh
# Development runs as root to match host bind-mount permissions.
# Production stage uses a non-root user.
ENTRYPOINT ["sh", "-c", "if [ -d /opt/node_modules_cache/.pnpm ] && [ ! -f node_modules/next/dist/bin/next ]; then echo 'node_modules missing or broken - restoring from image cache...'; rm -rf node_modules/*; cp -a /opt/node_modules_cache/. node_modules/; echo 'Done.'; fi; exec \"$@\"", "--"]
CMD ["pnpm", "dev"]

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM base AS production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/content ./content
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
RUN chown -R appuser:appuser /app
USER appuser
CMD ["pnpm", "start"]
