#!/bin/sh
# Doc : https://dev.mysql.com/doc/refman/8.4/en/reloading-sql-format-dumps.html
# Restauration dans une base séparée, depuis la racine du dépôt.
set -eu
umask 077
test "$#" -eq 1 || { echo "Usage : sh mysql/compose/restaurer.sh sauvegarde.sql.gz" >&2; exit 1; }
gzip -t "$1"
docker compose --env-file .env -f mysql/compose/compose.yaml exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  mysql -uroot -e "CREATE DATABASE IF NOT EXISTS restauration;"
'
temporaire=$(mktemp)
trap 'rm -f "$temporaire"' EXIT
gzip -dc "$1" > "$temporaire"
docker compose --env-file .env -f mysql/compose/compose.yaml exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  exec mysql -uroot restauration
' < "$temporaire"
docker compose --env-file .env -f mysql/compose/compose.yaml exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  mysql -uroot -e "SHOW TABLES FROM restauration;"
'
