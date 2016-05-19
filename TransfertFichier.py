# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016


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
                # en attente de r?ception
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

    #Lecture et recuperation des variables dans le fichier configServer
    with open("configServer", "rb") as fichierConfig:
        configRead = pickle.Unpickler(fichierConfig)
        HOST = configRead.load()
        PORT = int(configRead.load())
        USER = configRead.load()

    HOMESERVER = os.path.join("/home",USER,"Images")
    # Création du dossier attente de tranfert
    WAITPATH = os.path.join(os.path.expanduser("~"),"Pictures","Attente")
    if not os.path.exists(WAITPATH):
        os.makedirs(WAITPATH, mode=0o777)

    # Etablissement de la connexion avec le serveur
    # protocoles IPv4 et TCP
    print("Connection au serveur")
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try:
        mySocket.connect((HOST, PORT))
    except socket.error:
        print("La connexion a echoue.")
        sys.exit()

    # Dialogue avec le serveur : threads pour gerer la reception des messages
    th_Reception = ThreadReception(mySocket)
    th_Reception.start()

    while True:
        listFile = ListDirectory(WAITPATH)

        if len(listFile) > 0:
            file = Photo(listFile[0])
            datePath = datetime.now().date().strftime("%Y/%y.%m.%d/")
            pathDestination = os.path.join(HOMESERVER,datePath)
            fileDestination = os.path.join(pathDestination,file.nameFile)

            message_emis = b"makedirs {0}".format(pathDestination)
            try:
                # emission
                mySocket.send(message_emis.decode(encoding='UTF-8'))
            except:
                break

            message_emis = b"EnvoiPhoto {0}".format(file.nameFile)
            try:
                # emission
                mySocket.send(message_emis.decode(encoding='UTF-8'))
            except:
                break
            print("Envoi de la photo {0}".format(file.nameFile))
            scp = Scp(subprocess)
            scp.send(file.pathFile, fileDestination)
            print("Envoi OK")

            message_emis = b"Fichier {0} transfere".format(file.nameFile)
            try:
                # emission
                mySocket.send(message_emis.decode(encoding='UTF-8'))
            except:
                break

            # Création du dossier Date dans le répertoire de travail
            sourcePath = os.path.join(os.path.expanduser("~"),"Pictures",datePath)
            if not os.path.exists(sourcePath):
                os.makedirs(sourcePath, mode=0o777)
                # Creation du nouveau nom
            newPathFile = os.path.join(sourcePath,file.nameFile)
            # Deplace/rennome la photo
            file = file.move(newPathFile)
            message_emis = "Fichier '{0}' transferer vers '{1}'".format(file.nameFile, file.parenPathFile)
            try:
                # emission
                mySocket.send(message_emis.decode(encoding='UTF-8'))
            except:
                break

    mySocket.close()
    print("envoi des photos termine")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("/nProgramme interrompu par l'utilisateur")
        sys.exit()

