from data import db_session
from flask import Flask
from main_api import blueprint
from OpenSSL import SSL

context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_certificate('cert.pem')


db_session.global_init('db\sender.sqlite')
app = Flask(__name__)


if __name__ == '__main__':
    app.register_blueprint(blueprint)
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context='adhoc')
