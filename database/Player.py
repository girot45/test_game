class Player:
    def __init__(self, player_id: int, name: str, best_scores: int):
        self.id = player_id
        self.name = name
        self.best_scores = best_scores

    def set_scores(self, scores: int):
        self.best_scores = scores

