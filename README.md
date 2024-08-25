# PyGlicko2
Simple API written in Python for managing Glicko2 ratings of players

## How to use
1. Download the code into a directory
2. Make sure you have all the requirements which include but are not limited to: `flask`, `numpy`
3. Run `main.py`
4. If you would like to alter the settings, stop the program by pressing `Ctrl + C`
5. Edit the `glicko2.properties` file as desired
6. Run `main.py` and you're good to go!


This is intended to be used by other backends. There are no request headers or body needed currently, so you can just send a GET request as long as the URL contains all the needed parameters.

This is what a `/get-all` request and response would look like, for instance:

![image](https://github.com/user-attachments/assets/6c860dab-8e59-4f7b-9c70-990a1090e3de)

The floating point numbers in the arrays are the `glicko`, `rd`, and `volatility` in that order.


## Documentation

All parameters are a query in the request URL and **required**. For example, the parameters are in bold:

example.url/endpoint?**key=value&anotherkey=anothervalue**

For player names, you may want to input a player ID instead, depending on your needs.

### /add-default
Parameters:
- `player`: the name of the player
- `override`: whether to override any existing data for that player name (`True` or `False`)

### /add-custom

Parameters:
- `player`: the name of the player
- `override`: whether to override any existing data for that player name (`True` or `False`)
- `glicko`: the rating of the player
- `rd`: the rating deviation of the player
- `volatility`: the volatility of the player

### /remove
Parameters:
- `player`: the name of the player to remove

### /stats
Parameters:
- `player`: the name of the player to get stats of

### /get-all
Returns all of the keys (player names) and values (array [glicko, rd, volatility])

### /gxe-percentile
Parameters:
- `player`: the name of the player to get the percentile of

### /gxe-rating
Parameters:
- `player`: the name of the player to get the rating of

### /update
Parameters:
- `winner`: the name of the player who won
- `loser`: the name of the player who lost
