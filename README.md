**TiCoin Mining Simulator**

Herzlich willkommen zum TiCoin Mining Simulator!
Hier erfährst du, wie das Programm funktioniert, wie die wichtigen Dateien zusammenarbeiten und wie du alles einfach mit Docker und Docker Compose auf deinem Server laufen lassen kannst.
Ich empfehle, es nur intern im Heimnetz laufen zu lassen, da Flask nicht gerade das Sicherste ist und hauptsächlich nur für Testzwecke ist.

Mit dem Webhook, den ich unten im Text erkläre, kann der Verlauf, wann was durch die Simulation gefunden wurde, sicher von außen angezeigt werden, ohne den Dienst ins Internet nach außen verfügbar zu machen. Für den Webhook wird allerdings Discord gebraucht.



**1. Was macht dieses Programm?**

Simuliert das Mining von TiCoins.
Läuft als Web-App mit Flask.
Du kannst Mining starten und stoppen.
TiCoins werden gespeichert, damit dein Fortschritt nicht verloren geht.
Schickt Nachrichten an einen Discord-Textkanal, wenn TiCoins gefunden werden oder Mining startet/stoppt (nur sofern ein gültiger Webhook im Code zu Discord festgelegt ist, bitte Anleitung unten beachten).
Zeigt Mining-Fortschritt und Logs auf der Webseite an.


**2. Wichtige Dateien und ihre Aufgaben**

Dockerfile

Baut ein kleines Linux-Image mit Python 3.12.
Installiert benötigte Python-Bibliotheken aus requirements.txt.
Kopiert deinen Code in den Container.
Startet dein Programm (app.py).
Öffnet Port 5000 für die Web-App.


requirements.txt
Listet alle Python-Bibliotheken, die das Programm braucht:

    Flask
    Requests
    pytz

docker-compose.yml

Vereinfacht das Starten des Containers.
Definiert den Dienst „ticoins“.
Baut das Image basierend auf dem Dockerfile.
Verbindet den Port 5000 des Containers mit dem Server.
Bindet deinen Projektordner in den Container ein (So kannst du den geänderten Code einfach auf den Server laden und dann den Container neustarten, dann werden die Änderungen direkt übernommen.).
Setzt die Zeitzone auf Europa/Berlin.

app.py
In dieser Datei steht der gesamte programmierte Code inklusive der Weboberfläche usw. 

**3. Wie du das Programm auf deinem Server startest**

-Installiere Docker und Docker Compose auf deinem Server.

-Kopiere alle Dateien (app.py, Dockerfile, requirements.txt, docker-compose.yml) in einen Ordner auf deinem Server.
  
Terminal öffnen und in den Ordner, wo die Dateien im vorherigen Schritt reinkopiert worden sind, wechseln:
cd /pfad/zu/deinem/projekt

Docker-Image bauen und den Simulator Inklusive weboberfläche starten:
docker-compose up --build

Web-App öffnen:
http://deine-server-ip:5000
Dort siehst du dein TiCoin Mining Simulator.

**4. Nützliche Docker-Kommandos**

Container stoppen:
docker-compose down

Logs anzeigen:
docker-compose logs -f

Container neu starten:
docker-compose restart

**5. Wie funktioniert der Discord-Webhook aus der app.py?**

Dein TiCoin Mining Simulator schickt Nachrichten an einen Discord-Textkanal, damit du immer informiert bist, was gerade passiert – ganz automatisch!
Was ist ein Discord Webhook?

Ein Webhook ist eine spezielle Internet-Adresse (URL), die Discord dir gibt.
Über diese Adresse kannst mit deinem Programm Nachrichten an einen Discord-Textkanal senden.
Du musst dafür keinen Bot programmieren, sondern nur diese Webhook-URL nutzen, die discord dir gibt.

**6. Wie nutzt bei deinem Programm ein Discord Webhook?**

Im Code gibt es die Variable DISCORD_WEBHOOK_URL. Dort trägst du die Webhook-Adresse ein, die du bei deinem Discord-Server bekommst.
    
Wenn du nicht möchtest, dass diese Nachrichten an einem Discord-Server-Chatraum gesendet werden, dann passe den Webhook einfach nicht an, also lasse die Variable so, wie sie standardmäßig im Code ist.
Nachteil wäre: Du kannst den Stand und Verlauf der Mining-Simulation nur über die Weboberfläche sehen.

Falls du den Webhook, den du von Discord bekommen kannst, aber in der Variable DISCORD_WEBHOOK_URL festlegst, dann ist es so, dass
-Wenn ein TiCoin gefunden wurde, eine Nachricht mit der Info „TiCoin gefunden!“ an Discord geschickt wird.
-Wenn das Mining gestartet oder gestoppt wird, sendet dein Programm auch automatisch eine Nachricht an den Discord-Textkanal.

Die Nachrichten enthalten auch die genaue Zeit (Nach Berliner Zeitzone) und sind schön eingebettet.
So kannst du immer live verfolgen, was dein TiCoin Mining Simulator gerade macht – auch wenn du nicht auf der Web Oberfläche bist!

**7. Warum ist das praktisch?**

Du wirst sofort informiert, wenn TiCoins gefunden werden.
Du siehst, wann der Miner gestartet oder gestoppt wurde.
Du kannst diese Info-Nachrichten in Discord mit Freunden teilen oder sie nur für dich anzeigen lassen indem du den textkanal wo der webhook das reinsendet auf privat stellst.
Es läuft alles automatisch im Hintergrund, ohne dass du ständig die Webseite anschauen musst.

**8. Wie bekommst du deine Discord Webhook-URL?**

Öffne deinen Discord-Server.
Gehe in den Kanal, in dem du Nachrichten empfangen möchtest.
Klicke auf den „Einstellungs Button“ dann auf „Integration“ und „Webhook erstellen“.
Erstelle einen neuen Webhook und kopiere die URL.
Füge die URL in app.py bei DISCORD_WEBHOOK_URL ein.

**9. Sicherheitstipp**

Teile die Webhook-URL nicht öffentlich!
Jeder mit dieser URL kann Nachrichten in deinen Discord-Textkanal senden.

**10. Zusammenfassung Webhook**

Webhook = Adresse zum automatischen Senden von Nachrichten.
TiCoin Miner nutzt sie, um dich per Discord zu informieren.
Du bekommst Updates über gefundene TiCoins und Mining-Status.
Einfach in Discord erstellen und im Code eintragen.

**11. Warum Docker?**

Kein Setup von Python auf dem Server nötig.
Isolierter Container, der deine App sicher und sauber laufen lässt.
Einfaches Deployment und Updates durch Container-Neustart.
Einfaches Port-Management.

**12. Hinweise und Tipps**

Passe die DISCORD_WEBHOOK_URL in app.py an deine eigene an.
Ändere Mining-Parameter im Code für mehr Spaß.
Bei Problemen mit dem Speicherort kannst du das Volume im docker-compose.yml anpassen.
Nutze die Logs auf der Web Oberfläche, um den Mining-Fortschritt zu verfolgen.
Alternativ kannst du dein Mining Fortschritt über ein Discord Webhook einsehen (sofern dies eingerichtet ist)

**habe diese Anleitung/Beschrreibung mit KI generiert und zimlich viel angepasst hoffe das erleichtert euch bei der einrichtung des Dienstes bin leider nicht so gut in Anleitungen usw. schreiben aber habe mein bestes gegeben!**

**Viel Spaß euch! MFG Timo**
