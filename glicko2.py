import config

import math
import numpy

WIN: float = 1
LOSS: float = 0
DRAW: float = 0.5

def to_glicko2(glicko: float) -> float:
    return (glicko - 1500) / 173.7178

def to_rd2(rd: float) -> float:
    return rd / 173.7178

def to_glicko(glicko2: float) -> float:
    return 173.7178 * glicko2 + 1500

def to_rd(rd2: float) -> float:
    return 173.7178 * rd2

def g(rd: float) -> float:
    return 1 / math.sqrt(1 + 3 * (rd ** 2) / (math.pi ** 2))

def E(glicko2: float, glicko2j: float, rdj: float) -> float:
    return 1 / (1 + math.exp(-g(rdj) * (glicko2 - glicko2j)))

def variance(glicko2: float, enemy_glicko2: float, enemy_rd2: float) -> float:
    result_E: float = E(glicko2, enemy_glicko2, enemy_rd2)
    return ((g(enemy_rd2) ** 2) * result_E * (1 - result_E)) ** -1

def improvement(variance: float, glicko2: float, enemy_glicko2: float, enemy_rd2: float, result: float) -> float:
    return (g(enemy_rd2) * (result - E(glicko2, enemy_glicko2, enemy_rd2))) * variance

def f(x: float, variance: float, improvement: float, rd2: float, a: float) -> float:
    result_exp: float = math.exp(x)
    return (result_exp * ((improvement ** 2) - (rd2 ** 2) - variance - result_exp)
            / 2 * (((rd2 ** 2) + variance + result_exp) ** 2) - ((x - a) / (config.SYSTEM_CONSTANT ** 2)))

def new_volatility(volatility: float, variance: float, improvement: float, rd2: float) -> float:
    a: float = numpy.log(volatility ** 2)
    b: float
    c: float
    k: float

    if improvement ** 2 > (rd2 ** 2) + variance:
        b = numpy.log((improvement ** 2) - (rd2 ** 2) - variance)
    else:
        k = 1

        while f(a - k * config.SYSTEM_CONSTANT, variance, improvement, rd2, a) < 0:
            k += 1

        b = a - k * config.SYSTEM_CONSTANT

    Fa: float = f(a, variance, improvement, rd2, a)
    Fb: float = f(a, variance, improvement, rd2, a)
    Fc: float

    while math.fabs(b - a) > 0.000001:
        c = a + (a - b) * Fa / (Fb - Fa)
        Fc = f(c, variance, improvement, rd2, a)

        if Fc * Fb <= 0:
            a = b
            Fa = Fb
        else:
            Fa /= 2

        b = c
        Fb = Fc

    return math.exp(a / 2)

def pre_rating_rd(rd2: float, new_volatility: float) -> float:
    return math.sqrt((rd2 ** 2) +(new_volatility ** 2))

def new_rd(pr_rd2: float, variance: float) -> float:
    return 1 / math.sqrt((1 / (pr_rd2 ** 2)) + (1 / variance))

def new_glicko(new_rd2: float, glicko2: float, enemy_glicko2: float, enemy_rd2: float, result: float) -> float:
    return glicko2 + (new_rd2 ** 2) * (g(enemy_rd2) * (result - E(glicko2, enemy_glicko2, enemy_rd2)))

def glixare_percentile(glicko: float, rd: float) -> float:
    return 10000 / (1 + (10 ** (((1500 - glicko) * math.pi / math.sqrt(
        3 * (numpy.log(10) ** 2) * (rd ** 2) + 2500 * (64 * (math.pi ** 2) + 147 * (numpy.log(10) ** 2))))))) / 10000

def glixare_rating(glixare_percentile: float) -> float:
    return glixare_percentile * config.MAX_GLIXARE_RATING
