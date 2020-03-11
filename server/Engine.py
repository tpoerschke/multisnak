import os
import threading, time
import json
import socket

from .Board import Board
from .Food import Food
from .Snake import Snake, SnakeTail

class Engine(object):

    STOP = False

    def __init__(self, player_list, config):
        self.config = config
        self.player_list = player_list

        self.board = Board()
        self.snake_list = [Snake(self.board, player) for player in self.player_list]
        self.food = Food(self.board)

        # Flag setzen, damit sich die Schlange nicht bewegt (Debug / temporär)
        if len(self.snake_list) >= 2: self.snake_list[1].frozen = True
            
        #self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.tick_thread = threading.Thread(target=self.tick)

    def start(self):
        #os.system("clear")

        #self.input_thread.start()
        self.tick_thread.start()

    def tick(self):
        while not self.STOP:
            #self.board.clear()
            #self.board.draw_frame()

            self.food.tick()

            snakes_alive = list(filter(lambda snake: not snake.is_dead, self.snake_list))

            for snake in self.snake_list:
                if not snake.is_dead:
                    snake.tick()
                    snake.snake_collision(snakes_alive)
                    snake.might_eat(self.food)
                elif len(self.snake_list) > 1:
                    # respawn, wenn multiplayer
                    snake.respawn()
    
            snakes_alive_count = len(snakes_alive)
            # Der zweite Teil der Abfrage, macht den Singleplayer-Modus möglich
            # TODO: Diese Abfrage überarbeiten! 
            #if (len(self.snake_list) > 1 and snakes_alive_count <= 1) or (snakes_alive_count < 1):#
            if snakes_alive_count < 1: # Server stoppt nur im Singleplayer-Modus momentan
                self.STOP = True

            self.__send_data()

            time.sleep(1 / self.config["ticksPerSecond"])

    def __send_data(self):
        # TODO: GameData aufteilen und pro Schlange senden?
        # -> Falls Anzahl an Bytes zu groß werden
        try:
            data = str.encode(self.__build_json_str())
            for player in self.player_list:
                player.socket.send(data)
                self.__debug("Daten zum Client gesendet.")
        except OSError as err:
            print("WARNING", err)

    def __build_json_str(self):
        draw = {}

        draw["snakes"] = {}
        for snake in self.snake_list:
            draw["snakes"][snake.player.id] = [body.coords for body in snake.body]
        
        draw["food"] = self.food.coords

        game_data = {
            "state": "running" if not self.STOP else "stopped",
            "draw": draw
        }

        if not self.STOP:
            game_data["scoreboard"] = {snake.player.name: len(snake) for snake in self.snake_list}

        return json.dumps(game_data)

    def __debug(self, msg):
        if self.config["debug"]:
            print(f"DEBUG {msg}")