import json

class LevelManager(object):

    __LEVEL_PATH = "server/levels/"
    __LEVEL_FORMAT = ".json"

    def __init__(self):
        # Hier werden die json-Objekte gespeichert, welche
        # die einzelnen Level beschreiben. Die Reihenfolge
        # der Level bleibt erhalten, wenn die Level der 
        # Liste nach geladen werden
        self.levels = {}
        self.current_level = {}
        self.current_level_index = -1

    def load_levels(self, level_list):
        # Level aus den entsprechenden Dateien laden
        for level in level_list:
            with open(self.__LEVEL_PATH + level + self.__LEVEL_FORMAT, "r") as file:
                self.levels[level] = json.load(file)

        if len(list(self.levels.keys())) == 0:
            raise ValueError("No Levels loaded")

    def next_level(self):
        self.current_level_index += 1
        self.current_level = self.levels[list(self.levels.keys())[self.current_level_index]]

        # TODO: Return False, wenn kein neues Level mehr geladen werden kann
        return True

    