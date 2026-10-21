import os
import shutil
import subprocess
import sys

# install maven ouassila

#!/usr/bin/env python3

import subprocess

VERSION = "3.9.16"

MAVEN_SH = """\
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
export M2_HOME=/opt/maven
export MAVEN_HOME=/opt/maven
export PATH=${M2_HOME}/bin:${PATH}
"""


def run(cmd: str, **kwargs) -> None:
    print(f"$ {cmd}")
    subprocess.run(cmd, shell=True, check=True, executable="/bin/bash", **kwargs)

def install_Maven():
    print("\n=== Installation de Maven 3.9.16 ===")
    # sudo apt-get update / upgrade
    run("sudo apt-get update")
    run("sudo apt-get upgrade -y")

    # wget ... -P /tmp
    run(f"wget https://downloads.apache.org/maven/maven-3/{VERSION}/binaries/apache-maven-{VERSION}-bin.tar.gz -P /tmp")

    # sudo tar xf ... -C /opt
    run("sudo tar xf /tmp/apache-maven-*.tar.gz -C /opt")

    # sudo ln -s /opt/apache-maven-X /opt/maven
    run(f"sudo ln -sfn /opt/apache-maven-{VERSION} /opt/maven")

    # sudo nano /etc/profile.d/maven.sh  ->  écriture du fichier
    run("sudo tee /etc/profile.d/maven.sh > /dev/null", input=MAVEN_SH.encode())

    # sudo chmod u+x,g+x,o+x /etc/profile.d/maven.sh
    run("sudo chmod u+x,g+x,o+x /etc/profile.d/maven.sh")

    # source /etc/profile.d/maven.sh && mvn -version
    run("source /etc/profile.d/maven.sh && mvn -version")
    print("Maven a été bien installé ")


# Methode pour installer JAVA
def install_java():
    
    print("\n=== Installation de Java 21 ===")
    
    if not run_command(["sudo", "apt-get", "update"]):
        return
    if not run_command(["sudo", "apt-get", "upgrade"]):
        return
    
    if not run_command(["sudo", "apt-get", "install", "openjdk-21-jdk"]):
        print(
            "\nLe paquet openjdk-21-jdk n'est peut-être pas disponible "
            "dans les dépôts configurés sur cette version d'Ubuntu/Debian."
        )
        return
    run_command(["java", "-version"], check=False)
    run_command(["javac", "-version"], check=False)
    print("\nJava 21 a été installé (si les commandes de vérification ont réussi).")



    # sudo apt-get update && 
    # apt-get upgrade
# sudo apt-get install openjdk-21* # Java install

# # ajouter JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 dans  /etc/environment 
# # ajoute JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 dans .bashrc

# # Vérification de l'installation 
# java -version #récupérer la version
# source .bashrc
# echo $JAVA_HOME


def run_command(command, *, check=True):
    """Exécute une commande et affiche les erreurs si nécessaire."""
    print(f"\n$ {' '.join(command)}")
    try:
        subprocess.run(command, check=check)
    except subprocess.CalledProcessError as exc:
        print(f"\nErreur : la commande a échoué (code {exc.returncode}).")
        if check:
            return False
    return True


# Fonction pour afficher notre Menu de choix pour l'utilisateur
def show_menu():
    print("=" * 70)
    print(" " * 24 + "MENU D'INSTALLATION VMs")
    print("=" * 70)
    print("1 : Installation et configuration du JAVA (Version 21)")
    print("2 : Installation et configuration du maven")
    print("3 : Installation de Jenkins (Orchestrateur CI-CD)")
    print("4 : Installation et configuration d'Apache Tomcat")
    print("=" * 70)


def main():

    # if shutil.which("apt-get") is None:
    #     print("Ce script est prévu pour Ubuntu/Debian (commande apt-get introuvable).")
    #     sys.exit(1)

    actions = {
        "1": install_java,
        "2": install_Maven,
        # "3": install_jenkins,
        # "4": install_tomcat,
    }

    while True:
        show_menu()
        choice = input("Veuillez entrer le numéro de votre choix (1, 2, 3 ou 4) : ").strip()

        if choice in actions:
            actions[choice]()
            input("\nAppuyez sur Entrée pour revenir au menu...")
        elif choice.lower() in {"q", "quit", "exit"}:
            print("Au revoir.")
            break
        else:
            print("Choix invalide. Veuillez saisir 1, 2, 3 ou 4.")



if __name__ == "__main__":
    main()