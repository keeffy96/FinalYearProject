from flask import Flask, render_template, url_for, request, session, redirect, send_file, make_response, abort, Markup
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from gridfs.errors import NoFile
from werkzeug import secure_filename
import bcrypt
import gridfs
import random

app = Flask(__name__)

#MongoClient.connect('mongodb://keeffy96:password@ds115625.mlab.com:15625')
#db = client.mongologinexample

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pptx'])
db = MongoClient().connect_to_mongo
fs = gridfs.GridFS(db)
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

    #Render template to be changed, just testing login1 attribute
    return render_template('testTest.html', login1=login1)

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
        b1_completed = 0
        user_id = school + str(random.randint(1,1000)) 
        users.insert({'user_type': user_type, 'school': school, 'name': name, 'surname': surname, 'approved':approved, 'bebras1': b1_completed, 'user_id':user_id, 'password' : hashpass})
        session['user_id'] = user_id
        return redirect(url_for('bebras1'))

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
    babras1 = mongo.db.babras1
    if 'email' in session:
        name = users.find_one({'email':session['email']})['name']
        surname = users.find_one({'email':session['email']})['surname']
        instructorSchool = users.find_one({'email':session['email']})['school']
        userType = users.find_one({'email':session['email']})['user_type']
        uType = "instructor"
        if userType == "admin":
            uType = "admin"
        return render_template('profile_page/profile.html', name=name, surname=surname, instructorSchool=instructorSchool, userType=userType, uType=uType)

    elif 'user_id' in session:
        name = users.find_one({'user_id':session['user_id']})['name']
        surname = users.find_one({'user_id':session['user_id']})['surname']
        userid = users.find_one({'user_id':session['user_id']})['user_id']
        bebrasCompleted = users.find_one({'user_id':session['user_id']})['bebras1']
        userApproved = users.find_one({'user_id':session['user_id']})['approved']
        b1_todo = 1
        approved = 1
        if userApproved is 0:
            approved = 0
        if bebrasCompleted is 0:
            b1_todo = 0
        return render_template('profile_page/profile.html', name=name, surname=surname, userid=userid, b1_todo=b1_todo, approved=approved)

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

@app.route('/profilePage', methods=['POST', 'GET'])
def profilePage():
    babras1 = mongo.db.babras1
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']    
    result = babras1.find_one({'user_id': user_id})['finalResult']
    return render_template('profile_page/profilePage.html', result=result)

@app.route('/studentProgress')
def studentProgress():
    users = mongo.db.users
    babras1 = mongo.db.babras1
    userid = request.args.get("_id")
    selectedUser = users.find_one({'_id': ObjectId(userid)})['user_id']
    selectedUserName = users.find_one({'_id': ObjectId(userid)})['name']
    selectedUserSurname = users.find_one({'_id': ObjectId(userid)})['surname']
    selectedUserBebras = users.find_one({'_id': ObjectId(userid)})['bebras1']
    result = babras1.find_one({'user_id': selectedUser})['finalResult']
    approved = "Yes"
    if selectedUserBebras is 0:
        approved = "No"
    return render_template('profile_page/studentCheck.html', selectedUser=selectedUser, selectedUserName=selectedUserName, selectedUserSurname=selectedUserSurname, result=result, approved=approved)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'), 404

@app.route('/test')
def chart():
    babras1 = mongo.db.babras1
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']    
    result = babras1.find_one({'user_id': user_id})['finalResult']
    return render_template('testTest.html', result=result)

@app.route('/result')
def result():
    babras1 = mongo.db.babras1
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']    
    result = babras1.find_one({'user_id': user_id})['finalResult']
    return render_template('bebras_test/bebras1Results.html', user_id=user_id, result=result)

@app.route('/bebras1', methods=['POST','GET'])
def bebras1():
    if request.method == 'POST':
        babras1 = mongo.db.babras1
        users = mongo.db.users
        user_id = users.find_one({'user_id':session['user_id']})['user_id']
        users.update_one({'user_id':session['user_id']}, {'$set': {'bebras1': 1}})
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        q6 = request.form['q6']
        q7 = request.form['q7']
        q8 = request.form['q8']
        q9 = request.form['q9']
        q10 = request.form['q10']
        q11 = request.form['q11']
        q12 = request.form['q12']
        q13 = request.form['q13']
        grade = request.form['grade']
        babras1.insert({'user_id': user_id, 'answer1': q1, 'answer2': q2, 'answer3': q3, 'answer4': q4, 'answer5': q5, 'answer6': q6, 'answer7': q7, 'answer8': q8, 'answer9': q9, 'answer10': q10, 'answer11': q11, 'answer12': q12, 'answer13': q13, 'finalResult' : grade})
        return redirect(url_for('result'))
    return render_template('bebras_test/bebras1.html')

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadFiles', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            oid = fs.put(file, content_type=file.content_type, filename=filename)
            return render_template('files/uploadFile.html')            
    return render_template('files/uploadFile.html')

@app.route('/files')
def list_gridfs_files():
    files = [fs.get_last_version(file) for file in fs.list()]
    userTable = fs.list()
    #userTable = db.fs.files.find_one({'filename': 'BeaverLunchAnswer2.jpg'})
    #userTable = db.fs.files.get(userTable)
    #userTable = fs.get(filename = 'BeaverLunchAnswer2.jpg ')
    file_list = "\n".join(['<li><a href="%s">%s</a></li>' % (url_for('serve_gridfs_file', oid=str(file._id)), file.name) for file in files])

    return (file_list, render_template('files/uploadedFiles.html', files=files, file_list=file_list, userTable=userTable))

@app.route('/files/<oid>')
def serve_gridfs_file(oid):
    try:
        file = fs.get(ObjectId(oid))
        response = make_response(file.read())
        response.mimetype = file.content_type
        return response
    except NoFile:
        abort(404)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)