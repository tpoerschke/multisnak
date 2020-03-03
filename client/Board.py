from terminal_tools import *
from Drawable import Drawable

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