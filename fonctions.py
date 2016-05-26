# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016


from __future__ import unicode_literals
from __future__ import print_function


import os
import psutil


def ListDirectory(path):
    ''' Fonction listdirectory(path)
    Fait une liste de tous les fichiers dans le repertoire 'path'
    et des sous repertoires
    '''
    fichier=[]
    for root, dirs, files in os.walk(path):
        for i in files:
            fichier.append(os.path.join(root, i))
    return fichier


def pythonExist(pythonProcess):
    process = False
    for proc in psutil.process_iter():
        try:
            pinfo  = proc.as_dict(attrs=['pid', 'name'])
        except:
            pass
        else:
            if pinfo['name'] == 'python' and proc.cmdline()[1] == pythonProcess:
                process = proc.pid
    
    if type(process) == int:
        return process

