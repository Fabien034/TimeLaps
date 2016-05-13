TimeLaps sur Raspberry
======================

**En cours de dévellopement**

Objectif du projet
------------------

Prise de vue sur toutes les x secondes sur une plage horaires et période definie
Transfert des Photos de l'APN vers le Rpi
Transfert des photographies vers un serveur distant
Monitoring depuis une console en SSH

Installation
------------
* **Dépendances**

		sudo apt-get install openssh-server tmux gphoto2 git
		sudo Pip install exifread

	si vous ne disposé pas de Pip, vous le trouverez ici: `pip <http://pypi.python.org/pypi/pip>`
	
	Controle de l'APN via subprocess Gphoto: Attention RPi doit être configurer en français (raspi-config)
	
	**Fichier à suprimer pour l'utilisation de gphoto**

		sudo rm /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
		sudo rm /usr/share/gvfs/mounts/gphoto2.mount
		sudo rm /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor
		sudo rm /usr/lib/gvfs/gvfs-gphoto2-volume-monitor
		
	Redémarrer le Rpi
	
Fonctionnement
--------------

Sur le serveur:
	- Executer le script '~/TimeLaps/server.sh'

Sur le Rpi:
	- Configurer le Timelaps en executant le fichier '~/TimeLaps/FichierConfig.py'
	- Executer le script '~/TimeLaps/Timelaps.py' pour lancer le Timelaps

**L'authetification pat clef RSA**
Voir: '<http://jeyg.info/ssh-authentification-par-cles-rsa-ou-dsa/>'

Sources
-------

Gphoto2: '<http://gphoto.sourceforge.net/>'
Tmux: '<https://tmux.github.io/>'
David singleton: '<http://blog.davidsingleton.org/raspberry-pi-timelapse-controller/>'
