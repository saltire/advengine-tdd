from flask import Flask, jsonify, make_response, render_template

from advengine.gamedata import GameData


app = Flask(__name__)
app.secret_key = '\xf0\x9c:\xc5\xde3\xa0z^\x13\x12*\xc1\xa0J(\x8e\x9c\xb6\xb5\xa2\xc9\x19\xc3'


@app.route('/') # angular
def index():
    # this command caches the file, so disabling during development
    # return send_file('templates/game-ng.html')

    return make_response(open('web/templates/game-ng.html').read())


@app.route('/partials/<template>')
def get_partial(template):
    return make_response(open('web/templates/partials/{}.html'.format(template)).read())


@app.route('/gamedata')
@app.route('/gamedata/<game>')
def get_gamedata(game='starflight'):
    with open('games/{}.json'.format(game), 'rb') as gfile:
        gdata = GameData(gfile)

    # dicts can't be ordered in javascript, so we convert the container into a list (JS array)
    # we only want the attributes of the objects, so we convert each one into a dict (JS object)
    def convert_to_dicts(objs):
        # we're now indexing by number instead of id, so add the id to each dict as an attribute
        return [dict([('_id', oid)] +
                     # we can't serialize sets as json, so convert set attributes into sorted lists
                     [(attr, sorted(val) if isinstance(val, set) else val)
                      for attr, val in obj.__dict__.iteritems()])
                     for oid, obj in objs.iteritems()]

    return jsonify(nouns=convert_to_dicts(gdata.nouns),
                   rooms=convert_to_dicts(gdata.rooms),
                   vars=gdata.vars,
                   words=sorted(sorted(wordlist) for wordlist in gdata.lexicon.get_word_sets()),
                   sort_keys=False)


@app.route('/flask')
def index_flask():
    with open('games/starflight.json', 'rb') as gamefile:
        game = GameData(gamefile)

    return render_template('game.html',
                           rooms=game.rooms.items(),
                           nouns=game.nouns.items(),
                           vars=game.vars,
                           words=game.lexicon.get_word_sets(),
                           )
