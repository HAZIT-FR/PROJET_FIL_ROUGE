import subprocess

APT_INSTALL_LIST = ["curl", "jenkins"]
APT_INSTALL_LIST_SUBPROCESS = " ".join(APT_INSTALL_LIST)

CMD_WGET_PGP = "sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key"
CMD_REPO_JENKINS = 'echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null'
CMD_APT_UPDATE = "sudo apt-get update"
CMD_APT_INSTALL = "sudo apt install -y " + APT_INSTALL_LIST_SUBPROCESS

CMD_UFW_DISABLE = "sudo ufw disable"
CMD_JENKINS_ENABLE = "sudo systemctl enable jenkins"
CMD_JENKINS_START = "sudo systemctl start jenkins"

try:
    print(f"Récupération de la clé PGP avec {CMD_WGET_PGP}")
    subprocess.run(CMD_WGET_PGP, shell=True, check=True)

    print(f"Ajout du dépôt Jenkins avec {CMD_REPO_JENKINS}")
    subprocess.run(CMD_REPO_JENKINS, shell=True, check=True)

    print(f"Mise à jour des packages avec {CMD_APT_UPDATE}")
    subprocess.run(CMD_APT_UPDATE, shell=True, check=True)

    print(f"Installation des packages {APT_INSTALL_LIST} avec {CMD_APT_INSTALL}")
    subprocess.run(CMD_APT_INSTALL, shell=True, check=True)

    print(f"Désactivation du pare-feu avec {CMD_UFW_DISABLE}")
    subprocess.run(CMD_UFW_DISABLE, shell=True, check=True)

    print(f"Activation du service Jenkins avec {CMD_JENKINS_ENABLE}")
    subprocess.run(CMD_JENKINS_ENABLE, shell=True, check=True)

    print(f"Démarrage du service Jenkins avec {CMD_JENKINS_START}")
    subprocess.run(CMD_JENKINS_START, shell=True, check=True)

    print("Installation terminée avec succès.")

except subprocess.CalledProcessError as erreur:
    print(f"ERREUR : la commande a échoué : {erreur.cmd}")
    print(f"Code de retour : {erreur.returncode}")
    print("Installation interrompue.")