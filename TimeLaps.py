# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import subprocess
import pickle
from wrappers import Tmux
from fonctions import *

# Vérifie si le fichier configServer Existe sinon lance FichierConfig.py
CONFIGSERVER = os.path.join(os.path.expanduser("~"), "TimeLaps", "configServer")
if not os.path.isfile(CONFIGSERVER):
    subprocess.call(["python", os.path.join(os.path.expanduser("~"), "TimeLaps", "FichierConfig.py")])

# Création d'un dictionnaire pour l'état des scripts:
# 0 - Script non lancé
# 1 - Script lancé
# 2 - demande d'arrêt
# Deuxieme chiffre de la liste est le PID du process
dictEtatScript = {"CapturePhoto":[0,0], "TransfertFichier":[0,0], "ListDossierAttente":[0,0]}

with open("etatScript", "wb") as file:
    configWrite = pickle.Pickler(file)
    configWrite.dump(dictEtatScript)

etatScript = {}
with open("etatScript", "rb") as file:
        configRead = pickle.Unpickler(file)
        etatScript = configRead.load()

for cle,valeur in etatScript.items():
    print(cle,valeur)


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
script="CapturePhoto.py"
strScript = os.path.join(os.path.expanduser("~"), "TimeLaps", script)
windows.sendKeys("python {0}".format(strScript))
time.sleep(0.5)

# on vérifie que le script est lancé
processPythonPid = pythonExist(strScript)
if type(processPythonPid) == int:
    processPython = psutil.Process(processPythonPid)
    print("le script {} a été démarré : {}".format(strScript,processPythonPid))
    dictEtatScript["CapturePhoto"] = [1,processPythonPid]
else:
    print("le script {} n'a pas été démarré".format(strScript))
    sys.exit()


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
script="TransfertFichier.py"
strScript = os.path.join(os.path.expanduser("~"), "TimeLaps", script)
windows.sendKeys("python {0}".format(strScript))
time.sleep(0.5)

# on vérifie que le script est lancé
processPythonPid = pythonExist(strScript)
if type(processPythonPid) == int:
    processPython = psutil.Process(processPythonPid)
    print("le script {} a été démarré : {}".format(strScript,processPythonPid))
    dictEtatScript["TransfertFichier"] = [1,processPythonPid]
else:
    print("le script {} n'a pas été démarré".format(strScript))
    sys.exit()

# on la divise verticalement
windows.splitWindows("v")

# lancement du script ListDossierAttente.py
script="ListDossierAttente.py"
strScript = os.path.join(os.path.expanduser("~"), "TimeLaps", script)
windows.sendKeys("python {0}".format(strScript))
time.sleep(0.5)

# on vérifie que le script est lancé
processPythonPid = pythonExist(strScript)
if type(processPythonPid) == int:
    processPython = psutil.Process(processPythonPid)
    print("le script {} a été démarré : {}".format(strScript,processPythonPid))
    dictEtatScript["ListDossierAttente"] = [1,processPythonPid]
else:
    print("le script {} n'a pas été démarré".format(strScript))
    sys.exit()

# on attache la session
windows.attachSession()


# Mise à jour du dictionnaire 'dictEtatScript' dans le fichier 'etatScript'
with open("etatScript", "wb") as file:
    configWrite = pickle.Pickler(file)
    configWrite.dump(dictEtatScript)

etatScript = {}
with open("etatScript", "rb") as file:
        configRead = pickle.Unpickler(file)
        etatScript = configRead.load()

for cle,valeur in etatScript.items():
    print(cle,valeur)


