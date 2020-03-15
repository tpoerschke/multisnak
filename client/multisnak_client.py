import socket
import signal
import threading
import sys, os
import json, yaml
from termcolor import colored

from .user_input_handling import user_input_mapper
from .terminal_tools import *
from .Board import Board
from .Scoreboard import Scoreboard

CONFIG = {}

class Client(object):

    STOP = True

    # Die aktuelle Richtung. Wird zum Server
    # geschickt, sobald das Attribut (neu)gesetzt wird.
    direction = "right"

    def __init__(self):
        self.board = Board()
        self.scoreboard = Scoreboard()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.reciever_thread = threading.Thread(target=self.__recieve_data)  

        # Um den Loop im reciever-Thread zu steuern
        self.recieve_data = True     

        try:
            self.client_socket.connect((CONFIG["server"]["ip"], CONFIG["server"]["port"]))
            info("Verbindung zum Server hergestellt!")
            self.reciever_thread.start()
        except ConnectionRefusedError as err:
            print("ERROR Verbindung zum Server konnte nicht hergestellt werden.")
            self.client_socket.close()
            sys.exit(1)

        #self.client_socket.close()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name == "direction":
            self.__send_user_input_to_server()

    def __start(self):
        # Wird ausgeführt, wenn der Server das "prepare" sendet
        type(self).STOP = False
        self.input_thread.start()
        os.system("clear")
        self.board.draw_frame()

    def stop(self, signum, frame):
        Client.STOP = True
        self.recieve_data = False
        #go_to_terminal_coords(0, Board.height)
        print("Spiel beendet. Pfeiltaste drücken...")

    def __send_user_input_to_server(self):
        try:
            self.client_socket.send(str.encode(self.direction))
        except (BrokenPipeError, OSError):
            print("ERROR Daten konnten nicht zum Server gesendet werden.")

    def __recieve_data(self):
        while self.recieve_data: 
            try:
                recv = self.client_socket.recv(16384)
                if len(recv) == 0:
                    break
                #debug(recv.decode())
                self.__handle_recieved_data(json.loads(recv.decode().split("%%")[0]))
            except (OSError, json.decoder.JSONDecodeError) as err:
                go_to_terminal_coords(0, Board.height)
                print("ERROR", err)
                #print(recv.decode())
                #break
        self.client_socket.close()

    def __handle_recieved_data(self, game_data):
        # Das Spiel kennt die folgenen Stati:
        # 1) connect -> Verbindungsaufbau
        # 2) prepare -> Spielfeld wird gezeichnet, Input-Thread wird gestartet usw.
        # 3) running
        # 4) stopped
        state = game_data["state"]

        if state == "connect":
            if "msg" in game_data:
                print("SERVER", game_data["msg"])
        elif state == "prepare":
            self.__start()
        elif state == "running":
            if "draw" in game_data:
                self.__draw(game_data["draw"])
        elif state == "stopped":
            go_to_terminal_coords(0, Board.height)
            print("GAME OVER")
            Client.STOP = True
            self.recieve_data = False

        if "scoreboard" in game_data:
            self.__display_scoreboard(game_data["scoreboard"])

    def __draw(self, draw):
        self.board.clear()
        
        SNAKE_SYMBOL = "O"
        BLOCKED_SYMBOL = "#"
        FOOD_SYMBOL = "+"

        # Schlangen zeichnen
        for snake_key in draw["snakes"]:
            coords = draw["snakes"][snake_key]
            for x, y in coords:
                go_to_terminal_coords(x, y)
                sys.stdout.write(colored(SNAKE_SYMBOL, CONFIG["colors"][f"player{snake_key}"]) if CONFIG["colors"]["showColors"] else SNAKE_SYMBOL)
        
        # Blockierte Felder zeichnen
        for x, y in draw["blocked"]:
            go_to_terminal_coords(x, y)
            sys.stdout.write(BLOCKED_SYMBOL)

        # Essen zeichnen
        x, y = draw["food"]
        go_to_terminal_coords(x, y)
        sys.stdout.write(FOOD_SYMBOL)

        go_to_terminal_coords(0, Board.height)
        sys.stdout.flush()

    def __display_scoreboard(self, scoreboard_data):
        self.scoreboard.draw(scoreboard_data)

def debug(msg):
    if CONFIG["debug"]:
        print(f"DEBUG {msg}")

def info(msg):
    print(f"INFO {msg}")

def load_config(filepath):
    global CONFIG
    CONFIG = yaml.load(open(filepath, "r"), Loader=yaml.SafeLoader)
