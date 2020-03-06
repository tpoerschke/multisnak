import sys

from Drawable import Drawable
from Food import Food
from Board import Board

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

    def __init__(self, board, player):
        self.board = board
        self.player = player

        self.__head = SnakeHead((5,5), "right")
        self.body = []

        self.is_dead = False

        self.body += [self.__head]

        self.body.append(SnakeTail((4,5)))
        self.body.append(SnakeTail((3,5)))

    def __len__(self):
        return len(self.body)

    def tick(self):
        if not self.is_dead:
            self.move(self.player.requested_direction)
            self.__self_collision()
            self.__board_collision()

    def move(self, direction):
        # Neue Richtung muss auf dem Kopf gesetzt werden.
        # Zuvor jedoch muss die vorhandene Richtung jeweils
        # um ein Körperteil nach hinten gereicht werden, 
        # damit die Schlange auch um "die Kurve" kriecht.
        for i in range(len(self.body) - 1, 0, -1):
            part = self.body[i]
            part.move(self.body[i-1].coords)
            #self.board.draw(part)

        # Anschließend die neue Richtung am Kopf setzen
        self.__head.move(direction)
        #self.board.draw(self.__head)

        sys.stdout.flush()

    def might_eat(self, food : Food):
        if not food.eaten and food.coords == self.__head.coords:
            food.consume()
            self.__grow(food.times_eaten)
    
    def __grow(self, amount):
        for _ in range(amount):
            self.body.append(SnakeTail(self.body[-1].coords))

    def __board_collision(self):
        # Überprüft, ob der Kopf der Schlange, den Rand erreicht hat
        x, y = self.__head.coords
        if x == 0 or x == Board.width - 1 or y == 0 or y == Board.height - 1:
            self.is_dead = True

    def __self_collision(self):
        # Bei 1 beginnend, da der Kopf an 0ter Stelle liegt
        for i in range(1, len(self.body)):
            if self.__head.coords == self.body[i].coords:
                self.is_dead = True