import socket
import sys
import json, yaml
import time, threading

from Engine import Engine
from Player import Player

CONFIG = {}

class Server(object):

    # Deprecated
    client_connected = None

    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_list = []

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

        # TODO: Schön machen
        try:
            client_connected, client_address = self.serverSocket.accept()
            debug("Akzeptiert eine Verbindungsanfrage von %s:%s" % (client_address[0], client_address[1]))
            # Verbindung in Thread abwickeln, damit Anfragen schneller angenommen werden können
            threading.Thread(target=self.__connect_player, args=(client_connected, client_address)).start()
        except socket.error as err:
            info("Kein Spieler verbunden!")
            self.serverSocket.close()
            sys.exit()

        #self.client_connected = client_connected
        time.sleep(5) # Das Verbinden anderer Spieler simulieren

    def __connect_player(self, client_connected, client_address):
        new_player = Player(1, "Spieler 1", client_connected, client_address)
        info(f"Verbunden: {new_player.name} ({new_player.address[0]})")
        self.player_list.append(new_player)

        try:
            new_player.socket.send(str.encode("{\"state\": \"connect\", \"msg\": \"Das Spiel startet in Kürze...\"}"))
            debug("Benachrichtigung \"Start in Kürze\" zum Client gesendet")
        except OSError as err:
            print("WARNING", err)
        
    def do_game_loop(self):
        try:
            # Start-Mechanismen des Client anstoßen
            #self.client_connected.send()
            for player in self.player_list:
                player.socket.send(str.encode("{\"state\": \"prepare\"}"))
                debug(f"\"prepare\"-State an {player.name} gesendet.")
        except OSError as err:
            print("WARNING", err)

        ENGINE = Engine(self.player_list, CONFIG["engine"])
        ENGINE.start()

        for player in self.player_list:
            player.recieve_data()

        info("Spiel gestartet")

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