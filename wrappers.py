# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: Fabien Rosso

# Version 0.1.1 - 19 Avril 2016
# Version 0.1.2 - 29 Avril 2016



from __future__ import unicode_literals
from __future__ import print_function


import re
import os
import exifread
import shutil
import pickle
import subprocess


class Wrapper(object):

    def __init__(self, subprocess):
        self._subprocess = subprocess

    def call(self, cmd):
        p = self._subprocess.Popen(cmd, shell=True,
                                   stdout=self._subprocess.PIPE,
                                   stderr=self._subprocess.PIPE)
        out, err = p.communicate()
        return p.returncode, out.rstrip(), err.rstrip()


class NetworkInfo(Wrapper):

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)

    def network_status(self):
        iwcode, iwconfig, err = self.call("iwconfig")
        wlcode, wlan, err = self.call("ifconfig wlan0")
        etcode, eth, err = self.call("ifconfig eth0")
        ssid = None
        wip = None
        eip = None
        if iwcode == 0 and 'ESSID' in iwconfig:
            ssid = re.findall('ESSID:"([^"]*)', iwconfig)[0]
        if wlcode == 0 and 'inet addr' in wlan:
            wip = re.findall('inet addr:([^ ]*)', wlan)[0]
        if etcode == 0 and 'inet addr' in eth:
            eip = re.findall('inet addr:([^ ]*)', eth)[0]
        ret = ''
        if ssid:
            ret = ssid
        if wip:
            ret = ret + '\n' + wip
        elif eip:
            ret = ret + eip
        if not ssid and not wip and not eip:
            ret = 'No Network'
        return ret


class GPhoto(Wrapper):
    """ A class which wraps calls to the external gphoto2 process. """

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)
        self._CMD = 'gphoto2'
        self._shutter_choices = None
        self._iso_choices = None

    def capture_image_and_download(self):
        code, out, err = self.call(self._CMD + " --capture-image-and-download")
        if code != 0:
            raise Exception(err)
        filename = None
        for line in out.split(b'\n'):
            if line.startswith(b'Enregistrement du fichier en '):
                filename = line.split(b'Enregistrement du fichier en ')[1]
        return filename


class Photo():
    """Class definissant une photo caracterisee par:
    - Chemin (self.pathFile)
    - son nom (self.namefile)
    - son extension (self.extFile)
    - son dossier parent (self.parenPathFile)

    Fonction:
    - recupere la date de prise de vue (self.tag_date_time())
    - Deplace/renome le fichier dans un nouveau repertoire
      (self.move(newPath)) """

    def __init__(self, path):
        self.pathFile = path
        self.nameFile = os.path.split(self.pathFile)[1]
        self.extFile = os.path.splitext(self.pathFile)[1]
        self.parenPathFile = os.path.split(self.pathFile)[0]

    def tag_date_time(self):
        """ Recupere la date de prise de vue dans les exif avec la lib exifread
        N'est plus utilise dans la V0.1.1.1"""
        # Lecture des Exif
        with open(self.pathFile, "rb") as f:
            tags = exifread.process_file(f)
        # Recupere la date de prise de vue
        try:
            tagsDateTime = tags['Image DateTime'].values
        except Exception, e:
            print("Erreur: ") + str(e)
        return tagsDateTime

    def move(self, newPath):
        """Deplace/Renome la photo dans un repertoire newPath"""
        shutil.move(self.pathFile, newPath)
        file = Photo(newPath)
        return file


class Scp(Wrapper):
    """ A class which wraps calls to the external scp process. """

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)
        self._CMD = 'scp'

        with open("configServer", "rb") as fichierConfig:
            configRead = pickle.Unpickler(fichierConfig)
            self.host = configRead.load()
            self.port = configRead.load()
            self.user = configRead.load()
            self.portSsh = configRead.load()

    def send(self, file, fileDestination):
        code, out, err = self.call(self._CMD +
                                   " -P " + str(self.portSsh) +
                                   " -p " + file + " " +
                                   self.user + "@" + self.host + ":" +
                                   fileDestination)
        if code != 0:
            raise Exception(err)
        return out

class Tmux(Wrapper):
    """ A class which wraps calls to the external tmux process. """

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)
        self._CMD = 'tmux'
        self.session = os.environ["USER"]
        code, out, err = self.call(self._CMD + " -2 new-session -d -s " + self.session)
        if code != 0:
            raise Exception(err)

    def newWindows(self, nameWindows):
        code, out, err = self.call(self._CMD + " new-window -t " + self.session + ":1 -n '" + nameWindows + "'")
        if code != 0:
            raise Exception(err)
    
    def sendKeys(self, keys):
        code, out, err = self.call(self._CMD + " send-keys '" +  keys + "' C-m")
        if code != 0:
            raise Exception(err)

    def splitWindows(self, split):
        """ split = v pour vertical
            split = h pour horizontal """
        code, out, err = self.call(self._CMD + " split-window -" + split)
        if code != 0:
            raise Exception(err)

    def resizePane(self, prefixe, nb):
        """ prefixe = D (Resizes the current pane down)
            prefixe = U (Resizes the current pane upward)
            prefixe = L (Resizes the current pane left)
            prefixe = R (Resizes the current pane right) """
        code, out, err = self.call(self._CMD + " resize-pane -" + prefixe + " " + nb)
        if code != 0:
            raise Exception(err)

    def selectPane(self, nb):
        code, out, err = self.call(self._CMD + " select-pane -t " + nb)
        if code != 0:
            raise Exception(err)

    def attachSession(self):
        code, out, err = self.call(self._CMD + " -2 attach-session -t " + self.session)
        if code != 0:
            raise Exception(err)


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
