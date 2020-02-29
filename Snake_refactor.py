import termios, tty, sys, codecs
from contextlib import contextmanager

import os
import signal
import random
import time
import threading

STOP = False

#### START USER INPUT ####

@contextmanager
def cbreak():
    # Input-Modus einstellen, sodass die Benutzereingabe
    # nicht angeziegt wird
    old_attrs = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    try:
        yield
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attrs)

def user_input_handler():
    # Dieser Generator dekodiert stdin, sodass über Unicode-Zeichen
    # iteriert werden kann
    with cbreak():
        while True:
            yield sys.stdin.read(3)

def stop_program(signum, frame):
    global STOP
    STOP = True
    go_to_terminal_coords(0, Board.height)
    sys.stdout.write("Spiel beendet. Pfeiltaste drücken...")

def user_input_mapper():
    global STOP
    text = ""
    for c in user_input_handler():
        if STOP: break
        if c == "\x1b[A": Engine.direction = "up"
        if c == "\x1b[C": Engine.direction = "right"
        if c == "\x1b[B": Engine.direction = "down"
        if c == "\x1b[D": Engine.direction = "left"

#### ENDE USER INPUT ####

def go_to_terminal_coords(x, y):
    # Koordinaten des Terminals starten bei 1,1
    sys.stdout.write("\033[{0};{1}f".format(y+1, x+1))

class Engine(object):

    direction = "right"

    def __init__(self):
        self.board = Board()
        self.snake = Snake(self.board)
        self.food = Food(self.board)

        self.input_thread = threading.Thread(target=user_input_mapper)
        self.tick_thread = threading.Thread(target=self.tick)

    def start(self):
        os.system("clear")

        self.input_thread.start()
        self.tick_thread.start()

    def tick(self):
        global STOP
        while not STOP:
            self.board.clear()
            self.board.draw_frame()

            self.food.tick()

            self.snake.move(Engine.direction)
            self.snake.might_eat(self.food)

            time.sleep(0.1)

class Drawable(object):
    def __init__(self, coords, symbol):
        self.coords = coords
        self.symbol = symbol

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

        self.__body += [self.__head]

        self.__body.append(SnakeTail((4,5)))
        self.__body.append(SnakeTail((3,5)))

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


class Board(object):
    width = 100
    height = 40

    BORDER_SYMBOL = "#"

    def draw_frame(self):
        # Horizontale Rahmen
        for i in range(Board.width):
            # Rahmen oben
            go_to_terminal_coords(i, 0)
            sys.stdout.write(Board.BORDER_SYMBOL)
            # Rahmen unten
            go_to_terminal_coords(i, Board.height - 1)
            sys.stdout.write(Board.BORDER_SYMBOL)

        # Vertikale Rahmen
        for i in range(Board.height):
            # Rahmen links
            go_to_terminal_coords(0, i)
            sys.stdout.write(Board.BORDER_SYMBOL)
            # Rahmen rechts
            go_to_terminal_coords(Board.width - 1, i)
            sys.stdout.write(Board.BORDER_SYMBOL) 

        sys.stdout.flush()

    def draw_symbol(self, coords, symbol):
        x, y = coords
        go_to_terminal_coords(x, y)
        sys.stdout.write(symbol)

    def draw(self, obj : Drawable):
        x, y = obj.coords
        go_to_terminal_coords(x, y)
        sys.stdout.write(obj.symbol)

    def clear(self):
        for i in range(Board.width):
            for j in range(Board.height):
                go_to_terminal_coords(i,j)
                sys.stdout.write(" ")
        
        sys.stdout.flush()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_program)

    engine = Engine()
    engine.start()

