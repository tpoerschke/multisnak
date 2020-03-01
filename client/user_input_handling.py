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

# Deprecated
def stop_program(signum, frame):
    Engine.STOP = True
    #go_to_terminal_coords(0, Board.height)
    print("Spiel beendet. Pfeiltaste drücken...")

def user_input_mapper(engine):
    for c in user_input_handler():
        if engine.STOP: break
        if c == "\x1b[A": engine.direction = "up"
        if c == "\x1b[C": engine.direction = "right"
        if c == "\x1b[B": engine.direction = "down"
        if c == "\x1b[D": engine.direction = "left"

