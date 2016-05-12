# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016


from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import time

from wrappers import ListDirectory

def main():
    
    WAITPATH = os.path.join(os.path.expanduser("~"),"Pictures","Attente") 

    while True:
        try:
            os.system("clear") 
            filePath = ListDirectory(WAITPATH)
            if len(filePath) > 0:
                strFichier = "fichiers"
            else:
                strFichier = "fichier"
            print("{0} {1} dans le dossier Attente".format(len(filePath),strFichier))
            print(".")
            for f in filePath:
                print("|-- {0}".format(os.path.basename(f))) 
            time.sleep(2)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
