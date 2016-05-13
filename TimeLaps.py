# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import pickle

from wrappers import Tmux

# Vérifie si le fichier configServer Existe sinon lance FichierConfig.py
CONFIGSERVER = os.path.join(os.path.expanduser("~"), "TimeLaps", "configServer")
if not os.path.isfile(CONFIGSERVER):
    subprocess.call(["python", os.path.join(os.path.expanduser("~"), "TimeLaps", "FichierConfig.py")])

#Lecture et recuperation des variables dans le fichier configServer
with open("configServer", "rb") as fichierConfig:
    configRead = pickle.Unpickler(fichierConfig)
    HOST = configRead.load()
    PORT = int(configRead.load())
    USER = configRead.load()
    PORTSSH = int(configRead.load())

# Tmux
# nouvelle session
windows = Tmux(subprocess)
# nouvelle fenetre
windows.newWindows("TimeLaps")
# lancement du script CapturePhoto.py
windows.sendKeys("python {0}".format(os.path.join(os.path.expanduser("~"), "TimeLaps", "CapturePhoto.py")))
# on la divise verticalement
windows.splitWindows("v")
# on redimensionne depuis le bas
windows.resizePane("D", "5")
# on lance l'ouverture de tmux a distance sur le serveur
windows.sendKeys("ssh -p {0} -t {1}@{2} tmux a || ssh -p {0} -t {1}@{2} tmux".format(PORTSSH, USER, HOST))
# on selectionne la fenetre 0
windows.selectPane("0")
# on la divise horizontalement
windows.splitWindows("h")
# on redimensionne depuis le droite
windows.resizePane("R", "10")
# lancement du script TransfertFichier.py
windows.sendKeys("python {0}".format(os.path.join(os.path.expanduser("~"), "TimeLaps", "TransfertFichier.py")))
# on la divise verticalement
windows.splitWindows("v")
# lancement du script ListDossierAttente.py
windows.sendKeys("python {0}".format(os.path.join(os.path.expanduser("~"), "TimeLaps", "ListDossierAttente.py")))
# on attache la session
windows.attachSession()


