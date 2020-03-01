import socket
import signal
import threading

from user_input_handling import user_input_mapper

class Client(object):

    STOP = False

    # Die aktuelle Richtung. Wird zum Server
    # geschickt, sobald das Attribut (neu)gesetzt wird.
    direction = "right"

    def __init__(self):
        self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.input_thread.start()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect(("localhost", 10028))

        print("DEBUG Verbundung zum Server hergestellt!")

        #self.client_socket.close()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if name == "direction":
            self.__send_user_input_to_server()

    def __send_user_input_to_server(self):
        self.client_socket.send(str.encode(self.direction))

def main():
    #signal.signal(signal.SIGINT, stop_program)

    Client()

if __name__ == "__main__":
    main()