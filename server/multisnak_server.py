import socket
import sys
import json, yaml
import time

from Engine import Engine

CONFIG = {}

def main():
    load_config("server.config.yaml")

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind und Listen
    try:
        serverSocket.bind(("localhost", CONFIG["port"]))
        serverSocket.listen()
    except socket.error as msg:
        print("ERROR " + str(msg))
        sys.exit()

    info("Warte auf eine Verbindungsanfrage")
    serverSocket.settimeout(CONFIG["connectionTimeout"])
    debug(f"Wartezeit: {CONFIG['connectionTimeout']} Sekunden")

    try:
        client_connected, client_address = serverSocket.accept()
        debug("Akzeptiert eine Verbindungsanfrage von %s:%s" % (client_address[0], client_address[1]))
    except socket.error as err:
        info("Kein Spieler verbunden!")
        serverSocket.close()
        sys.exit()

    try:
        client_connected.send(str.encode("{\"state\": \"connect\", \"msg\": \"Das Spiel startet in Kürze...\"}"))
        debug("Daten zum Client gesendet.")
    except OSError as err:
        print("WARNING", err)

    time.sleep(5) # Das Verbinden anderer Spieler simulieren

    try:
        # Start-Mechanismen des Client anstoßen
        client_connected.send(str.encode("{\"state\": \"prepare\"}"))
        debug("Daten zum Client gesendet.")
    except OSError as err:
        print("WARNING", err)

    ENGINE = Engine(client_connected, CONFIG["engine"])
    ENGINE.start()

    while True:
        recv = client_connected.recv(512);
        if len(recv) == 0:
            break
        
        # In Zukunft validieren?
        ENGINE.direction = recv.decode()
        debug("user_input: " +recv.decode())

    client_connected.close()    

def debug(msg):
    if CONFIG["debug"]:
        print(f"DEBUG {msg}")

def info(msg):
    print(f"INFO {msg}")

def load_config(filepath):
    global CONFIG
    CONFIG = yaml.load(open(filepath, "r"), Loader=yaml.SafeLoader)

if __name__ == "__main__":
    main()