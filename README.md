# TimeLaps
Projet TimeLaps sur Rpi

Prise de vue toutes les x secondes sur une plage horaires defini par le fichier config et transfert des photo vers un serveur

Executer le script fichierConfig.py pour les reglages
Executer le script TimeLaps.py pour lancer la prise de vue
Executer le script TransfertFichier.py pour lancer le transfer vers le serveur

Controle de l'APN via subprocess Gphoto: Attention RPi doit être configurer en français (raspi-config)

L'APN doit etre en mode semi-automatique et la MAP faite manuellement

Fichier à suprimer pour l'utilisation de gphoto et redemarrer le rpi
	sudo rm /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
	sudo rm /usr/share/gvfs/mounts/gphoto2.mount
	sudo rm /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor
	sudo rm /usr/lib/gvfs/gvfs-gphoto2-volume-monitor