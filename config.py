import os

FILE_NAME: str = 'glicko2.properties'

SYSTEM_CONSTANT: float = 0.5
UNRANKED_GLICKO: float = 1500
UNRANKED_RD: float = 350
UNRANKED_VOLATILITY: float = 0.06
MAX_GLIXARE_RATING: float = 25000

def set_property(key: str, value: float):
    global SYSTEM_CONSTANT
    global UNRANKED_GLICKO
    global UNRANKED_RD
    global UNRANKED_VOLATILITY
    global MAX_GLIXARE_RATING

    match key:
        case 'system-constant':
            SYSTEM_CONSTANT = value
        case 'unranked-glicko':
            UNRANKED_GLICKO = value
        case 'unranked-rd':
            UNRANKED_RD = value
        case 'unranked-volatility':
            UNRANKED_VOLATILITY = value
        case 'max-glixare-rating':
            MAX_GLIXARE_RATING = value

def save():
    with open(FILE_NAME, 'w') as f:
        properties: list[str] = [
            'system-constant=' + str(SYSTEM_CONSTANT),
            'unranked-glicko=' + str(UNRANKED_GLICKO),
            'unranked-rd=' + str(UNRANKED_RD),
            'unranked-volatility=' + str(UNRANKED_VOLATILITY),
            'max-glixare-rating=' + str(MAX_GLIXARE_RATING)
        ]

        for property in properties:
            f.write(property + '\n')

        f.close()

def load():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME) as f:
            for line in f.readlines():
                kv = line.split('=')

                try:
                    set_property(kv[0], float(kv[1]))
                except TypeError:
                    continue
    else:
        save()
