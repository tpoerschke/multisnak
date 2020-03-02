import random

from Board import Board
from Drawable import Drawable

class Food(Drawable):
    
    SYMBOL = "+"

    def __init__(self, board):
        super().__init__(coords = (0, 0), symbol = Food.SYMBOL)

        self.board = board
        self.eaten = True # Damit Essen direkt zufällig spawnt

    def tick(self):
        if not self.eaten:
            pass
            #self.board.draw(self)
        else:
            self.__spawn()

    def __spawn(self):
        # Board.width - 2 -> auf Board.width - 1 liegt der Rahmen
        # Selbiges gilt für die Höhe
        self.coords = (random.randrange(1, Board.width - 2), random.randrange(1, Board.height - 2))
        self.eaten = False