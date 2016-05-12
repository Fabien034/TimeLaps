# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016


from __future__ import unicode_literals
from __future__ import print_function

import os
import subprocess
import pickle


from datetime import datetime
import time
from time import sleep

from wrappers import *

import ptvsd
ptvsd.enable_attach(None)

os.system("clear")


def main():

    raw_input("Appuyer sur une touche pour demarrer le TimeLaps")
    print("---------")
    print("Timelapse")
    print("---------")
    print("Lecture des fichiers config et declaration des variables")
    # Lecture et recuperation des variables dans le fichier config
    with open("config", "rb") as fichierConfig:
        configRead = pickle.Unpickler(fichierConfig)
        DATE_START = configRead.load()
        DATE_STOP = configRead.load()
        TIME_SLOT_MINI = configRead.load()
        TIME_SLOT_MAXI = configRead.load()
        INTER_SHOT_DELAY_SEC = configRead.load()
    print("Date de debut: {0}".format(DATE_START))
    print("Date de Fin: {0}".format(DATE_STOP))
    print("Heure de debut: {0}".format(TIME_SLOT_MINI))
    print("Heure de Fin: {0}".format(TIME_SLOT_MAXI))

    # Création du dossier attente de tranfert
    WAITPATH = os.path.join(os.path.expanduser("~"), "Pictures", "Attente")
    if not os.path.exists(WAITPATH):
        os.makedirs(WAITPATH, mode=0o777)

    # inscription des class
    camera = GPhoto(subprocess)

    timeLapsStart = False

    while timeLapsStart == False:
        while datetime.now() > DATE_START and datetime.now() < DATE_STOP:
            timeLapsStart = True

            while datetime.now().time() > TIME_SLOT_MINI and datetime.now().time() < TIME_SLOT_MAXI:
                debutTimeTotal = time.time()
                try:
                    print("Capture et download de la photo")
                    timeScriptShot = time.time()
                    datetimeShot = datetime.now()
                    fileName = camera.capture_image_and_download()
                    print("Photo {0} prise".format(fileName))
                except Exception, e:
                    print("Error on capture.") + e
                    print("Retrying...")
                    continue

                # inscription de la class Photo
                file = Photo(os.path.join(os.path.expanduser("~"),
                                          "TimeLaps", fileName))

                print("Renome le fichier et le deplace dans dossier source")
                # Creation du nouveau nom
                newPathFile = os.path.join(WAITPATH,
                                           str('{0}{1}'
                                               .format(datetimeShot.strftime
                                                       ("%y%m%d-%H%M%S"),
                                                       file.extFile)))

                # Deplace/rennome la photo
                file = file.move(newPathFile)
                print("Fichier '{0}' transferer vers '{1}'"
                      .format(file.nameFile, file.parenPathFile))

                # Calcul du temps d'execution du script
                timeScriptShot = time.time()-timeScriptShot
                print("")
                print("--------------------------")
                print("Temps Total: {0}".format(timeScriptShot))
                print("--------------------------")
                print("")

                # Timer avant prochaine capture
                if timeScriptShot < INTER_SHOT_DELAY_SEC:
                    sleep(INTER_SHOT_DELAY_SEC-timeScriptShot)

    print("Le TimeLaps est termine")

if __name__ == "__main__":
    main()
