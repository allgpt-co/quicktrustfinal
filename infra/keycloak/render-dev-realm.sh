#!/bin/sh
set -eu
: "${KEYCLOAK_CLIENT_SECRET:?KEYCLOAK_CLIENT_SECRET is required}"
mkdir -p /opt/keycloak/data/import
sed "s|__KEYCLOAK_CLIENT_SECRET__|${KEYCLOAK_CLIENT_SECRET}|g"   /opt/keycloak/data/realm-export.dev.json > /opt/keycloak/data/import/realm-export.json
exec /opt/keycloak/bin/kc.sh start-dev --import-realm
