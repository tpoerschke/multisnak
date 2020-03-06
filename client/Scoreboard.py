from .terminal_tools import *
from .Board import Board

class Scoreboard:

    headline = "SCOREBOARD"

    def __init__(self):
        self.data = {}
        self.y = Board.height + 1
        self.height = 3
        self.col_width = 40

    def draw(self, new_data):
        self.data = new_data
        self.__clear()
        go_to_terminal_coords(0, self.y)
        sys.stdout.write("SCOREBOARD")
        y = self.y + 1
        counter = 0
        for key in self.data:
            go_to_terminal_coords(0 if counter % 2 == 0 else self.col_width, y + counter // 2)
            sys.stdout.write(f"{key}: {self.data[key]}".ljust(self.col_width))
            counter += 1
        sys.stdout.flush()

    def __clear(self):
        for i in range(0, self.col_width * 2):
            for j in range(self.y, self.height):
                go_to_terminal_coords(i,j)
                sys.stdout.write(" ")
        
        sys.stdout.flush()