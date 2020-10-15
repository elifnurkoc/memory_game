import random
from copy import copy

from memory_game.message_translator import MessageTranslator
from memory_game.interactor import Interactor
from memory_game.visualizer import Visualizer
from memory_game.config import Config
from memory_game.player import Player


class Game:
    """
    Main class holding the game state and to execute game logic
    """

    def __init__(self, config: Config):

        # Dependent classes:
        self.message_translator = MessageTranslator()
        self.interactor = Interactor()
        self.visualizer = Visualizer(config)

        # These instance variables can be initialized by the config file
        self.min_size = config.get_min_size()
        self.max_size = config.get_max_size()
        self.characters = config.get_characters()
        self.set_language(config.get_language())

        # Initialization of the instance variables
        self.map = None
        self.mask = None
        self.player_list = []
        self.all_moves = []
        self.player_matching_moves = {}
        self.turn_owner_idx= 0

    def get_current_player(self) -> Player:
        """
        Returns the player who owns the turn

        :return: Player
        """
        return self.player_list[self.turn_owner_idx]

    def create_map(self, size: int) -> tuple:
        """
        Selects the characters randomly and forms the distribution for the game board

        What is map and mask?
        Map: The main character distribution

        Mask: Current state of the game board. Some characters are revealed, some are hidden, as they are not discovered yet.
        The numbers within are representing the backside of the cards in the original game. Also numbers are used to
        index the card position.

        :param size: Size of one edge of the game board
        :return: tuple holding the map and mask
        """
        if size % 2 == 1:
            size += 1
            print(self.message_translator.messages["new_size"].format(size))

        # Limiting the size within the determined min max board size
        size = max(min(size, self.max_size), self.min_size)
        chr_size = int(size**2 / 2)

        # Play sequence is randomized
        random.shuffle(self.characters)
        choosen_characters = self.characters[:chr_size]
        choosen_characters += choosen_characters
        random.shuffle(choosen_characters)

        # Creation of map and mask
        map = [choosen_characters[i] for i in range(0, size**2)]
        mask = [' {:02d} '.format(i) for i in range(0, size**2)]

        return map, mask

    def uncover_mask(self, move: tuple) -> None:
        """
        Flipping the cards if they are matching

        :param move: Player's matching move in form of (card index, card index)
        """
        f, s = move
        self.mask[f] = self.map[f]
        self.mask[s] = self.map[s]

    def show_map(self) -> None:
        """
        Displays the game map with open characters. Useful for debugging.
        """
        self.visualizer.show_map(self.map)

    def show_mask(self) -> None:
        """
        Displays the current status of the game board.

        :return: None
        """
        self.visualizer.show_map(self.mask)

    def add_player(self, player: Player) -> None:
        """
        Adds a new player to the game.

        :param player:
        """
        self.player_matching_moves[player] = []
        self.player_list.append(player)

    def start(self) -> None:
        """
        Main game loop.
        """
        # Ask user to get the board size
        board_size = self.interactor.get_game_size()

        # Ask user to get the player count
        user_input = self.interactor.get_player_size()

        # Create data for the game board
        self.map, self.mask = self.create_map(board_size)

        # Shuffle the players
        random.shuffle(self.player_list)

        # Ask for the player names
        for i in range(0, user_input):
            p = self.interactor.get_player_name(i+1)
            self.add_player(Player(p))

        while True:
            # Displays the player name
            self.show_turn_header()

            try:
                # Ask for the players move
                move = self.interactor.get_player_move()
            except Exception as e:
                print(self.message_translator.messages["invalid"])
                continue

            # Check if the move is a valid one
            if not self.is_move_valid(move):
                print(self.message_translator.messages["invalid"])
                continue

            # Play the turn and display the current status of the board
            self.player_turn(move)
            self.show_mask_with_player_move()

            # Check if the game is over, declare winners
            if self.is_over():
                print(self.message_translator.messages["g_over"])
                self.show_result()
                break

    def set_language(self, language: str) -> None:
        """
        Sets the game language. Default is english.

        :param language: Abbreviation of the supported languages in string form
        """
        if language == "tr":
            self.interactor.message_translator.set_turkish()
            self.visualizer.message_translator.set_turkish()
            self.message_translator.set_turkish()
        elif language == "de":
            self.interactor.message_translator.set_german()
            self.visualizer.message_translator.set_german()
            self.message_translator.set_german()

    def is_move_valid(self, move: tuple) -> bool:
        """
        Checks if the players move a valid one.

        :param move: tuple of card indexes
        :return: bool
        """

        first, second = move

        board_length = len(self.map)

        # Card indices are within the game board
        if first < 0 or second < 0 or first >= board_length or second >= board_length:
            return False

        # Two indices cannot be equal to each other
        if first == second:
            return False

        # Indices cannot be chosen from the open cards
        if self.map[first] == self.mask[first] or self.map[second] == self.mask[second]:
            return False

        return True

    def player_turn(self, move: tuple) -> bool:
        """
        Player opens two cards.

        If cards are not matching, turn is switched.

        :param move: ...
        :return: true if user find matching pairs, false if not.
        """
        player = self.player_list[self.turn_owner_idx]
        self.all_moves.append(move)

        first, second = move
        if self.map[first] == self.map[second]:
            self.uncover_mask(move)
            self.player_matching_moves[player].append(move)
            return True

        self.__switch_turn()
        return False

    def __switch_turn(self) -> None:
        """
        Switches the turn to the next player.
        """
        self.turn_owner_idx = (self.turn_owner_idx + 1) % len(self.player_list)

    def show_turn_header(self) -> None:
        """
        Displays the name of the turn owner.
        """
        self.visualizer.show_turn_header(self.get_current_player(), self.mask)

    def show_mask_with_player_move(self) -> None:
        """
        After the player turn, players choices must be shown to all players, so that all players can see and memorize
        the underlying cards.
        """
        if not len(self.all_moves):
            self.visualizer.show_map(self.mask)
            return

        # Get the latest move in the game (independent from players)
        move = self.all_moves[-1]
        f, s = move

        # copy of the local mask, we dont adjust the main mask, just the copy of it.
        # This is used only for displaying information, not holding player turn information.
        local_mask = copy(self.mask)
        local_mask[f] = self.map[f]
        local_mask[s] = self.map[s]
        self.visualizer.show_map(local_mask)

    def is_over(self) -> bool:
        """
        :return: True if the game is over.
        """
        if self.mask == self.map:
            return True
        return False

    def show_result(self) -> None:
        """
        Displays the game result information. Including final scores and winners.
        If there is a draw, those players are declared as winners.
        """
        sorted_matching_moves = sorted(self.player_matching_moves.items(), key=lambda x: len(x[1]), reverse=True)
        winning_score = len(sorted_matching_moves[0][1])

        winners = []
        for player, moves in sorted_matching_moves:
            print("{}: \t{}".format(player, len(moves)))
            if len(moves) == winning_score:
                winners.append(player)
        print(self.message_translator.messages["win"].format(winners))


def main():
    game = Game(Config("config.json"))
    game.start()


if __name__ == "__main__":
    main()

