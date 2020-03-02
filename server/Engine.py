import os
import threading, time
import json
import socket

from Board import Board
from Food import Food
from Snake import Snake, SnakeTail

class Engine(object):

    STOP = False
    direction = "right"

    def __init__(self, socket : socket.socket):
        # Später sollte die Engine eine liste aller Client-Threads bekommen
        self.socket = socket

        self.board = Board()
        self.snake = Snake(self.board, self)
        self.food = Food(self.board)

        #self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.tick_thread = threading.Thread(target=self.tick)

    def start(self):
        #os.system("clear")

        #self.input_thread.start()
        self.tick_thread.start()

    def tick(self):
        while not self.STOP:
            print("DEBUG tick")
            #self.board.clear()
            #self.board.draw_frame()

            self.food.tick()

            self.snake.tick()
            self.snake.might_eat(self.food)

            if self.snake.is_dead:
                self.STOP = True

            self.__send_data()

            time.sleep(0.1)

    def __send_data(self):
        try:
            self.socket.send(str.encode(self.__build_json_str()))
            print("DEBUG Daten zum Client gesendet.")
        except OSError as err:
            print("WARNING", err)

    def __build_json_str(self):
        drawables = []
        drawables.extend(self.snake.body)
        drawables.append(self.food)

        draw = [{"coords": drawable.coords, "symbol": drawable.SYMBOL} for drawable in drawables]

        game_data = {
            "draw": draw
        }

        return json.dumps(game_data)