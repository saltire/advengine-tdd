from flask import g, jsonify, redirect, render_template, request, session, url_for

from advengine.adventure import Adventure
from web import app


GAME = 'starflight'


@app.before_request
def before_request():
    if request.path.startswith('/play'):
        if 'state' in session:
            g.adv = session['state']
        else:
            init_adventure()


def init_adventure():
    session['history'] = []
    session['queue'] = None
    #session.permanent = True
    g.adv = Adventure('./games/{}.json'.format(GAME))
    do_turn('', True)


def do_turn(command, start=False):
    if session['queue']:
        # use queued messages as output
        command = ''
        output = session['queue']
        session['queue'] = None
    else:
        # execute a command (or start the game)
        output = g.adv.start_game() if start else g.adv.do_command(command)
        session['state'] = g.adv

    if 'PAUSE' in output:
        # output messages before PAUSE, and add the rest to the queue
        i = output.index('PAUSE') + 1
        session['queue'] = output[i:]
        output = output[:i]

    session['history'].append((command, output))


@app.route('/play')
def player():
    return render_template('game.html', title='Starflight', history=session['history'])


@app.route('/play/command', methods=['post'])
def do_command():
    g.adv = session['state']
    do_turn(request.form.get('command'))
    return redirect(url_for('player'))


@app.route('/play/fetch', methods=['post'])
def do_ajax_command():
    g.adv = session['state']
    do_turn(request.form.get('command'))
    command, output = session['history'][-1]
    return jsonify({'input': command, 'output': output})


@app.route('/play/newgame', methods=['get', 'post'])
def new_game():
    session.destroy()
    init_adventure()
    return redirect(url_for('player'))


@app.route('/play/help')
def show_help():
    root = url_for('player', _external=True).rstrip('/')
    return render_template('help.html', title='Help', root=root)
