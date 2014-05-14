from web import app


if __name__ == '__main__':
    app.debug = True
    app.config['SESSION_PATH'] = 'sessions'
    app.run()
