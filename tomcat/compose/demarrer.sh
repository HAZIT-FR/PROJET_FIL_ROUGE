#!/bin/sh
set -eu
: "${TOMCAT_PASSWORD:?Mot de passe Tomcat absent}"
case "$TOMCAT_PASSWORD" in *[!a-zA-Z0-9]*) echo 'Utiliser un mot de passe alphanumérique.' >&2; exit 1 ;; esac
umask 077
cat > "$CATALINA_HOME/conf/tomcat-users.xml" <<EOF
<tomcat-users>
  <role rolename="manager-script" />
  <role rolename="manager-gui" />
  <user username="admin" password="$TOMCAT_PASSWORD" roles="manager-script,manager-gui" />
</tomcat-users>
EOF
exec catalina.sh run
