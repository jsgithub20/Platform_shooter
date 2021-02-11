class GameState:
    def __init__(self, game_id):
        self.game_id = game_id
        self.roles = ["shooter", "chopper"]
        self.match_types = ["Deathmatch", "1st23", "Best of 3"]
        self.match_score = {"match_type": self.match_types[0], "round": 0, "shooter": 0, "chopper": 0,
                            "map": 0, "game_finished": False}
        self.map = 0
        self.ready = False
