import sys

from .Drawable import Drawable
from .Food import Food
from .Board import Board
from .Player import Player

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

        # TODO: Spawn-Positionen relativ zum Kopf vorhalten, damit auch woanders gespawnt werden kann ?
        self.__spawn_positions = [(5,5 + (self.player.id * 2)), (4,5 + (self.player.id * 2)), (3,5 + (self.player.id * 2))]

        self.__head = SnakeHead(self.__spawn_positions[0], "right")
        self.body = []

        self.is_dead = False
        self.frozen = False # Wird momentan lediglich zum debug verwendet

        self.body += [self.__head]

        self.body.append(SnakeTail(self.__spawn_positions[1]))
        self.body.append(SnakeTail(self.__spawn_positions[2]))

    def __len__(self):
        return len(self.body)

    def tick(self):
        if not self.is_dead:
            self.move(self.player.requested_direction)
            self.__self_collision()
            self.__board_collision()

    def move(self, direction):
        if self.frozen: return
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

    def respawn(self):
        # Den Körper, um 10 Elemente verkleinern
        new_body = self.body[:-10]
        if len(new_body) < 3:
            new_body = self.body[:3]
        self.body = new_body

        # Neu positionieren
        for i in range(len(self)):
            self.body[i].coords = self.__spawn_positions[i] if i < len(self.__spawn_positions) else self.__spawn_positions[-1]
        
        # Richtung zurücksetzen
        self.player.requested_direction = Player.DEFAULT_DIRECTION

        self.is_dead = False

    def snake_collision(self, snake_list):
        for other_snake in snake_list:
            if other_snake is not self and any(filter(lambda part: part.coords == self.__head.coords, other_snake.body)):
                self.is_dead = True
                print(self.player.name + " ist tot!")
                break

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
                break