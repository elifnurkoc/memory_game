from memory_game.message_translator import MessageTranslator


class Interactor:
    """
    Base class for handling the user interaction. Uses console as an input medium.
    """

    def __init__(self):
        self.message_translator = MessageTranslator()

    def get_player_move(self):
        move_1 = int(input(self.message_translator.messages["pick_first"]))
        move_2 = int(input(self.message_translator.messages["pick_second"]))
        return move_1, move_2

    def get_game_size(self):
        game_size = int(input(self.message_translator.messages["game_size"]))
        return game_size

    def get_player_size(self):
        player_size = int(input(self.message_translator.messages["player_size"]))
        return player_size

    def get_player_name(self, idx):
        return input(self.message_translator.messages["players"].format(idx))