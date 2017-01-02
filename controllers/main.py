from flask import *
from extra import db
import hashlib
import uuid

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
    return render_template('index.html')

@main.route('/login', methods=['POST', 'GET'])
def login_route():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cur = db.cursor()
        cur.execute('SELECT * FROM User WHERE username=%s;', [username])

        if cur.rowcount != 1:
            return render_template('login.html', userNameNotExist=True)

        user_info = cur.fetchone()

        salted_password = user_info['password'].split('$', 2)
        algorithm = salted_password[0]
        salt = salted_password[1]
        hashed_password = salted_password[2]

        m = hashlib.new(algorithm)
        m.update(salt + password)
        password_to_be_verified = m.hexdigest()

        if password_to_be_verified != hashed_password:
            return render_template('login.html', passwordWrong=True)

        session['username'] = username
        return redirect(url_for('main.main_route'))
    return render_template('login.html')

@main.route('/logout', methods=['GET'])
def logout_route():
    if 'username' in session:
        session.pop('username', None)

    return redirect(url_for('main.main_route'))

@main.route('/signup', methods=['GET', 'POST'])
def signup_route():
    if 'username' in session:
        return redirect(url_for('main.main_route'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cur = db.cursor()
        cur.execute('SELECT * FROM User WHERE username=%s;', [username])

        if cur.rowcount != 0:
            return render_template('signup.html', userNameExists=True)

        algorithm = 'sha512'
        salt = uuid.uuid4().hex

        m = hashlib.new(algorithm)
        m.update(salt + password)
        password_hash = m.hexdigest()
        password_to_be_stored = '$'.join([algorithm, salt, password_hash])

        cur.execute('INSERT INTO User (username, password) VALUES(%s, %s);', (username, password_to_be_stored))

        return render_template('index.html')

    return render_template('signup.html')
