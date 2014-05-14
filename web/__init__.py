from flask import Flask


app = Flask(__name__)
app.secret_key = '\xf0\x9c:\xc5\xde3\xa0z^\x13\x12*\xc1\xa0J(\x8e\x9c\xb6\xb5\xa2\xc9\x19\xc3'


import builder.views
import player.views
