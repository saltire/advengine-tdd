import os

from flask import g, jsonify, redirect, render_template, request, session, url_for

from simplekv.fs import FilesystemStore
from flask.ext.kvsession import KVSessionExtension

from advengine.adventure import Adventure
from web import app


gamepath = './games/starflight.json'


@app.before_first_request
def init_session():
    app.logger.debug('init session')
    store = FilesystemStore(app.config['SESSION_PATH'])
    KVSessionExtension(store, app)


@app.before_request
def before_request():
    if 'state' in session:
        g.adv = Adventure(gamepath, session['state'])
    else:
        init_adventure()


def init_adventure():
    session['history'] = []
    session['queue'] = None
    session['state'] = None
    #session.permanent = True
    g.adv = Adventure(gamepath)
    do_turn('')


def do_turn(command):
    if session['queue']:
        command = ''
        output = session['queue']
        session['queue'] = None
    else:
        output = g.adv.do_command(command)
        session['state'] = g.adv.export_state()

    if 'PAUSE' in output:
        i = output.index('PAUSE') + 1
        session['queue'] = (output[i:])
        output = output[:i]

    session['history'].append((command, output))


@app.route('/')
def index():
    return render_template('game.html', title='Starflight',
                           history=session['history'])


@app.route('/command', methods=['post'])
def do_command():
    g.adv = Adventure(gamepath, session['state'])
    do_turn(request.form.get('command'))
    return redirect(url_for('index'))


@app.route('/fetch', methods=['post'])
def do_ajax_command():
    g.adv = Adventure(gamepath, session['state'])
    do_turn(request.form.get('command'))
    command, output = session['history'][-1]
    return jsonify({'input': command, 'output': output})


@app.route('/newgame', methods=['get', 'post'])
def new_game():
    session.destroy()
    init_adventure()
    return redirect(url_for('index'))


@app.route('/help')
def show_help():
    root = url_for('index', _external=True).rstrip('/')
    return render_template('help.html', title='Help', root=root)
