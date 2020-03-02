import socket
import signal
import threading
import sys

from user_input_handling import user_input_mapper

class Client(object):

    STOP = False

    # Die aktuelle Richtung. Wird zum Server
    # geschickt, sobald das Attribut (neu)gesetzt wird.
    direction = "right"

    def __init__(self):
        self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.input_thread.start() # TODO: Thread erst starten, wenn das Spiel startet

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

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

def debug(msg):
    print(f"DEBUG {msg}")

def main():
    #signal.signal(signal.SIGINT, stop_program)

    Client()

if __name__ == "__main__":
    main()