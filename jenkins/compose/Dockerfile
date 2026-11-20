# Doc Jenkins et plugins : https://www.jenkins.io/doc/book/installing/docker/
FROM jenkins/jenkins:lts-jdk21@sha256:74401de6a6f92e1afe1b02d1c8e3d0c33f263bfb5275dd8813f9150355f2367b

USER root
ARG MAVEN_VERSION=3.9.16
ARG SCANNER_VERSION=8.4.0.16527
ARG SCANNER_SHA256=0bc442965fe778693e714234b75ad9ee8667d6fe53e90556f86eb215fa4073a5

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl unzip ca-certificates mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Doc Maven : https://maven.apache.org/install.html
RUN set -eu; \
    url="https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz"; \
    curl -fsSL "$url" -o /tmp/maven.tar.gz; \
    curl -fsSL "$url.sha512" -o /tmp/maven.sha512; \
    echo "$(cat /tmp/maven.sha512)  /tmp/maven.tar.gz" | sha512sum -c -; \
    tar -xzf /tmp/maven.tar.gz -C /opt; \
    mv "/opt/apache-maven-${MAVEN_VERSION}" /opt/maven; \
    rm /tmp/maven.*

# La distribution Any utilise le JDK déjà présent.
# Doc : https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner
RUN set -eu; \
    curl -fsSL "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SCANNER_VERSION}.zip" -o /tmp/scanner.zip; \
    echo "${SCANNER_SHA256}  /tmp/scanner.zip" | sha256sum -c -; \
    unzip -q /tmp/scanner.zip -d /opt; \
    mv "/opt/sonar-scanner-${SCANNER_VERSION}" /opt/sonar-scanner; \
    rm /tmp/scanner.zip

ENV JAVA_HOME=/opt/java/openjdk \
    MAVEN_HOME=/opt/maven \
    SONAR_SCANNER_HOME=/opt/sonar-scanner
ENV PATH="${MAVEN_HOME}/bin:${SONAR_SCANNER_HOME}/bin:${PATH}"
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt \
    && mkdir /backups && chown jenkins:jenkins /backups

USER jenkins
