from data import db_session
from flask import Flask
from main_api import blueprint

db_session.global_init('db\sender.sqlite')
app = Flask(__name__)


if __name__ == '__main__':
    app.register_blueprint(blueprint)
    app.run(host='0.0.0.0', port=8080, debug=True)
