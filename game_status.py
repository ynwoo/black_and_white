class Game_status:
    def __init__(self) -> None:
        self.round = 0
        self.first_player = None
        self.second_player = None
        self.turn = -1  # -1: members[0] turn, 1: members[1] turn
        self.game_results = {}
        self.scores= {}
        self.numeric_tiles = {}
