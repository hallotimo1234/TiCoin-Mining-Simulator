from flask import Flask, jsonify
import threading
import time
import random
import datetime
import pytz
import json
import os
import requests
import logging

app = Flask(__name__)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

DISCORD_WEBHOOK_URL = "---Trage_Hier_Dein_Discord_WebHook_Ein---"


ticoins = 0.0
MINING_CHANCE = 0.025
mining_speed = 5
mining = False
progress = 0
log = []

lock = threading.Lock()
last_saved_ticoins = None

def send_discord_message(message: str):
    berlin = pytz.timezone('Europe/Berlin')
    now = datetime.datetime.now(berlin)
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S")

    embed = {
        "title": "TiCoin Mining Simulator",
        "description": "─────────────────────",
        "color": 16766720,
        "fields": [
            {"name": "TiCoin gefunden!", "value": message, "inline": False},
            {"name": "Zeitpunkt", "value": timestamp, "inline": False}
        ]
    }

    data = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[DISCORD] Fehler beim Senden der Nachricht: {response.status_code} {response.text}")
    except Exception as e:
        print(f"[DISCORD] Ausnahme beim Senden der Nachricht: {e}")

def send_discord_start_message():
    global ticoins

    berlin = pytz.timezone('Europe/Berlin')
    now = datetime.datetime.now(berlin)
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S")

    embed = {
        "title": "TiCoin Mining Simulator",
        "description": "Mining Gestartet\n─────────────────────",
        "color": 52224,
        "fields": [
            {"name": "Datum & Uhrzeit", "value": timestamp, "inline": False},
            {"name": "Aktueller TiCoin Stand", "value": f"{ticoins:.8f} TiC", "inline": False},
        ]
    }

    data = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[DISCORD] Fehler beim Senden der Start-Nachricht: {response.status_code} {response.text}")
        else:
            print("[DISCORD] Start-Nachricht erfolgreich gesendet!")
    except Exception as e:
        print(f"[DISCORD] Ausnahme beim Senden der Start-Nachricht: {e}")

def send_discord_stop_message():
    global ticoins

    berlin = pytz.timezone('Europe/Berlin')
    now = datetime.datetime.now(berlin)
    timestamp = now.strftime("%d.%m.%Y %H:%M:%S")

    embed = {
        "title": "TiCoin Mining Simulator",
        "description": "Mining Gestoppt\n─────────────────────",
        "color": 16711680,
        "fields": [
            {"name": "Datum & Uhrzeit", "value": timestamp, "inline": False},
            {"name": "Aktueller TiCoin Stand", "value": f"{ticoins:.8f} TiC", "inline": False},
        ]
    }

    data = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[DISCORD] Fehler beim Senden der Stopp-Nachricht: {response.status_code} {response.text}")
        else:
            print("[DISCORD] Stopp-Nachricht erfolgreich gesendet!")
    except Exception as e:
        print(f"[DISCORD] Ausnahme beim Senden der Stopp-Nachricht: {e}")

def mine():
    global ticoins, mining, progress, log
    while mining:
        steps = 100
        for i in range(steps):
            if not mining:
                print("[BUTTON] Mining gestoppt!")
                progress = 0
                return
            with lock:
                progress = i + 1
            time.sleep(mining_speed / steps)

        with lock:
            chance = MINING_CHANCE / 100
            if random.random() < chance:
                reward = 0.00000001
                ticoins += reward
                berlin = pytz.timezone('Europe/Berlin')
                now = datetime.datetime.now(berlin)
                timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
                log.append(f"{timestamp} - TiCoin gefunden! +{reward:.8f} TiC")
                print(f"[MINER] TiCoin gefunden! Neuer Stand: {ticoins:.8f} TiC")
                send_discord_message(f"🪙 +{reward:.8f} TiC")
            progress = 0

def load_data():
    global ticoins, last_saved_ticoins
    if os.path.exists("save_data.json"):
        with open("save_data.json", "r") as f:
            data = json.load(f)
            ticoins_str = data.get("ticoins", "0.00000000")
            ticoins = float(ticoins_str)
            print(f"[LADE_DATEN] TiCoins geladen: {ticoins:.8f}")
            last_saved_ticoins = ticoins
    else:
        print("[LADE_DATEN] Keine gespeicherte Datei gefunden.")
        last_saved_ticoins = 0.0

def save_periodically():
    global last_saved_ticoins
    while True:
        time.sleep(5)
        with lock:
            if ticoins != last_saved_ticoins:
                with open("save_data.json", "w") as f:
                    json.dump({"ticoins": f"{ticoins:.8f}"}, f)
                last_saved_ticoins = ticoins
                now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
                timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
                log.append(f"{timestamp} - TiCoins gespeichert: {ticoins:.8f}")
                print(f"[SPEICHER_DATEN] TiCoins gespeichert: {ticoins:.8f} TiC")

def get_web_logs():
    return [entry for entry in log if "TiCoins gespeichert" not in entry]

@app.route('/')
def index():
    return f'''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <title>TiCoin Mining Portal</title>
    <style>
        body {{ background: #121212; color: white; font-family: Arial, sans-serif; text-align: center; }}
        #progress {{ width: 80%; height: 20px; }}
        button {{ font-size: 18px; padding: 10px 20px; margin: 10px; cursor: pointer; }}
        #log {{ background: #222; padding: 10px; height: 150px; overflow-y: scroll; margin: 20px auto; width: 80%; text-align: left; }}
        .log-entry {{ margin-bottom: 4px; color: #90ee90; }}
    </style>
</head>
<body>
    <h1>TiCoin Mining Simulator</h1>
    <div>TiCoins: <span id="ticoins">{ticoins:.8f}</span></div>
    <progress id="progress" value="0" max="100"></progress><br/>
    <button id="toggle">Starte Mining</button>
    <div id="status"></div>

    <h3>Mining Verlauf:</h3>
    <div id="log"></div>

    <script>
        const toggleBtn = document.getElementById('toggle');
        const ticoinsSpan = document.getElementById('ticoins');
        const progressBar = document.getElementById('progress');
        const statusDiv = document.getElementById('status');
        const logDiv = document.getElementById('log');
        const MAX_LOG_ENTRIES = 5;
        let mining = false;

        let shownLogs = new Set();

        function updateStatus() {{
            fetch('/status').then(res => res.json()).then(data => {{
                ticoinsSpan.textContent = data.ticoins;
                progressBar.value = data.progress;

                data.log.forEach(line => {{
                    if (!shownLogs.has(line) && line.includes("TiCoin gefunden")) {{
                        const div = document.createElement("div");
                        div.textContent = line;
                        div.classList.add("log-entry");
                        logDiv.appendChild(div);
                        shownLogs.add(line);
                    }}
                }});

                logDiv.scrollTop = logDiv.scrollHeight;

                if (data.mining) {{
                    statusDiv.textContent = "Mining läuft...";
                    toggleBtn.textContent = "Stoppe Mining";
                    mining = true;
                    setTimeout(updateStatus, 500);
                }} else {{
                    statusDiv.textContent = "Mining gestoppt.";
                    toggleBtn.textContent = "Starte Mining";
                    progressBar.value = 0;
                    mining = false;
                }}
            }});
        }}

        toggleBtn.onclick = () => {{
            if (mining) {{
                fetch('/stop', {{method: 'POST'}}).then(() => {{
                    mining = false;
                    toggleBtn.textContent = "Starte Mining";
                    statusDiv.textContent = "Mining gestoppt.";
                    progressBar.value = 0;
                }});
            }} else {{
                fetch('/start', {{method: 'POST'}}).then(() => {{
                    mining = true;
                    toggleBtn.textContent = "Stoppe Mining";
                    statusDiv.textContent = "Mining läuft...";
                    updateStatus();
                }});
            }}
        }};

        window.onload = updateStatus;
    </script>
</body>
</html>
'''

@app.route('/start', methods=['POST'])
def start():
    global mining
    if not mining:
        mining = True
        print("[BUTTON] Mining gestartet!")
        send_discord_start_message()
        threading.Thread(target=mine, daemon=True).start()

    return jsonify(success=True)

@app.route('/stop', methods=['POST'])
def stop():
    global mining
    mining = False
    send_discord_stop_message()
    return jsonify(success=True)

@app.route('/status')
def status():
    with lock:
        return jsonify(
            ticoins=f"{ticoins:.8f}",
            progress=progress,
            log=get_web_logs()[-20:],
            mining=mining
        )

if __name__ == "__main__":
    load_data()
    print("[MAIN] TiCoin Miner ist bereit zum Mining")
    threading.Thread(target=save_periodically, daemon=True).start()
    host = '0.0.0.0'
    port = 5000
    print(f"[MAIN] Server läuft auf http://{host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)