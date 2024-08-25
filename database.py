import glicko2
import config

import os

# key: name, value: [glicko, rd, volatility]
players: dict[str, [float, float, float]] = {}

FILE_NAME: str = 'rankings.csv'

class Player():
    def __init__(self, glicko: float, rd: float, volatility: float):
        self.glicko: float = glicko
        self.rd: float = rd
        self.volatility: float = volatility

        self.glicko2: float = glicko2.to_glicko2(glicko)
        self.rd2: float = glicko2.to_rd2(rd)

    def get_updated_values(self, enemy, result: float) -> list[float]:
        variance: float = glicko2.variance(self.glicko2, enemy.glicko2, enemy.rd2)
        improvement: float = glicko2.improvement(variance, self.glicko2, enemy.glicko2, enemy.rd2, result)
        new_volatility: float = glicko2.new_volatility(self.volatility, variance, improvement, self.rd2)
        pr_rd2: float = glicko2.pre_rating_rd(self.rd2, new_volatility)
        new_rd2: float = glicko2.new_rd(pr_rd2, variance)
        new_glicko2: float = glicko2.new_glicko(new_rd2, self.glicko2, enemy.glicko2, enemy.rd2, result)

        new_glicko: float = glicko2.to_glicko(new_glicko2)
        new_rd: float = glicko2.to_rd(new_rd2)

        if new_rd > config.UNRANKED_RD:
            new_rd = config.UNRANKED_RD

        return [new_glicko, new_rd, new_volatility]

def save():
    with open(FILE_NAME, 'w') as f:
        for player in players:
            glicko: str = str(players[player][0])
            rd: str = str(players[player][1])
            volatility: str = str(players[player][2])

            f.write(f'{player},{glicko},{rd},{volatility}\n')

def load():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME) as f:
            for line in f.readlines():
                values: list[str] = line.split(',')
                players[values[0]] = [float(values[1]), float(values[2]), float(values[3])]
    else:
        save()

def update_rankings(winner_name: str, loser_name: str) -> None:
    winner: Player = Player(players[winner_name][0], players[winner_name][1], players[winner_name][2])
    loser: Player = Player(players[loser_name][0], players[loser_name][1], players[loser_name][2])

    players[winner_name] = winner.get_updated_values(loser, glicko2.WIN)
    players[loser_name] = loser.get_updated_values(winner, glicko2.LOSS)
