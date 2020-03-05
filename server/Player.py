import socket
import threading

class Player(object):

    DEFAULT_DIRECTION = "right"

    def __init__(self, player_id, name, socket : socket.socket, address):
        self.socket = socket
        self.name = name
        self.id = player_id
        self.address = address

        self.requested_direction = Player.DEFAULT_DIRECTION

    def recieve_data(self):
        def recieve_loop():
            while True:
                recv = self.socket.recv(512);
                if len(recv) == 0:
                    break
                
                # In Zukunft validieren?
                self.requested_direction = recv.decode()
                #debug("user_input: " + recv.decode())

            self.socket.close()    
        
        threading.Thread(target=recieve_loop).start()