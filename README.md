# VirtualBox Setup

* VirtualBox Extensionpack für USB Support installieren:
	* Passende Version herunterladen
	* VboxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack
* User zur Virtualbox Gruppe hinzufügen um USB zugriff zu erlauben:
	* usermod -aG vboxusers USER
* Virtualbox -> Ändern -> USB -> IDS Kamera und Arduino hinzufügen

# IDS Treiber installieren

Die IDS Software Suite muss unter folgendem Link heruntergeladen werden:
[IDS Camera Suite](https://de.ids-imaging.com/download-details/AB00687.html?os=linux&version=&bus=64&floatcalc=)

Hierfür wird ein Benutzerkonto benötigt.

* Das heruntergeladene Verzeichnis entpacken
* In das Verzeichnis wechseln
* Installation: sudo sh ./uyey*.run 
* IDS Deamon starten: sudo systemctl start ueyeusbdrc

# Scanner Software Installation

* apt install libgtk-3-dev
* apt install freeglut3-dev
* git clone https://github.com/Schwub/LMU_Zahnscanner
* cd LMU_Zahnscanner/horus
* pip3 install wxpython
* pip3 install opencv-python
* pip3 install pyopengl
* pip3 install matplotlib
* pip3 install numpy
* pip3 install scipy
* python3 horus

## Nur Für Virtualbox

* export DISPLAY=:0
