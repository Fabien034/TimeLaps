# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016


from __future__ import unicode_literals
from __future__ import print_function

import socket, sys, threading, time, os

# adresse IP et port utilises par le serveur
HOST = ""
PORT = 50100

serveurLance = True
dictClient = {}  # dictionnaire des connexions clients


class ThreadClient(threading.Thread):
    '''derivation de classe pour gerer la connexion avec un client'''
    
    def __init__(self,conn):

        threading.Thread.__init__(self)
        self.connexion = conn
        
        # Memoriser la connexion dans le dictionnaire        
        self.nom = self.getName() # identifiant du thread "<Thread-N>"
        dictClient[self.nom] = self.connexion
        print("Connexion du client", self.connexion.getpeername(),self.nom ,self.connexion)        
        message = "Vous etes connecte au serveur.\n"
        self.connexion.send(message.decode(encoding='UTF-8'))        
        
    def run(self):

        # Réception des messages       
        while True:            
            try:
                # attente réponse client
                MessageRecu = self.connexion.recv(4096)
                if MessageRecu:
                    MessageRecu = MessageRecu.decode(encoding='UTF-8')
                    print("message du client",self.nom,">",MessageRecu)
                    TraitementMessage(self.nom, MessageRecu)
            except:
                # fin du thread
                print ("Client (%s, %s) is offline" % infos_connexion)
                self.connexion.close()
                dictClient.remove(self.connexion)
                continue 
            
            # on traite les messages recu
            

        print("\nFin du thread",self.nom)
        self.connexion.close()


def TraitementMessage (Client, Message):
    """ Traitement du message recu """  
    if Message.split(" ")[0] == "makedirs":
        if not os.path.exists(Message.split(" ")[1]):
            os.makedirs(Message.split(" ")[1], mode=0o777)


def main():    
    # Initialisation du serveur
    # Mise en place du socket avec les protocoles IPv4 et TCP
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try:
        mySocket.bind((HOST, PORT))
    except socket.error:
        print("La liaison du socket a l'adresse choisie a echoue.")
        sys.exit()

    print("Le serveur écoute à présent sur le port {}".format(PORT))
    
    while serveurLance:
        mySocket.listen(5)
        try:
            connexion, adresse = mySocket.accept()
        except:
            sys.exit()
        # Créer un nouvel objet thread pour gérer la connexion
        th = ThreadClient(connexion)
        # The entire Python program exits when no alive non-daemon threads are left
        th.setDaemon(1)
        th.start()


    # fermeture des sockets
    for client in dictClient:
        dictClient[client].close()
        print("Deconnexion du socket", client)

    input("\nAppuyer sur Entree pour quitter l'application...\n")
    # fermeture des threads (daemon) et de l'application


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programme interrompu par l'utilisateur")
        if dictClient:
            for client in dictClient:
                dictClient[client].close()
                print("Deconnexion du socket", client)
        sys.exit()
