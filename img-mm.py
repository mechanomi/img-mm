import sys

from pprint import pformat

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return pformat(sys.argv)

if __name__ == '__main__':
    app.run()
