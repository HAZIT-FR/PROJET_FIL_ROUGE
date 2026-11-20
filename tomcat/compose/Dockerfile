FROM tomcat:9.0.124-jdk21-temurin-noble
RUN cp -r /usr/local/tomcat/webapps.dist/manager /usr/local/tomcat/webapps/manager
COPY context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml
COPY demarrer.sh /usr/local/bin/demarrer.sh
RUN chmod 755 /usr/local/bin/demarrer.sh
ENTRYPOINT ["/usr/local/bin/demarrer.sh"]
