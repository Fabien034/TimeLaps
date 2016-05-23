# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016

## Debug VisualStudio
# import ptvsd
# ptvsd.enable_attach(None)

from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import subprocess
import pickle
import socket
import threading

from datetime import datetime
from time import sleep

from wrappers import *

os.system("clear")


class ThreadReception(threading.Thread):
    """objet thread gerant la reception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # ref.  du socket de connexion

    def run(self):
        while True:
            try:
                # en attente de reception
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.encode(encoding='UTF-8')
                print(message_recu)
            except:
                # fin du thread
                break

        print("ThreadReception arrete. Connexion interrompue.")
        self.connexion.close()


def main():
    raw_input("Appuyer sur une touche pour demarrer l'envoi des photos")

    os.system("clear")

    #Lecture et recuperation des variables dans le fichier configServer
    with open("configServer", "rb") as fichierConfig:
        configRead = pickle.Unpickler(fichierConfig)
        HOST = configRead.load()
        PORT = int(configRead.load())
        USER = configRead.load()
        PORTSSH = int(configRead.load())

    HOMESERVER = os.path.join("/home",USER,"Images")
    # Création du dossier attente de tranfert
    WAITPATH = os.path.join(os.path.expanduser("~"),"Pictures","Attente")
    if not os.path.exists(WAITPATH):
        os.makedirs(WAITPATH, mode=0o777)

    # Etablissement de la connexion avec le serveur
    # protocoles IPv4 et TCP
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    print(" >> Connexion en cours avec " + HOST + "...")
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        print(" >> le serveur '" + host + "' est introuvable.")
        sys.exit()

    # Dialogue avec le serveur : threads pour gerer la reception des messages
    th_Reception = ThreadReception(mySocket)
    th_Reception.start()

    while True:
        listFile = ListDirectory(WAITPATH)

        if len(listFile) > 0:
            file = Photo(listFile[0]) # Création de la class photo
            octets = os.path.getsize(file.pathFile) / 1024 # Nombre d'octets de la photo
            print(" >> OK : '" + file.nameFile + "' [" + str(octets) + " Ko]")
            
            # on crée le chemin du fichier pour le serveur suivant la date de création
            datePath = time.strftime("%Y/%y.%m.%d/",file.createDate)
            pathDestination = os.path.join(HOMESERVER,datePath)
            fileDestination = os.path.join(pathDestination,file.nameFile)

            # on demande au serveur de créer le chemin si il n'eiste pas
            message_emis = b"makedirs {0}".format(pathDestination)
            try:
                # emission
                mySocket.send(message_emis.decode(encoding='UTF-8'))
                time.sleep(0.1)
            except:
                break

            # on indique au serveur que l'on va lui enoyer un fichier de x octets
            message_emis = b"EnvoiPhoto {0} {1}".format(file.nameFile,octets)
            try:
                # emission
                mySocket.send(message_emis.decode(encoding='UTF-8'))
                time.sleep(0.1)
            except:
                break
            print(" >> Envoi de la photo '{0}'".format(file.nameFile))

            # subprocess SCP pour l'envoie de la photo
            subprocess.call(["scp", "-P", bytes(PORTSSH), "-p", file.pathFile ,"{0}@{1}:{2}".format(USER, bytes(HOST), fileDestination)])

            time.sleep(0.01)
            print(" >> Envoi OK")
            
            # on crée le chemin du fichier pour le rangement sur le RPi suivant la date de création
            # si il n'existe pas on crée le dossier
            sourcePath = os.path.join(os.path.expanduser("~"),"Pictures",datePath)
            if not os.path.exists(sourcePath):
                os.makedirs(sourcePath, mode=0o777)
            # Creation du nouveau nom
            newPathFile = os.path.join(sourcePath,file.nameFile)
            # Deplace/rennome la photo
            file = file.move(newPathFile)
            print(" >> Fichier '{0}' déplacé vers '{1}'".format(file.nameFile, file.parenPathFile))
            print("")


    mySocket.close()
    print(" >> envoi des photos termine")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programme interrompu par l'utilisateur")
        sys.exit(0)

