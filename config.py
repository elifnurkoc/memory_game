import os
import json
from memory_game.message_translator import MessageTranslator


class Config:

    __MAX_SIZE = 4
    __MIN_SIZE = 2
    __CHARACTERS = [" AA ", " BB ", " CC ", " DD ", " EE ", " FF ", " GG ", " HH "]
    __LANGUAGE = "en"

    def __init__(self, config_file):
        self.config_file = config_file
        self.message_translator = MessageTranslator()

        if not os.path.exists(config_file):
            raise IOError(self.message_translator.messages["not_exist"])

        self.__read_config_file()

    def __read_config_file(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def get_min_size(self):
        return self.config.get("min_size", self.__MIN_SIZE)

    def get_max_size(self):
        return self.config.get("max_size", self.__MAX_SIZE)

    def get_characters(self):
        return self.config.get("characters", self.__CHARACTERS)

    def get_characters_visual(self):
        return self.config.get("character_visuals", None)

    def get_back_image(self):
        return self.config.get("back_image", None)

    def get_language(self):
        return self.config.get("language", self.__LANGUAGE)

    def __repr__(self):
        return str(self.config)