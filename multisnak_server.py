from server import Server, load_config

def main():
    load_config("server.config.yaml")
    server = Server()
    server.connect_clients()
    server.do_game_loop()

if __name__ == "__main__":
    main()