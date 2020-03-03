import socket
import signal
import threading
import sys
import json

from user_input_handling import user_input_mapper
from Board import Board

class Client(object):

    STOP = False

    # Die aktuelle Richtung. Wird zum Server
    # geschickt, sobald das Attribut (neu)gesetzt wird.
    direction = "right"

    def __init__(self):
        self.board = Board()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.input_thread.start() # TODO: Thread erst starten, wenn das Spiel startet

        self.reciever_thread = threading.Thread(target=self.__recieve_data)
        self.reciever_thread.start()

        try:
            self.client_socket.connect(("localhost", 10028))
            debug("Verbindung zum Server hergestellt!")
        except ConnectionRefusedError as err:
            print("ERROR Verbindung zum Server konnte nicht hergestellt werden.")
            self.client_socket.close()
            sys.exit(1)

        #self.client_socket.close()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name == "direction":
            self.__send_user_input_to_server()

    def __send_user_input_to_server(self):
        try:
            self.client_socket.send(str.encode(self.direction))
        except (BrokenPipeError, OSError):
            print("ERROR Daten konnten nicht zum Server gesendet werden.")

    def __recieve_data(self):
        while True: # TODO: Vernünftige Abbruchbedingung
            try:
                recv = self.client_socket.recv(2048)
                if len(recv) == 0:
                    break
                print("DEBUG", recv.decode())
                self.__display(json.loads(recv.decode()))
            except OSError as err:
                print("ERROR", err)

    def __display(self, game_data):
        self.board.clear()
        for symbol in game_data["draw"]:
            self.board.draw_symbol(symbol["coords"], symbol["symbol"])
        sys.stdout.flush()

def debug(msg):
    print(f"DEBUG {msg}")

def main():
    #signal.signal(signal.SIGINT, stop_program)

    Client()



if __name__ == "__main__":
    main()