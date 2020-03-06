import random

from .Board import Board
from .Drawable import Drawable

class Food(Drawable):
    
    SYMBOL = "+"

    def __init__(self, board):
        super().__init__(coords = (0, 0), symbol = Food.SYMBOL)

        self.board = board
        self.eaten = True # Damit Essen direkt zufällig spawnt
        self.times_eaten = 0

    def tick(self):
        if self.eaten:
            self.__spawn()

    def consume(self):
        if not self.eaten:
            self.eaten = True
            self.times_eaten += 1

    def __spawn(self):
        # Board.width - 2 -> auf Board.width - 1 liegt der Rahmen
        # Selbiges gilt für die Höhe
        self.coords = (random.randrange(1, Board.width - 2), random.randrange(1, Board.height - 2))
        self.eaten = False