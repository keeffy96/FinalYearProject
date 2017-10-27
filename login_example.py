from flask import Flask, render_template, url_for, request, session, redirect, send_file
from flask_pymongo import PyMongo
from bson import ObjectId
import bcrypt
import random

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://keeffy96:password@ds115625.mlab.com:15625/mongologinexample'

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home_page/home.html')

@app.route('/signIn')
def signIn():
    if 'email' in session:
        email = session['email']
        return redirect(url_for('profile'))
    
    elif 'user_id' in session:
        user_id = session['user_id']
        return redirect(url_for('profile'))

    else:
        return render_template('user_authentication/signIn.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login = users.find_one({'email' : request.form['email']})
    login1 = users.find_one({'user_id' : request.form['email']})

    if login:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login['password']) == login['password'] :
            session['email'] = request.form['email']
            return redirect(url_for('signIn'))

    if login1:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login1['password']) == login1['password'] :
            session['user_id'] = request.form['email']
            return redirect(url_for('signIn'))

    return 'Invalid email/password combination'

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    return render_template('home_page/home.html')

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
        session['user_id'] = user_id
        return redirect(url_for('signIn'))

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
    users = mongo.db.users
    if 'email' in session:
        name = users.find_one({'email':session['email']})['name']
        surname = users.find_one({'email':session['email']})['surname']
        student = [item for item in users.find({'approved': 0})]
        instructorSchool = users.find_one({'email':session['email']})['school']
        keys = ['name', 'surname', 'user_id']
        student = [student[1].get(key) for key in keys]        
        return render_template('profile_page/profile.html', name=name, surname=surname, student=student, instructorSchool=instructorSchool)

    elif 'user_id' in session:
        name = users.find_one({'user_id':session['user_id']})['name']
        surname = users.find_one({'user_id':session['user_id']})['surname']
        return render_template('profile_page/profile.html', name=name, surname=surname)

    else:
        return redirect(url_for('signIn')) 

@app.route('/editProfile', methods=['POST', 'GET'])
def editProfile():
    if request.method == 'POST':
        users = mongo.db.users
        name = request.form['name']
        surname = request.form['surname']
        users.update_one({'email':session['email']}, {'$set': {'name': name, 'surname': surname}})
        return redirect(url_for('profile'))
    
    return render_template('profile_page/editProfile.html')

@app.route('/approveStudent', methods=['POST'])
def approveStudent():
    users = mongo.db.users
    studentRadio = request.form['studentRadio']
    #student = [item for item in users.find({'approved': 0})]

    #student = [item for item in users.find({'approved': 0})]
    result = users.update_one({'school': 469}, {'$set': {'approved' : 0}})

    return redirect(url_for('profile'))


@app.route('/file-downloads/')
def file_downloads():
    return render_template('testTest.html')
    
@app.route('/return-filez/')
def return_file():
    return send_file('static/img/PleaseWork.pptx', attachment_filename='powerpoint.pptx')

@app.route('/UsersPage')
def UsersPage():
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    school = users.find_one({'email':session['email']})['school']
    userTable = users.find({'school':school, 'user_type': 'student'})
    return render_template('profile_page/UsersPage.html', name=name, surname=surname, userTable=userTable)

@app.route('/update')
def update():
    users = mongo.db.users
    userid = request.args.get("_id")
    users.update_one({'_id': ObjectId(userid)}, {'$set': {'approved': 1}})
    return redirect(url_for('UsersPage'))

@app.route('/toBeApproved')
def toBeApproved():
    users = mongo.db.users
    school = users.find_one({'email':session['email']})['school']
    userTable = users.find({'school':school, 'approved': 0})
    return render_template('profile_page/UsersPage.html', userTable=userTable)


@app.route('/testingPage/')
def testingPage():
    return render_template('TestingPageCSS.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)