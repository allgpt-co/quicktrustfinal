#!/bin/sh
set -e

# When ./frontend is bind-mounted to /app, node_modules from the host
# may have broken symlinks (pnpm workspace paths). Detect this and
# restore from the image cache.
if [ -d "/opt/node_modules_cache/.pnpm" ]; then
  if [ ! -f "node_modules/next/dist/bin/next" ]; then
    echo "node_modules missing or broken — restoring from image cache..."
    rm -rf node_modules/*
    cp -a /opt/node_modules_cache/. node_modules/
    echo "Done."
  fi
fi

exec "$@"
