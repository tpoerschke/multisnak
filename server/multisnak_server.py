import socket
import sys
import json, yaml
import time

from Engine import Engine

CONFIG = {}

class Server(object):

    client_connected = None

    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_clients(self):
         # Bind und Listen
        try:
            self.serverSocket.bind(("localhost", CONFIG["port"]))
            self.serverSocket.listen()
        except socket.error as msg:
            print("ERROR " + str(msg))
            sys.exit()

        info("Warte auf eine Verbindungsanfrage")
        self.serverSocket.settimeout(CONFIG["connectionTimeout"])
        debug(f"Wartezeit: {CONFIG['connectionTimeout']} Sekunden")

        try:
            client_connected, client_address = self.serverSocket.accept()
            debug("Akzeptiert eine Verbindungsanfrage von %s:%s" % (client_address[0], client_address[1]))
        except socket.error as err:
            info("Kein Spieler verbunden!")
            self.serverSocket.close()
            sys.exit()

        try:
            client_connected.send(str.encode("{\"state\": \"connect\", \"msg\": \"Das Spiel startet in Kürze...\"}"))
            debug("Benachrichtigung \"Start in Kürze\" zum Client gesendet")
        except OSError as err:
            print("WARNING", err)

        self.client_connected = client_connected
        time.sleep(5) # Das Verbinden anderer Spieler simulieren
        
    def do_game_loop(self):
        try:
            # Start-Mechanismen des Client anstoßen
            self.client_connected.send(str.encode("{\"state\": \"prepare\"}"))
            debug("Daten zum Client gesendet.")
        except OSError as err:
            print("WARNING", err)

        ENGINE = Engine(self.client_connected, CONFIG["engine"])
        ENGINE.start()

        while True:
            recv = self.client_connected.recv(512);
            if len(recv) == 0:
                break
            
            # In Zukunft validieren?
            ENGINE.direction = recv.decode()
            debug("user_input: " +recv.decode())

        self.client_connected.close()    

def main():
    load_config("server.config.yaml")
    server = Server()
    server.connect_clients()
    server.do_game_loop()

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