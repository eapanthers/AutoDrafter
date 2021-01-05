from scipy.stats import chi2


class Player:
    def __init__(self):
        self.adp = 0
        self.proj_points = 0
        self.name = "None"
        self.prob_available = 0
        self.emission_table = {}
        self.picked = False

    def __init__(self, adp: float, proj: float, name: str):
        self.adp = adp
        self.proj_points = proj
        self.name = name
        self.prob_available = 0
        self.emission_table = {}
        self.picked = False

    def get_prob_available(self, pick: int, next_pick: int, randomness: float) -> float:
        if self.picked:
            self.emission_table[pick] = 0
            self.emission_table[next_pick] = 0
            return 0
        if pick in self.emission_table.keys():
            return self.emission_table[pick]
        if pick < self.adp < next_pick:
            prob = 1 - chi2.cdf(next_pick, (self.adp / randomness) ** 2)
            self.emission_table[pick] = prob
            return prob
        else:
            self.emission_table[pick] = 1
            return 1

    def pick(self) -> None:
        self.picked = True
