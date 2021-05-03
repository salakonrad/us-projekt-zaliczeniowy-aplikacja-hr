from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.exceptions import abort
from flask_mysql_connector import MySQL
from flask_paginate import Pagination, get_page_parameter
import MySQLdb.cursors
import re
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'home'

# app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_HOST'] = 'mysql'  # Added to run properly when with docker-compose
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE'] = 'hr'
mysql = MySQL(app)


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    if d1 == d2:
        return 1
    else:
        return abs((d2 - d1).days)


def mysql_query(sql):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return result


def get_post(user_id, holiday_type):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(f"SELECT * FROM hr.holidays_balance INNER JOIN users ON holidays_balance.id_users = users.id WHERE "
                f"users.id='{user_id}' AND holidays_balance.holiday_type='{holiday_type}';")
    post = cur.fetchall()
    if post is None:
        abort(404)
    return post


def get_posts(user_id):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(f"SELECT * FROM hr.holidays_balance INNER JOIN users ON holidays_balance.id_users = users.id WHERE "
                f"users.id='{user_id}';")
    posts = cur.fetchall()
    return posts


def get_salary(user_id):
    cur = mysql.new_cursor(dictionary=True)
    if check_current_user_is_admin():
        cur.execute(f"SELECT salaries.id,salaries.amount_net,salaries.amount_gross,salaries.date,users.email "
                    f"FROM hr.salaries INNER JOIN hr.users ON salaries.id_users = users.id;")
    else:
        cur.execute(f"SELECT * FROM hr.salaries WHERE id_users={user_id};")
    salary = cur.fetchall()
    return salary


# TODO: Refactor maybe mysql to not to use dictoniary here, otherwise need to extract value from dict
def get_user_id_db(email):
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(f"SELECT id FROM users WHERE email='{email}';")
    user_id = cur.fetchall()
    for dict_item in user_id:
        user_id = dict_item['id']
    return user_id


def is_logged():
    if "email" in session:
        return True


def check_current_user_is_admin():
    user_id = get_user_id_db(get_email_from_session())
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(f"SELECT * FROM hr.users WHERE id={user_id};")
    user = cur.fetchall()
    for dict_item in user:
        is_admin = dict_item['role']
        return is_admin == "admin"


def get_email_from_session():
    if "email" in session:
        return session["email"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/holidays_balances')
def holidays_balances():
    if is_logged():
        return render_template('holidays_balances.html', posts=get_posts(get_user_id_db(get_email_from_session())))
    else:
        return redirect(url_for('signin'))


@app.route('/<holiday_type>')
def post(holiday_type):
    user_id = get_user_id_db(get_email_from_session())
    post = get_post(user_id, holiday_type)
    return render_template('single_balance.html', post=post)


@app.route('/absences')
def absences():
    if is_logged():
        return render_template('absences_menu.html', check_current_user_is_admin=check_current_user_is_admin())
    else:
        return redirect(url_for('signin'))


@app.route('/absences_requests')
def absences_requests():
    if is_logged():
        user_id = get_user_id_db(get_email_from_session())
        if check_current_user_is_admin():
            cur = mysql.new_cursor(dictionary=True)
            # cur.execute(f"SELECT * FROM `holidays_requests` INNER JOIN hr.users ON holidays_requests.id_users = users.id;")
            # cur.execute(f"SELECT hr.holidays_requests.id AS holiday_request_id, hr.users.email, hr.holidays_requests.holiday_type, "
            #             f"hr.holidays_requests.date_from, hr.holidays_requests.date_to FROM `holidays_requests` INNER "
            #             f"JOIN hr.users ON holidays_requests.id_users = users.id;")
            cur.execute(f"SELECT hr.holidays_requests.id AS holiday_request_id, hr.users.id AS user_id ,"
                        f"hr.users.email, hr.holidays_requests.holiday_type, hr.holidays_requests.date_from, "
                        f"hr.holidays_requests.date_to FROM `holidays_requests` INNER JOIN hr.users ON "
                        f"holidays_requests.id_users = users.id;")
            employees_absences = cur.fetchall()
            # return str(employees_absences)
            return render_template('absences_list.html', employees_absences=employees_absences,
                                   check_current_user_is_admin=check_current_user_is_admin())
        else:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(f"SELECT * FROM hr.holidays_requests WHERE id_users={user_id};")
            absences_requests = cur.fetchall()
            return render_template('absences_list.html', absences_requests=absences_requests,
                                   check_current_user_is_admin=check_current_user_is_admin())
    else:
        return redirect(url_for('signin'))


@app.route('/accept_absence/<int:absence_id>')
def accept_absence(absence_id):
    if is_logged():
        if check_current_user_is_admin():
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(f"SELECT * FROM hr.holidays_requests WHERE id={absence_id};")
            absences_requests = cur.fetchall()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            for dict_item in absences_requests:
                id_users = dict_item['id_users']
                holiday_type = dict_item['holiday_type']
                date_from = dict_item['date_from']
                date_to = dict_item['date_to']
                amount_of_absence = days_between(str(date_from), str(date_to))
                cursor.execute(f"UPDATE hr.holidays_balance SET amount_left = amount_left - {amount_of_absence} "
                               f"WHERE id_users={id_users} AND holiday_type='{holiday_type}';")
            cursor.execute(f"DELETE FROM hr.holidays_requests WHERE holidays_requests.id={absence_id};")
            mysql.connection.commit()
            return redirect(url_for('absences_requests'))
    else:
        return redirect(url_for('signin'))


@app.route('/remove_absence/<int:absence_id>')
def remove_absence(absence_id):
    if is_logged():
        user_id = get_user_id_db(get_email_from_session())
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"DELETE FROM hr.holidays_requests WHERE holidays_requests.id={absence_id};")
        mysql.connection.commit()
        return redirect(url_for('absences_requests'))
    else:
        return redirect(url_for('signin'))


@app.route('/add_absence', methods=['GET', 'POST'])
def add_absence():
    user_id = get_user_id_db(get_email_from_session())
    if request.method == 'POST' and 'holiday_type' in request.form and 'date_from' in request.form and 'date_to' in request.form:
        holiday_type = request.form['holiday_type']
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        amount_of_absence = days_between(date_from, date_to)
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(f"SELECT id_users, holiday_type, amount_left FROM hr.holidays_balance WHERE id_users={user_id} "
                    f"and holiday_type='{holiday_type}';")
        days_left = cur.fetchall()
        for dict_item in days_left:
            amount_left = dict_item['amount_left']
            if amount_of_absence > amount_left:
                flash(f'Not enough holiday balance to create a request! Only {amount_left} days left!')
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(f"INSERT INTO hr.holidays_requests (id_users, holiday_type, date_from, date_to) VALUES "
                               f"({user_id}, '{holiday_type}', '{date_from}', '{date_to}');")
                mysql.connection.commit()
                flash('Absence request sent!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
        return render_template('absence_add.html')
    if is_logged():
        return render_template('absence_add.html')
    else:
        return redirect(url_for('signin'))


@app.route('/salaries/<email>', methods=['GET', 'POST'])
def salaries_filtered(email):
    if is_logged() and check_current_user_is_admin():
        search = False
        q = request.args.get('q')
        if q:
            search = True
        # Get page number
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # Set limit to results on one page
        limit = 4
        offset = page*limit - limit
        # SQL Queries
        sql = f"SELECT salaries.*, users.email FROM hr.salaries INNER JOIN hr.users ON salaries.id_users = users.id " \
              f"WHERE users.email='{email}'; "
        salary_count = len(mysql_query(sql))
        sql = f"SELECT salaries.*, users.email FROM hr.salaries INNER JOIN hr.users ON salaries.id_users = users.id " \
              f"WHERE users.email='{email}' LIMIT {offset}, {limit}; "
        salary = mysql_query(sql)
        sql = f"SELECT * FROM hr.users WHERE email != 'boss@salins.pl';"
        users = mysql_query(sql)
        # Prepare Pagination
        pagination = Pagination(page=page, per_page=limit, total=salary_count, search=search, record_name='salary')
        return render_template('salaries.html', users=users, salaries=salary,
                               check_current_user_is_admin=check_current_user_is_admin(), pagination=pagination, css_framework='bootstrap4')
    else:
        return redirect(url_for('signin'))


@app.route('/salaries', methods=['GET', 'POST'])
def salaries():
    user_id = get_user_id_db(get_email_from_session())
    if is_logged():
        if request.method == 'POST' and 'email' in request.form and 'amount_net' in request.form \
                and 'amount_gross' in request.form and 'transfer_date' in request.form:
            email = request.form['email']
            amount_net = request.form['amount_net']
            amount_gross = request.form['amount_gross']
            transfer_date = request.form['transfer_date']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"INSERT INTO hr.salaries (id_users, amount_net, amount_gross, date) VALUES "
                           f"({email}, {amount_net}, {amount_gross}, '{transfer_date}');")
            mysql.connection.commit()
        search = False
        q = request.args.get('q')
        if q:
            search = True
        # Get page number
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # Set limit to results on one page
        limit = 4
        offset = page*limit - limit
        # SQL Queries
        if check_current_user_is_admin():
            sql = f"SELECT salaries.*, users.email FROM hr.salaries INNER JOIN hr.users ON " \
                  f"salaries.id_users = users.id; "
            salary_count = len(mysql_query(sql))
            sql = f"SELECT salaries.*, users.email FROM hr.salaries INNER JOIN hr.users ON " \
                  f"salaries.id_users = users.id LIMIT {offset}, {limit}; "
            salary = mysql_query(sql)
            sql = f"SELECT * FROM hr.users WHERE email != 'boss@salins.pl';"
            users = mysql_query(sql)
        else:
            sql = f"SELECT * FROM hr.salaries WHERE id_users={user_id};"
            salary_count = len(mysql_query(sql))
            sql = f"SELECT * FROM hr.salaries WHERE id_users={user_id} LIMIT {offset}, {limit};"
            salary = mysql_query(sql)
        # Prepare Pagination
        pagination = Pagination(page=page, per_page=limit, total=salary_count, search=search, record_name='salary')
        return render_template('salaries.html', users=users, salaries=salary,
                               check_current_user_is_admin=check_current_user_is_admin(), pagination=pagination, css_framework='bootstrap4')
    else:
        return redirect(url_for('signin'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM hr.users WHERE email='{email}'")
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not email or not password:
            flash('Please fill out the form!')
        else:
            cursor.execute(f"INSERT INTO hr.users (email, password, role) VALUES ('{email}', '{password}', 'user')")
            # TODO : 1. Insert holiday balance for new user mscierzynski i zwykly
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(f"SELECT id from hr.users WHERE email='{email}';")
            account_data = cur.fetchall()
            for dict_item in account_data:
                user_id = dict_item['id']
                cursor.execute(f"INSERT INTO hr.holidays_balance (id_users, holiday_type, amount_left) VALUES "
                               f"({user_id}, 'urlop-macierzynski', 10), ({user_id}, 'urlop-na-zadanie', 4), "
                               f"({user_id}, 'urlop-wypoczynkowy', 26);")
            mysql.connection.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM hr.users WHERE email='{email}' AND password='{password}'")
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session["email"] = email
            # TODO: Get rid of get_email_from_session and put user's id from DB into session
            # session['id'] = account['id']
            # session['email'] = account['email']
            user_id = get_user_id_db(get_email_from_session())
            return redirect(url_for('index'))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('signin'))
    return render_template('signin.html', msg='')


@app.route('/user_panel', methods=['GET', 'POST'])
def user_panel():
    msg = ''
    if is_logged():
        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form \
                and 'retype_new_password' in request.form:
            user_id = get_user_id_db(get_email_from_session())
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            retype_new_password = request.form['retype_new_password']
            if new_password != retype_new_password:
                flash("Passwords doesn't match")
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(f"SELECT * FROM hr.users WHERE id={user_id};")
            account_data = cur.fetchall()
            for dict_item in account_data:
                old_password_db = dict_item['password']
                if old_password == old_password_db:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(f"UPDATE hr.users SET password = '{new_password}' WHERE id={user_id};")
                    mysql.connection.commit()
                    flash('Password changed.')
                    return render_template('user_panel.html')
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(f"SELECT * FROM hr.users WHERE email != 'boss@salins.pl';")
        users = cur.fetchall()
        return render_template("user_panel.html", users=users, check_current_user_is_admin=check_current_user_is_admin())
    return render_template('signin.html', msg='')


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if is_logged() and check_current_user_is_admin():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"DELETE FROM hr.users WHERE id={user_id};")
        cursor.execute(f"DELETE FROM hr.holidays_balance WHERE id_users={user_id};")
        cursor.execute(f"DELETE FROM hr.holidays_requests WHERE id_users={user_id};")
        cursor.execute(f"DELETE FROM hr.salaries WHERE id_users={user_id};")
        mysql.connection.commit()
        return redirect(url_for('user_panel'))
    else:
        return redirect(url_for('signin'))


@app.route('/logout')
def logout():
    session.pop("email", None)
    return redirect(url_for('signin'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
