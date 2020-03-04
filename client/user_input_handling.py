import termios, sys, tty
from contextlib import contextmanager

#sys.path.append("..") # Temporär für import unten
#from .terminal_tools import *
#from .Board import Board

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

def user_input_mapper(client):
    opposite_list = [{"up", "down"}, {"left", "right"}]
    for c in user_input_handler():
        if client.STOP: break

        # Richtung über Pfeiltasten ermitteln
        new_direction = ""
        if c == "\x1b[A": new_direction = "up"
        if c == "\x1b[C": new_direction = "right"
        if c == "\x1b[B": new_direction = "down"
        if c == "\x1b[D": new_direction = "left"

        # Input validieren, damit der Spieler nicht umkehren kann
        # (würde außerdem zum sofortigen Tod der Schlange führen)
        if {client.direction, new_direction} not in opposite_list:
            client.direction = new_direction


