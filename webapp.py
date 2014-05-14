import os

from flask import jsonify

from web import app


@app.route('/')
def index():
    return ''


@app.route('/games')
def get_games():
    return jsonify({'games': [game.rstrip('.json') for game in os.listdir('./games')
                              if game[-5:] == '.json']})


if __name__ == '__main__':
    app.debug = True
    app.config['SESSION_PATH'] = 'sessions'
    app.run()
