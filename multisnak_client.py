import signal

from client import load_config, Client

def main():
    load_config("client.config.yaml")
    client = Client()
    signal.signal(signal.SIGINT, client.stop) 

if __name__ == "__main__":
    main()