from flask import Flask

from simplekv.fs import FilesystemStore
from flask.ext.kvsession import KVSessionExtension


app = Flask(__name__)
app.secret_key = '\xf0\x9c:\xc5\xde3\xa0z^\x13\x12*\xc1\xa0J(\x8e\x9c\xb6\xb5\xa2\xc9\x19\xc3'


@app.before_first_request
def init_session():
    store = FilesystemStore(app.config['SESSION_PATH'])
    KVSessionExtension(store, app)


import builder
import player
