import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect(("localhost", 10028))

    print("DEBUG Verbundung zum Server hergestellt!")

    print("RECIEVED:", client_socket.recv(512).decode())

    client_socket.close()

if __name__ == "__main__":
    main()