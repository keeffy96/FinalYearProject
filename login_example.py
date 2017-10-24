from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import random

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://keeffy96:password@ds115625.mlab.com:15625/mongologinexample'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signIn')
def signIn():
    if 'email' in session:
        email = session['email']
        return redirect(url_for('profile'))

    #elif 'user_id' in session:
     #   user_id = session['user_id']
      #  return redirect(url_for('profile'))

    else:
        return render_template('user_authentication/signIn.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_instructor = users.find_one({'email' : request.form['email']})

    if login_instructor:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_instructor['password']) == login_instructor['password'] :
            session['email'] = request.form['email']
            return redirect(url_for('signIn'))

    return 'Invalid email/password combination'

@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            user_type = 'instructor'
            school = request.form['school']
            title = request.form['title']
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            users.insert({'user_type':user_type,'school': school, 'title': title, 'name' : name, 'surname': surname, 'email' : email, 'password' : hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('signIn'))
        
        return 'That email already exists!'

    return render_template('user_authentication/register.html')

@app.route('/studentRegister', methods=['POST', 'GET'])
def studentRegister():
    if request.method == 'POST':
        users = mongo.db.users
        user_type = 'student'
        school = request.form['school']
        name = request.form['name']
        surname = request.form['surname']        
        hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
        approved = 0
        user_id = random.randint(1,1000) 
        users.insert({'user_type': user_type, 'school': school, 'name': name, 'surname': surname, 'approved':approved, 'user_id':user_id, 'password' : hashpass})
        #session['user_id'] = user_id
        #return redirect(url_for('signIn'))

    return render_template('user_authentication/studentRegister.html')

@app.route('/babras', methods=['POST', 'GET'])
def studentBabrasTest1():
    if request.method == 'POST':
        babras1 = mongo.db.babras1
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        answer3 = request.form['answer3']
        answer4 = request.form['answer4']
        answer5 = request.form['answer5']
        answer6 = request.form['answer6']
        babras1.insert({'answer1': answer1, 'answer2': answer2, 'answer3': answer3, 'answer4': answer4, 'answer5': answer5, 'answer6': answer6})

    return render_template('studentBabrasTest1.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        users = mongo.db.users
        name = users.find_one({'email':session['email']})['name']
        surname = users.find_one({'email':session['email']})['surname']

        #loops db and gets all instances where approved is 0
        student = [item for item in users.find({'approved': 0})]
        instructorSchool = users.find_one({'email':session['email']})['school']

        keys = ['name', 'surname', 'user_id']

        student = [student[0].get(key) for key in keys]

        return render_template('profile.html', name=name, surname=surname, student=student, instructorSchool=instructorSchool)

    return redirect(url_for('signIn')) 

@app.route('/editProfile', methods=['POST', 'GET'])
def editProfile():
    if request.method == 'POST':
        users = mongo.db.users
        name = request.form['name']
        surname = request.form['surname']
        users.update_one({'email':session['email']}, {'$set': {'name': name, 'surname': surname}})
        return redirect(url_for('profile'))
    
    return render_template('editProfile.html')

@app.route('/approveStudent', methods=['POST'])
def approveStudent():
    users = mongo.db.users
    studentRadio = request.form['studentRadio']
    #student = [item for item in users.find({'approved': 0})]
    result = users.update_one({'user_id': 265}, {'$set': {'approved' : 0}})

    return redirect(url_for('profile'))




if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)