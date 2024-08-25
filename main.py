import glicko2
import config
import database

import atexit
from flask import Flask, request, make_response

config.load()
database.load()

app: Flask = Flask(__name__)

already_cleaning_up: bool = False

@app.route('/add-default')
def add_player_with_defaults():
    player_name: str = request.args['player']
    override: bool = bool(request.args['override'])
    if not player_name in database.players.keys() or override:
        database.players[player_name] = [config.UNRANKED_GLICKO, config.UNRANKED_RD, config.UNRANKED_VOLATILITY]
        return make_response('OK', 200)
    return make_response('Bad Request', 400)

@app.route('/add-custom')
def add_player_with_custom_settings():
    player_name: str = request.args['player']
    override: bool = bool(request.args['override'])
    glicko: float = float(request.args['glicko'])
    rd: float = float(request.args['rd'])
    volatility: float = float(request.args['volatility'])
    if not player_name in database.players.keys() or override:
        database.players[player_name] = [glicko, rd, volatility]
        return make_response('OK', 200)
    return make_response('Bad Request', 400)

@app.route('/remove')
def remove_player():
    player_name: str = request.args['player']
    database.players.pop(player_name)
    return make_response('OK', 200)

@app.route('/stats')
def get_stats():
    player_name: str = request.args['player']
    return database.players[player_name]

@app.route('/get-all')
def get_all():
    return database.players

@app.route('/gxe-percentile')
def get_gxe_percentile():
    player_name: str = request.args['player']
    player_stats: list[float] = database.players[player_name]
    return str(glicko2.glixare_percentile(player_stats[0], player_stats[1]))

@app.route('/gxe-rating')
def get_gxe_rating():
    player_name = request.args['player']
    player_stats: list[float] = database.players[player_name]
    glixare_percentile: float = glicko2.glixare_percentile(player_stats[0], player_stats[1])
    return str(glicko2.glixare_rating(glixare_percentile))

@app.route('/update')
def update():
    winner_name: str = request.args['winner']
    loser_name: str = request.args['loser']
    database.update_rankings(winner_name, loser_name)
    return make_response('OK', 200)

def cleanup():
    global already_cleaning_up

    print("cleaning up")
    if already_cleaning_up:
        return

    already_cleaning_up = True
    config.save()
    database.save()

# note that cleanup() runs twice on debug mode for no reason
app.run(debug=False)
atexit.register(cleanup)
