import os
import threading, time
import json
import socket

from Board import Board
from Food import Food
from Snake import Snake, SnakeTail

class Engine(object):

    STOP = False

    def __init__(self, player_list, config):
        self.config = config
        self.player_list = player_list
        self.socket = player_list[0].socket # temporär

        self.board = Board()
        self.snake = Snake(self.board, player_list[0])
        self.snake_list = []
        self.snake_list.append(self.snake)
        self.food = Food(self.board)

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

            self.snake.tick()
            self.snake.might_eat(self.food)

            if self.snake.is_dead:
                self.STOP = True

            self.__send_data()

            time.sleep(1 / self.config["ticksPerSecond"])

    def __send_data(self):
        # TODO: GameData aufteilen und pro Schlange senden?
        # -> Falls Anzahl an Bytes zu groß werden
        try:
            self.socket.send(str.encode(self.__build_json_str()))
            self.__debug("Daten zum Client gesendet.")
        except OSError as err:
            print("WARNING", err)

    def __build_json_str(self):
        drawables = []
        drawables.extend(self.snake.body)
        drawables.append(self.food)

        draw = [{"coords": drawable.coords, "symbol": drawable.SYMBOL} for drawable in drawables]

        game_data = {
            "state": "running" if not self.STOP else "stopped",
            "draw": draw
        }

        if not self.STOP:
            scoreboard = {snake.player.name: len(snake) for snake in self.snake_list}
            scoreboard["Spieler 2"] = 99999 # temp
            scoreboard["Spieler 3"] = 99999 # temp
            scoreboard["Spieler 4"] = 99999 # temp
            game_data["scoreboard"] = scoreboard

        return json.dumps(game_data)

    def __debug(self, msg):
        if self.config["debug"]:
            print(f"DEBUG {msg}")