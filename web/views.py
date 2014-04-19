from flask import Flask, render_template

from advengine.gamedata import GameData


app = Flask(__name__)
app.secret_key = '\xf0\x9c:\xc5\xde3\xa0z^\x13\x12*\xc1\xa0J(\x8e\x9c\xb6\xb5\xa2\xc9\x19\xc3'


@app.route('/')
def index():
    with open('games/starflight.json', 'rb') as gamefile:
        game = GameData(gamefile)

    return render_template('game.html',
                           rooms=game.rooms.items(),
                           nouns=game.nouns.items(),
                           vars=game.vars,
                           words=game.lexicon.get_word_sets(),
                           )
