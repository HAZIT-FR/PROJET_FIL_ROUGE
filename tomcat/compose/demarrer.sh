#!/bin/sh
set -eu
: "${TOMCAT_PASSWORD:?Mot de passe Tomcat absent}"
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
