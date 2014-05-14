from flask import jsonify, make_response

from advengine.gamedata import GameData

from web import app


@app.route('/build')
def builder():
    # this command caches the file, so disabling during development
    # return send_file('templates/game-ng.html')

    return make_response(open('web/templates/builder.html').read())


@app.route('/build/gamedata')
@app.route('/build/gamedata/<game>')
def get_gamedata(game='starflight'):
    with open('games/{}.json'.format(game), 'rb') as gfile:
        gdata = GameData(gfile)

    # dicts can't be ordered in javascript, so we convert the container into a list (JS array)
    # we only want the attributes of the objects, so we convert each one into a dict (JS object)
    def json_ordered_array(objs):
        # we're now indexing by number instead of id, so add the id to each dict as an attribute
        return [dict([('id', oid)] +
                     # we can't serialize sets as json, so convert set attributes into sorted lists
                     [(attr, sorted(val) if isinstance(val, set) else val)
                      for attr, val in obj.__dict__.iteritems()])
                     for oid, obj in objs.iteritems()]

    return jsonify(nouns=json_ordered_array(gdata.nouns),
                   rooms=json_ordered_array(gdata.rooms),
                   vars=[{'id': var, 'value': value} for var, value in gdata.vars.iteritems()],
                   words=sorted(sorted(wordlist) for wordlist in gdata.lexicon.get_word_sets()),
                   messages=[{'id': mid, 'msg': msg} for mid, msg in gdata.messages.iteritems()],
                   controls=gdata.controls.values(),
                   )
