import socket
import sys
import json, yaml
import time, threading

from .Engine import Engine
from .Player import Player

CONFIG = {}

class Server(object):

    # Deprecated
    client_connected = None

    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_list = []

    def connect_clients(self):

        # Spieleranzahl abfragen 
        print("Wie viele Spieler spielen mit? (1 - 4 / 0 -> Abbruch)")
        correct_input = False
        player_count = 0
        while not correct_input:
            try:
                player_count = int(input(">> "))
                if player_count < 0 or player_count > 4:
                    raise ValueError
                else:
                    correct_input = True
            except: 
                print("Eingabe ungültig (1 - 4 / 0 -> Abbruch)")

        # ggf. aussteigen
        if player_count == 0:
            sys.exit()

        # Bind und Listen
        try:
            self.serverSocket.bind(("localhost", CONFIG["port"]))
            self.serverSocket.listen()
        except socket.error as msg:
            print("ERROR " + str(msg))
            sys.exit()

        player_con_threads = []
        for i in range(player_count):
            debug("Warte auf eine Verbindungsanfrage")
            self.serverSocket.settimeout(CONFIG["connectionTimeout"])
            debug(f"Wartezeit: {CONFIG['connectionTimeout']} Sekunden")

            # TODO: Schön machen
            try:
                client_connected, client_address = self.serverSocket.accept()
                debug("Akzeptiert eine Verbindungsanfrage von %s:%s" % (client_address[0], client_address[1]))
                # Verbindung in Thread abwickeln, damit Anfragen schneller angenommen werden können
                t = threading.Thread(target=self.__connect_player, args=(client_connected, client_address))
                t.start()
                player_con_threads.append(t)
            except socket.error as err:
                print("WARNING Fehler bei der Verbindung mit Spieler " + str(len(self.player_list) + 1) + "!")

        if len(self.player_list) == 0:
            info("Kein Spieler verbunden!")
            self.serverSocket.close()
            sys.exit()
        else:
            for t in player_con_threads: t.join()
            info(str(len(self.player_list)) + " Spieler verbunden!")
            time.sleep(5) 

    def __connect_player(self, client_connected, client_address):
        player_id = len(self.player_list) + 1
        new_player = Player(player_id, f"Spieler {player_id}", client_connected, client_address)
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

def debug(msg):
    if CONFIG["debug"]:
        print(f"DEBUG {msg}")

def info(msg):
    print(f"INFO {msg}")

def load_config(filepath):
    global CONFIG
    CONFIG = yaml.load(open(filepath, "r"), Loader=yaml.SafeLoader)
