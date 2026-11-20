# Projet fil rouge — Jenkins

GitLab → Jenkins → SonarQube → Artifactory → Tomcat. Sauvegarde MySQL en fin de pipeline.

Chaque techno a un dossier `compose/` (service et fichiers associés) et un dossier `kube/` (manifeste Kubernetes).
Chaque Compose se lance séparément, depuis la racine du dépôt, avec `-f` et le même fichier `.env`.
Les anciens scripts Python sont conservés ; ils ne servent pas au déploiement conteneurisé.

## Docker Compose

Prévoir Docker, Compose v2, 16 Go de RAM minimum et environ 40 Go libres.
Utiliser Compose et Kubernetes successivement sur une machine de 16 Go.
SonarQube demande `vm.max_map_count=1048576` sur l’hôte Linux du moteur Docker.

```sh
sh initialiser.sh
# Adapter HOST_IP, GITLAB_URL et JENKINS_URL dans .env.
docker network create fil-rouge
docker compose --env-file .env -f postgres/compose/compose.yaml up -d --wait
docker compose --env-file .env -f mysql/compose/compose.yaml up -d --wait
docker compose --env-file .env -f gitlab/compose/compose.yaml up -d
docker compose --env-file .env -f jenkins/compose/compose.yaml up -d --build
docker compose --env-file .env -f tomcat/compose/compose.yaml up -d --build
docker compose --env-file .env -f artifactory/compose/compose.yaml up -d
docker compose --env-file .env -f sonarqube/compose/compose.yaml up -d
```

`.env` est privé et ignoré par Git.
Sur CT-PYTHON-01, remplacer `127.0.0.1` et `localhost` par `192.168.1.42` pour accéder aux interfaces depuis le LAN.

```sh
docker compose --env-file .env -f jenkins/compose/compose.yaml exec jenkins java -version
docker compose --env-file .env -f jenkins/compose/compose.yaml exec jenkins javac -version
docker compose --env-file .env -f jenkins/compose/compose.yaml exec jenkins mvn -version
docker compose --env-file .env -f jenkins/compose/compose.yaml exec jenkins git --version
docker compose --env-file .env -f jenkins/compose/compose.yaml exec jenkins sonar-scanner --version
```

| Service | Port hôte | Compte initial |
| --- | --- | --- |
| GitLab | 8088 | root, mot de passe `.env` |
| Jenkins | 8080 | admin, mot de passe `.env` |
| Tomcat | 8089 | deployer, accès API uniquement |
| Artifactory | 8082 | admin / password, à changer au premier accès |
| SonarQube | 9000 | admin / admin, à changer au premier accès |

MySQL et PostgreSQL restent sur le réseau interne. Premier démarrage GitLab : plusieurs minutes.
Les mots de passe de base ne s’appliquent qu’à l’initialisation des volumes vides.

## Pipeline

1. Importer l’application dans le GitLab local. Créer un jeton limité à la lecture du dépôt.
2. Dans SonarQube, créer le projet `fil-rouge` et un jeton d’analyse.
3. Dans Artifactory, terminer l’initialisation et créer un dépôt local **Generic** nommé `war-local`. Créer un compte autorisé à y déposer les WAR.
4. Dans Jenkins → Manage Jenkins → Credentials → System → Global, ajouter :

| ID | Type | Valeur |
| --- | --- | --- |
| gitlab | Username with password | utilisateur GitLab et jeton en mot de passe |
| sonarqube | Secret text | jeton d’analyse |
| artifactory | Username with password | compte de dépôt et son mot de passe/jeton |

`tomcat` et `mysql` sont déjà déclarés dans `jenkins/compose/jenkins.yaml`.
Créer un job **Pipeline**, coller `jenkins/Jenkinsfile` dans **Pipeline script**, puis enregistrer.
Premier lancement : il installe les paramètres et s’arrête faute d’adresse applicative.
Relancer avec **Build with Parameters**, en renseignant par exemple `http://gitlab/groupe/application.git` et la branche.

Le pipeline attend un projet Maven simple : `pom.xml` à la racine, sources dans `src/main`, un seul WAR dans `target/`.
Il compile sans exécuter les tests. L’analyse SonarQube attend le résultat du Quality Gate avant de poursuivre.
Le WAR est déposé dans `war-local/fil-rouge/<numéro du build>/application.war`, puis déployé sous `/application`.
MySQL : hôte `mysql`, port `3306`, base et utilisateur `application`. Adapter la configuration JDBC à l’application lorsqu’elle sera fournie.
Tomcat 9 utilise `javax.servlet` ; une application Jakarta récente demandera une adaptation.
MySQL 8.4 LTS remplace la version 5.7 suggérée dans le sujet ; compatibilité à confirmer avec l’application.

## Sauvegarde

Les dumps compressés sont dans `/backups` du conteneur Jenkins, sur un volume distinct.
Copier le dump choisi, puis le restaurer dans la base séparée `restauration` :

```sh
mkdir -p backups
chmod 700 backups
docker compose --env-file .env -f jenkins/compose/compose.yaml cp jenkins:/backups/. backups/
sh mysql/compose/restaurer.sh backups/nom-du-fichier.sql.gz
```

La base `application` reste en place. Supprimer la base `restauration` après vérification.
Les dumps restent privés.

## Kubernetes

Un cluster et `kubectl` doivent être disponibles, avec une StorageClass par défaut.
Arrêter les conteneurs Compose avant de lancer Kubernetes. Construire les mêmes images, puis les charger dans Minikube :

```sh
docker compose --env-file .env -f jenkins/compose/compose.yaml build
docker compose --env-file .env -f tomcat/compose/compose.yaml build
minikube image load fil-rouge/jenkins:1.0
minikube image load fil-rouge/tomcat:1.0
kubectl kustomize . > /dev/null
kubectl apply -k .
kubectl -n fil-rouge get pods,pvc,svc
```

Pour un autre cluster, publier les deux images dans un registre accessible et remplacer leur nom dans les manifests.
Le namespace `fil-rouge` possède ses propres volumes : les données Compose ne sont pas transférées automatiquement.
Reprendre l’initialisation GitLab/SonarQube/Artifactory et le job Jenkins ci-dessus.

Ouvrir les interfaces avec un port-forward par terminal (ports de `.env`, depuis la machine qui exécute les commandes) :

```sh
kubectl -n fil-rouge port-forward service/gitlab 8088:80
kubectl -n fil-rouge port-forward service/jenkins 8080:8080
kubectl -n fil-rouge port-forward service/tomcat 8089:8080
kubectl -n fil-rouge port-forward service/artifactory 8082:8082
kubectl -n fil-rouge port-forward service/sonarqube 9000:9000
```

Adapter les URL `.env` au point d’accès utilisé avant `kubectl apply -k .`.
Les échanges du pipeline utilisent les Services internes ; le Jenkinsfile reste identique.
Vérifier aussi les quatre outils avec `kubectl -n fil-rouge exec deploy/jenkins -- <commande>`.
Récupérer les sauvegardes avec `kubectl -n fil-rouge cp <pod-jenkins>:/backups backups`.
Ne pas supprimer les volumes pour simplement arrêter la démonstration.

## Fin du TP

Pour arrêter un composant :

```sh
docker compose --env-file .env -f tomcat/compose/compose.yaml down
```

En fin de TP, ces commandes suppriment les composants et leurs données :

```sh
for techno in gitlab jenkins tomcat mysql artifactory sonarqube postgres; do
  docker compose --env-file .env -f "$techno/compose/compose.yaml" down -v
done
docker network rm fil-rouge
kubectl delete namespace fil-rouge
```

Références : [sujet](https://drive.google.com/file/d/1WfSx4R9hgGVbpFAQOqGsYJLbTMPzFZ4f/view), [Maven](https://maven.apache.org/download.cgi), [SonarScanner](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner), [Artifactory](https://docs.jfrog.com/installation/docs/docker).
