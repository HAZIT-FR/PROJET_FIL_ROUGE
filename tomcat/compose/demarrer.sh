#!/bin/sh
# Rôles du Manager : https://tomcat.apache.org/tomcat-9.0-doc/manager-howto.html#Configuring_Manager_Application_Access
set -e
test -n "$TOMCAT_PASSWORD" || exit 1
mot_de_passe=$(printf '%s' "$TOMCAT_PASSWORD" | sed 's/\&/\&amp;/g; s/</\&lt;/g; s/"/\&quot;/g')
umask 077
cat > "$CATALINA_HOME/conf/tomcat-users.xml" <<EOF
<tomcat-users>
  <role rolename="manager-script" />
  <role rolename="manager-gui" />
  <user username="admin" password="$mot_de_passe" roles="manager-script,manager-gui" />
</tomcat-users>
EOF
exec catalina.sh run
