"""
Flask API.
"""
import re
import os
import sys
import logging
import pickle
import threading
import time

import yaml
import pymongo
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from prometheus_flask_exporter import PrometheusMetrics


# Make connection to MongoDB with photo data
with open("api_config.yaml") as yaml_file:
    config_dict = yaml.load(yaml_file)["config_dictionary"]

for i in os.listdir('static/images'):
    if 'png' in i:
        os.system(f"rm static/images/{i}")

db = pymongo.MongoClient(
    'mongo1:27017',
    username=config_dict['mongo_user'],
    password=config_dict['mongo_password'],
    authSource=config_dict['mongo_database'],
    authMechanism='SCRAM-SHA-256')[config_dict['mongo_database']]
try:
    db.list_collections()
except Exception as exception:
    logging.error("Problem with connection to MongoDB\n%s", exception.args)
    sys.exit(2)

collection_photos = db[config_dict['collection_photos']]
collection_labels = db[config_dict['collection_labels']]

user_history = {}

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'mysql-db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'users'

# Initialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/pythonlogin/', methods=['GET', 'POST'])
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    """
    http://localhost:5000/pythonlogin/
    This will be the login page, we need to use both GET and POST requests.

    :return: redirect to home page for successfully log-in user
             redirect to login page for unsuccessfully log-in user with proper message
    """
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        # pylint: disable=no-else-return
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('index.html', msg=msg)
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/api/logout')
@app.route('/pythonlogin/logout')
def logout():
    """
    http://localhost:5000/python/logout
    This will be the logout page.

    :return: Redirect to login page.
    """
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(_):
    """
    Page not found.
    :param _: caught exception
    :return: redirect to 404 page
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(_):
    """
    Internal server error.
    :param _: caught exception
    :return: redirect to 503 page
    """
    return render_template('500.html'), 500


@app.route('/api/register', methods=['GET', 'POST'])
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    """
    http://localhost:5000/pythinlogin/register
    This will be the registration page, we need to use both GET and POST.

    :return: redirect to register page with proper message
    """
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form \
            and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/api/home')
@app.route('/pythonlogin/home')
def home():
    """
    http://localhost:5000/pythinlogin/home
    This will be the home page, only accessible for loggedin users.

    :return: redirect to home page for loggedin user
             redirect to login page for non-loggedin user
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/api/profile')
@app.route('/pythonlogin/profile')
def profile():
    """
    http://localhost:5000/pythinlogin/profile
    This will be the profile page, only accessible for loggedin users.

    :return: redirect to profile page
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        settings = db["app_settings"]
        links = [*settings.find()]

        # Getting user's urls
        # urls = []
        # for i in links:
        #     if i["user"] == account['username']:
        #         urls.append(i["url"])

        # Getting all urls
        urls = [i["url"] for i in links]

        # Show the profile page with account info
        return render_template('profile.html', account=account, urls = urls)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/api/find_by_tag/<index>')
@app.route('/pythonlogin/find_by_tag/<index>')
def browser(index):
    """
    http://localhost:5000/pythonlogin/find_by_tag/0

    :param index: number of image that should be displayed
    :return: redirect to page with proper image
    """
    # We need user
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    user = account['username']
    index = int(index)
    # case no pictures found
    if not user_history[user]:
        return redirect(url_for('home'))
    photo_date = user_history[user][index]
    # Render a browser with image
    return render_template("browser.html", data=photo_date[0], all_info=photo_date[1],
                           next_pic=f"{(index + 1) % len(user_history[user])}",
                           previous_pic=f"{(index - 1) % len(user_history[user])}")


def get_info(founded, labels):
    """
    Function for choose only matching elements form photo.

    :param founded:
    :param labels:
    :return:
    """
    # Caught - all object in the photo
    caught_objects = founded["labels"]
    info = []
    for caught_object in caught_objects:
        # i[:4] tagi zaczynaja sie od 5 elementu
        if set(labels) & set(caught_object[4:]):
            info.append(caught_object)
    # Returns a list of elements in the photo, that link to the tag
    return info


def get_photos(labels, found, user):
    """
    Function for save matching images.

    :param labels:
    :param found:
    :param user:
    :return: None
    """
    for img in found:
        # Saving photo form database
        photo = pickle.loads(collection_photos.find_one({"id": img['id']})['photo'])
        photo = Image.fromarray(photo)
        blue, green, red = photo.split()
        photo = Image.merge("RGB", (red, green, blue))
        photo.save(f'static/images/{img["id"]}.png')
        # We need info about all matching elements in the photo
        info = get_info(img, labels)
        user_history[user].append([img["id"], info])


@app.route('/goto', methods=['POST', 'GET'])
def goto():
    """
    http://localhost/goto
    Initialize the acquisition of photos and redirect to /pythonlogin/find_by_tag/0

    :return: redirect to page with found photo.
    """
    # We need user
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    user = account['username']

    user_history[user] = []
    text = request.form['index']
    # Colects all matching information from database
    labels = [x.strip().lower() for x in text.split(',')]
    big_labels = [x[0].upper() + x[1:] for x in labels]
    labels = list(set(labels + big_labels))
    found = [*collection_labels.find({'labels': {"$elemMatch": {"$elemMatch": {"$in": labels}}}})]
    # Starts the thread which supports saving images
    try:
        img_download_thread = threading.Thread(target=get_photos, args=(labels, found, user))
        img_download_thread.start()
    except Exception:
        logging.error("Unsuccessful initialization of downloading photos")
    time.sleep(2)
    # Redirect to first matching element
    return redirect('/pythonlogin/find_by_tag/0')


@app.route('/add_stream', methods=['POST', 'GET'])
def add_stream():
    """

    :return:
    """
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    user = account['username']

    text = request.form['index'].strip()
    print(db["app_settings"].find({"url": text}))
    if [*db["app_settings"].find({"url": text})]:
        print('not added')
        return redirect('/pythonlogin/profile')
    record = {"url": text, "user": user, "inserted": int(time.time())}
    try:
        db["app_settings"].insert_one(record)
        logging.info("%s has added url %s to db", user, text)
    except Exception:
        logging.error("Unsuccessful insertion of %s for user %s", text, user)
    return redirect('/pythonlogin/profile')


if __name__ == '__main__':
    with open('/etc/hostname', 'r') as f:
        hostname = f.read().strip()
    app.run(host=hostname, port=80)
