import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = 'home'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts


def is_logged():
    if "user" in session:
        # user = session["user"]
        return True


@app.route('/')
def index():
    return render_template('index.html', posts=get_posts(), is_logged=is_logged())


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post, is_logged=is_logged())


@app.route('/about')
def about():
    return render_template('about.html', is_logged=is_logged())


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if email == "milox@milox" and password == "milox":
        return redirect(url_for('index'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('signup'))


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def signin_post():
    # email = request.form.get('email')
    # name = request.form.get('name')
    # password = request.form.get('password')
    #
    # if email == "milox@milox" and password == "milox":
    #     return render_template('home.html', button_logout=True, posts=get_posts())
    # else:
    #     return "Wrong username or pass"
    if request.method == "POST":
        user = request.form["email"]
        session["user"] = user
        return redirect(url_for('index'))
    else:
        flash('Please check your login details and try again.')
        return render_template("signin.html")


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=5000)
