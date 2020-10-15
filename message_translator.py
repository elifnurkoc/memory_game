class MessageTranslator:
    """
    Holds the displayable messages and their translation in multiple language
    """

    def __init__(self):
        self.messages = {
            "pick_first": "Pick your first card: ",
            "pick_second": "Pick your second card: ",
            "turn": "~~~ {}'s Turn ~~~",
            "not_exist": "Config file does not exist",
            "size": "Your value is rounded to {}",
            "game_size": "Game board size: ",
            "invalid": "Invalid move, please play again",
            "player_size": "How many players will play this game?: ",
            "g_over": "Game over",
            "win": "Winner: {}",
            "players": "enter {}. player's name: "
        }

    def set_turkish(self):
        self.messages["pick_first"] = "Ilk karti seciniz: "
        self.messages["pick_second"] = "Ikinci karti seciniz: "
        self.messages["turn"] = "~~~ {}'in sirasi  ~~~"
        self.messages["not_exist"] = "Yapılandırma dosyası mevcut değil"
        self.messages["size"] = "Degeriniz {}'a Yuvarlandi"
        self.messages["game_size"] = "Oyun tahtasi boyutu: "
        self.messages["invalid"] = "Gecersiz hamle. Lütfen tekrar oyna"
        self.messages["player_size"] = "Kac oyuncu oynayacak?: "
        self.messages["g_over"] = "Oyun Bitti"
        self.messages["win"] = "Kazanan: {}"
        self.messages["players"] = "{}. oyuncunun ismini girin: "

    def set_german(self):
        self.messages["pick_first"] = "Wähle erste Karte: "
        self.messages["pick_second"] = "Wähle zweite Karte: "
        self.messages["turn"] = "~~~ Reihe von {} ~~~"
        self.messages["not_exist"] = "Konfigurationsdatei existiert nicht"
        self.messages["new_size"] = "Ihr Wert wird auf {} gerundet"
        self.messages["game_size"] = "Spielfeldgröße: "
        self.messages["invalid"] = "Ungültiger Bewegung. Bitte noch einmal spielen"
        self.messages["player_size"] = "Wie viele spieler spielt dies Game?: "
        self.messages["g_over"] = "Spiel zu Ende"
        self.messages["win"] = "Sieger: {}"
        self.messages["players"] = "{}. Spielername eingeben: "
