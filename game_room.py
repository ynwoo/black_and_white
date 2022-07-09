class Game_room:
    def __init__(self) -> None:
        self.members = []

        self.main_channel = None
        self.start = False
        self.can_join = False
        self.emojis = {
        "0\u20E3" : 0,
        "1\u20E3" : 1,
        "2\u20E3" : 2,
        "3\u20E3" : 3,
        "4\u20E3" : 4,
        "5\u20E3" : 5,
        "6\u20E3" : 6,
        "7\u20E3" : 7,
        "8\u20E3" : 8
        }