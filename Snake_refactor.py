import os, sys
import signal
import random
import time, threading

from client.user_input_handling import *
from client.terminal_tools import *
from client.Board import Board
from client.Drawable import Drawable

class Engine(object):

    STOP = False
    direction = "right"

    def __init__(self):
        self.board = Board()
        self.snake = Snake(self.board)
        self.food = Food(self.board)

        self.input_thread = threading.Thread(target=user_input_mapper, args=(self,))
        self.tick_thread = threading.Thread(target=self.tick)

    def start(self):
        os.system("clear")

        self.input_thread.start()
        self.tick_thread.start()

    def tick(self):
        while not ENGINE.STOP:
            self.board.clear()
            self.board.draw_frame()

            self.food.tick()

            self.snake.tick()
            self.snake.might_eat(self.food)

            if self.snake.is_dead:
                ENGINE.STOP = True

            time.sleep(0.1)

class Food(Drawable):
    
    SYMBOL = "+"

    def __init__(self, board):
        super().__init__(coords = (0, 0), symbol = Food.SYMBOL)

        self.board = board
        self.eaten = True # Damit Essen direkt zufällig spawnt

    def tick(self):
        if not self.eaten:
            self.board.draw(self)
        else:
            self.__spawn()

    def __spawn(self):
        # Board.width - 2 -> auf Board.width - 1 liegt der Rahmen
        # Selbiges gilt für die Höhe
        self.coords = (random.randrange(1, Board.width - 2), random.randrange(1, Board.height - 2))
        self.eaten = False


class SnakeTail(Drawable):
    
    SYMBOL = "O"

    def __init__(self, coords):
        super().__init__(coords, SnakeTail.SYMBOL)

    def move(self, new_coords):
        self.coords = new_coords

class SnakeHead(SnakeTail):
    def __init__(self, coords, direction):
        super().__init__(coords)

    def move(self, new_direction):
        x, y = self.coords
        if new_direction == "up":
            y = y - 1
        elif new_direction == "right":
            x = x + 1
        elif new_direction == "down":
            y = y + 1
        elif new_direction == "left":
            x = x - 1

        self.coords = (x, y)

class Snake(object):

    __head = SnakeHead((5,5), "right")
    __body = []

    def __init__(self, board):
        self.board = board

        self.is_dead = False

        self.__body += [self.__head]

        self.__body.append(SnakeTail((4,5)))
        self.__body.append(SnakeTail((3,5)))

    def tick(self):
        self.move(ENGINE.direction)
        self.__self_collision()
        self.__board_collision()

    def move(self, direction):
        # Neue Richtung muss auf dem Kopf gesetzt werden.
        # Zuvor jedoch muss die vorhandene Richtung jeweils
        # um ein Körperteil nach hinten gereicht werden, 
        # damit die Schlange auch um "die Kurve" kriecht.
        for i in range(len(self.__body) - 1, 0, -1):
            part = self.__body[i]
            part.move(self.__body[i-1].coords)
            self.board.draw(part)

        # Anschließend die neue Richtung am Kopf setzen
        self.__head.move(direction)
        self.board.draw(self.__head)

        sys.stdout.flush()

    def might_eat(self, food : Food):
        if food.coords == self.__head.coords:
            food.eaten = True
            self.__grow()
    
    def __grow(self):
        self.__body.append(SnakeTail(self.__body[-1].coords))

    def __board_collision(self):
        # Überprüft, ob der Kopf der Schlange, den Rand erreicht hat
        x, y = self.__head.coords
        if x == 0 or x == Board.width - 1 or y == 0 or y == Board.height - 1:
            self.is_dead = True

    def __self_collision(self):
        # Bei 1 beginnend, da der Kopf an 0ter Stelle liegt
        for i in range(1, len(self.__body)):
            if self.__head.coords == self.__body[i].coords:
                self.is_dead = True


ENGINE = Engine()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_program)

    ENGINE.start()

