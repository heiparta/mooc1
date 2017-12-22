import os
import sqlite3

from flask import Flask, render_template, g, abort, session, request
app = Flask("mooc")
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sql.db'),
    SECRET_KEY='dev',
))


def db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
def index():
    params = dict()
    cur = db().execute('select title from entries where user={} order by id desc'.format(request.args.get('user', 1)))
    params['entries'] = cur.fetchall()
    return render_template('index.html', **params)


@app.route('/entries', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
