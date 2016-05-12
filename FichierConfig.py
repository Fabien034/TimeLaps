# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016



import pickle
from datetime import date, time, datetime

def convertInt (listeStr):
    listeInt = []
    for x in listeStr:
     listeInt.append(int(x))    
    return listeInt    

dateStart = convertInt(raw_input("Entrez la date de debut (jj.mm.aaaa): ").split('.'))
dateStop = convertInt(raw_input("Entrez la date de fin (jj.mm.aaaa): ").split('.'))
timleSlotMini = convertInt(raw_input("Entrez une heure de debut (hh:mm): ").split(':'))
timleSlotMaxi = convertInt(raw_input("Entrez une heure de fin (hh:mm): ").split(':'))
interShotDelaySec = float(raw_input("entrez l'intervalle entre les photos (minute): "))*60
host = raw_input("Entrez l'ip du serveur (77.147.64.38): ")
if host == "":
    host = "77.147.64.38"
user = raw_input("Entrez le nom de l'utilisateur sur le serveur (spm) : ")
if user == "":
    user = "spm"
port = 50100

dateStart = datetime(dateStart[2],dateStart[1],dateStart[0],timleSlotMini[0],timleSlotMini[1])
dateStop = datetime(dateStop[2],dateStop[1],dateStop[0],timleSlotMaxi[0],timleSlotMaxi[1])
timleSlotMini = time(timleSlotMini[0],timleSlotMini[1])
timleSlotMaxi = time(timleSlotMaxi[0],timleSlotMaxi[1])

with open("configServer", "wb") as fichierConfig:
    configWrite = pickle.Pickler(fichierConfig)
    configWrite.dump(host)
    configWrite.dump(port)
    configWrite.dump(user)

with open("config", "wb") as fichierConfig:
    configWrite = pickle.Pickler(fichierConfig)
    #enregistrement dans le fichier config
    configWrite.dump(dateStart)
    configWrite.dump(dateStop)
    configWrite.dump(timleSlotMini)
    configWrite.dump(timleSlotMaxi)
    configWrite.dump(interShotDelaySec) 
