#!/bin/sh
# Doc : https://dev.mysql.com/doc/refman/8.4/en/reloading-sql-format-dumps.html
# Depuis la racine du dépôt : sh mysql/compose/restaurer.sh sauvegarde.sql.gz
set -e
gzip -t "$1"
docker compose --env-file .env -f mysql/compose/compose.yaml exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  mysql -uroot -e "CREATE DATABASE IF NOT EXISTS restauration;"
'
gzip -dc "$1" | docker compose --env-file .env -f mysql/compose/compose.yaml exec -T mysql sh -c '
  export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
  exec mysql -uroot restauration
'
