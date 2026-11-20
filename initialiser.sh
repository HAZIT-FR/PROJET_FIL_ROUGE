#!/bin/sh
set -eu
cd "$(dirname "$0")"
test ! -e .env || { echo '.env existe déjà, aucun changement.'; exit 0; }
umask 077
python3 - <<'PY'
from pathlib import Path
import secrets

contenu = Path('.env.example').read_text()
for ligne in contenu.splitlines():
    cle, valeur = ligne.split('=', 1)
    if cle.endswith('_PASSWORD'):
        contenu = contenu.replace(ligne + '\n', cle + '=' + secrets.token_hex(24) + '\n')
with open('.env', 'x') as fichier:
    fichier.write(contenu)
PY
echo '.env créé. Adapter les adresses avant de démarrer.'
