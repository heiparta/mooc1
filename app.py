import os
import sqlite3

from flask import Flask, render_template, g, abort, request, redirect, url_for, make_response
app = Flask("mooc")
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sql.db'),
    SECRET_KEY='dev',
))


def db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(app.config['DATABASE'], isolation_level=None)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    cur = db().execute('select id, name from users where name="{}" AND password="{}" LIMIT 1'.format(username, password))
    user = cur.fetchone()
    if not user:
        return redirect(url_for('login'))
    redirect_target = request.args.get('next', url_for('index'))
    res = make_response(redirect(redirect_target))
    res.set_cookie('username', username)
    return res


@app.route("/logout")
def logout():
    res = make_response(redirect(url_for('login')))
    res.set_cookie('username', '', expires=0)
    return res


@app.route("/")
def index():
    """Validate cookie and redirect to user entries"""
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    cur = db().execute('select id, name from users where name="{}" LIMIT 1'.format(username))
    user = cur.fetchone()
    if not user:
        return redirect(url_for('login'))
    return redirect(url_for('entries'))


@app.route("/entries", methods=["GET"])
def entries():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    cur = db().execute('select id, name from users where name="{}" LIMIT 1'.format(username))
    user = cur.fetchone()
    if not user:
        return redirect(url_for('login'))
    params = dict(username=user["name"])
    cur.execute('select id, title from entries where user={} order by id desc'.format(user['id']))
    params['entries'] = cur.fetchall()
    return render_template('entries.html', **params)


@app.route('/entries', methods=['POST'])
def add_entry():
    app.logger.info("WOOT {} {}".format(request.cookies, request.form))
    if not ('title' in request.form and 'content' in request.form):
        abort(400)
    username = request.cookies.get('username')
    if not username:
        app.logger.warning("No user1", username)
        return redirect(url_for('login'))
    cur = db().execute('select id, name from users where name="{}" LIMIT 1'.format(username))
    user = cur.fetchone()
    if not user:
        print("No user", username)
        return redirect(url_for('login'))
    params = dict(
        user=user['id'],
        title=request.form.get('title'),
        content=request.form.get('content'),
    )
    cur.execute('insert into entries (user, title, content) VALUES(:user, :title, :content)', params)
    return redirect(url_for('entries'))


@app.route('/entries/<entry_id>', methods=['GET'])
def show_entry(entry_id):
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    query = 'select id, title, content from entries where id="{}" LIMIT 1'.format(entry_id)
    app.logger.debug("FULL query: %s", query)
    # Circumvent the sqlite SQL injection protection by splitting the query by
    # semicolon and executing each part as separate query
    queries = query.split(';')
    entry = None
    for query in queries:
        app.logger.debug("query: %s", query)
        cur = db().execute(query)
        result = cur.fetchone()
        if result:
            entry = result
    app.logger.debug("res: %s", entry)
    if not entry:
        return redirect(url_for('entries'))
    return render_template('entry.html', entry=entry)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
