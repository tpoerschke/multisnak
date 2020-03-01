import sys 

def go_to_terminal_coords(x, y):
    # Koordinaten des Terminals starten bei 1,1
    sys.stdout.write("\033[{0};{1}f".format(y+1, x+1))