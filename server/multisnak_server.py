import socket
import sys
import json

def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind und Listen
    try:
        serverSocket.bind(("localhost", 10028))
        serverSocket.listen()
    except socket.error as msg:
        print("ERROR " + str(msg))
        sys.exit()

    print("DEBUG Warte auf eine Verbindungsanfrage")

    client_connected, client_address = serverSocket.accept()

    print("DEBUG Akzeptiert eine Verbindungsanfrage von %s:%s" % (client_address[0], client_address[1]))

    # data_dict = {
    #     "state": "prepare",
    #     "snake": [(2,3), (3,3)]
    # }

    # client_connected.send(str.encode(json.dumps(data_dict)))

    while True:
        print("DEBUG user_input:", client_connected.recv(512).decode())

    client_connected.close()

if __name__ == "__main__":
    main()