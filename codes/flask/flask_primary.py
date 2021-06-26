from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# @app.route('/404')
# def test_abort():
#     abort(404)
#
#
# @app.route('/')
# def fucking_index():
#     return "fucking idiots all of you!"
#
#
# @app.route('/admin')
# def hello_admin():
#     return 'Hello Admin'
#
#
# @app.route('/guest/<guest>')
# def hello_guest(guest):
#     return 'Hello %s as Guest' % guest
#
#
# @app.route('/user/<name>')
# def hello_user(name):
#     if name == 'admin':
#         return redirect(url_for('hello_admin'))
#     else:
#         return redirect(url_for('hello_guest', guest=name))


if __name__ == '__main__':
    app.run(debug=True)
