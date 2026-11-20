# Doc : https://www.jenkins.io/doc/book/installing/docker/
FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update && apt-get install -y git curl unzip ca-certificates mariadb-client

# Doc : https://maven.apache.org/install.html
RUN curl -L https://archive.apache.org/dist/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.tar.gz -o /tmp/maven.tar.gz \
    && tar -xzf /tmp/maven.tar.gz -C /opt \
    && mv /opt/apache-maven-3.9.16 /opt/maven \
    && rm /tmp/maven.tar.gz

# Distribution Any, avec le Java déjà installé.
# Doc : https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner
RUN curl -L https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-8.4.0.16527.zip -o /tmp/scanner.zip \
    && unzip /tmp/scanner.zip -d /opt \
    && mv /opt/sonar-scanner-8.4.0.16527 /opt/sonar-scanner \
    && rm /tmp/scanner.zip

ENV JAVA_HOME=/opt/java/openjdk
ENV MAVEN_HOME=/opt/maven
ENV SONAR_SCANNER_HOME=/opt/sonar-scanner
ENV PATH="/opt/maven/bin:/opt/sonar-scanner/bin:${PATH}"

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt \
    && mkdir /backups && chown jenkins:jenkins /backups

USER jenkins
