import math

from memory_game.config import Config
from memory_game.message_translator import MessageTranslator


class Visualizer:
    """
    This class is used to display any kind information in the selected language.
    """

    def __init__(self, config: Config):
        self.message_translator = MessageTranslator()

        # Not used for this particular base class but can used in the inherited classes.
        self.config = config

    def show_map(self, map_object):
        size = int(math.sqrt(len(map_object)))

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for y in range(0, size):
            line = []
            for x in range(0, size):
                idx = y * size + x
                line.append(map_object[idx])
            print(''.join(line))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def show_turn_header(self, player: object, mask):
        print(self.message_translator.messages["turn"].format(player))
        self.show_map(mask)
