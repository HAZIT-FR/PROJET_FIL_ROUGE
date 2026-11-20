#!/bin/sh
# Restauration dans une base séparée, depuis la racine du dépôt.
set -eu
umask 077
test "$#" -eq 1 || { echo "Usage : sh mysql/restaurer.sh sauvegarde.sql.gz" >&2; exit 1; }
gzip -t "$1"
docker compose exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  mysql -uroot -e "CREATE DATABASE IF NOT EXISTS restauration;"
'
temporaire=$(mktemp)
trap 'rm -f "$temporaire"' EXIT
gzip -dc "$1" > "$temporaire"
docker compose exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  exec mysql -uroot restauration
' < "$temporaire"
docker compose exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  mysql -uroot -e "SHOW TABLES FROM restauration;"
'
