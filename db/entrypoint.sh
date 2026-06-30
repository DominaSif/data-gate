#!/bin/bash
set -e

INIT_DIR="${INIT_DIR:-/docker-entrypoint-initdb.d/init}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$INIT_DIR/roles.sql"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$INIT_DIR/schema.sql"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$INIT_DIR/rls.sql"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$INIT_DIR/grants.sql"
