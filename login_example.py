from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://keeffy96:password@ds115625.mlab.com:15625/mongologinexample'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    if 'email' in session:
        return 'You are logged in as ' + session['email']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password'] :
            session['email'] = request.form['email']
            return redirect(url_for('index'))

    return 'Invalid email/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            users.insert({'name' : name, 'surname': surname, 'email' : email, 'password' : hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        
        return 'That email already exists!'

    return render_template('register.html')

@app.route('/studentRegister', methods=['POST', 'GET'])
def studentRegister():
    if request.method == 'POST':
        babras1 = mongo.db.babras1
        q1 = request.form['q1']
        q2 = request.form['q2']
        babras1.insert({'q1':q1, 'q2': q2})

    return render_template('studentRegister.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)