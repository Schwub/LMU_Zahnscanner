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
* pip installieren: apt get install python-pip
* pip install wxPython
* pip install opencv-python
* pip install pyopengl
* pip install serial
* pip install scipy
* pip install matplotlib==2.0.2

## Nur Für Virtualbox

* export DISPLAY=:0
