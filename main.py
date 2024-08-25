import glicko2
import config
import database

from flask import Flask, request

config.load()
database.load()

app: Flask = Flask(__name__)

@app.route('/add-default')
def add_player_with_defaults():
    player_name: str = request.args['player']
    override: bool = bool(request.args['override'])
    if not player_name in database.players.keys():
        database.players[player_name] = [config.UNRANKED_GLICKO, config.UNRANKED_RD, config.UNRANKED_VOLATILITY]

@app.route('/add-custom')
def add_player_with_custom_settings():
    player_name: str = request.args['player']
    glicko: float = float(request.args['glicko'])
    rd: float = float(request.args['rd'])
    volatility: float = float(request.args['volatility'])

@app.route('/stats')
def get_stats():
    player_name: str = request.args['player']
    return database.players[player_name]

@app.route('/gxe-percentile')
def get_gxe_percentile():
    player_name: str = request.args['player']
    player_stats: list[float] = database.players[player_name]
    return glicko2.glixare_percentile(player_stats[0], player_stats[1])

@app.route('/gxe-rating')
def get_gxe_rating():
    player_name = request.args['player']
    player_stats: list[float] = database.players[player_name]
    glixare_percentile: float = glicko2.glixare_percentile(player_stats[0], player_stats[1])
    return glicko2.glixare_rating(glixare_percentile)

app.run(debug=True)
