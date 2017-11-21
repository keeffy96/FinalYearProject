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
app.secret_key = 'mysecret'

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
        babras1 = mongo.db.babras1
        bebras2 = mongo.db.bebras2
        user_type = 'student'
        school = request.form['school']
        name = request.form['name']
        surname = request.form['surname']        
        hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
        approved = 0
        b1_completed = 0
        b2_completed = 0
        user_id = school + str(random.randint(1,1000)) 
        users.insert({'user_type': user_type, 'school': school, 'name': name, 'surname': surname, 'approved':approved, 'bebras1': b1_completed, 'bebras2': b2_completed, 'user_id':user_id, 'password' : hashpass})
        session['user_id'] = user_id
        q1 = "N/A"
        q2 = "N/A"
        q3 = "N/A"
        q4 = "N/A"
        q5 = "N/A"
        q6 = "N/A"
        q7 = "N/A"
        q8 = "N/A"
        q9 = "N/A"
        q10 = "N/A"
        q11 = "N/A"
        q12 = "N/A"
        q13 = "N/A"
        grade = "N/A"
        babras1.insert({'user_id': user_id, 'answer1': q1, 'answer2': q2, 'answer3': q3, 'answer4': q4, 'answer5': q5, 'answer6': q6, 'answer7': q7, 'answer8': q8, 'answer9': q9, 'answer10': q10, 'answer11': q11, 'answer12': q12, 'answer13': q13, 'finalResult' : grade})
        bebras2.insert({'user_id': user_id, 'answer1': q1, 'answer2': q2, 'answer3': q3, 'answer4': q4, 'answer5': q5, 'answer6': q6, 'answer7': q7, 'answer8': q8, 'answer9': q9, 'answer10': q10, 'answer11': q11, 'answer12': q12, 'answer13': q13, 'finalResult' : grade})
        return redirect(url_for('bebras1'))

    return render_template('user_authentication/studentRegister.html')

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
    bebras2 = mongo.db.bebras2
    userid = request.args.get("_id")
    selectedUser = users.find_one({'_id': ObjectId(userid)})['user_id']
    selectedUserName = users.find_one({'_id': ObjectId(userid)})['name']
    selectedUserSurname = users.find_one({'_id': ObjectId(userid)})['surname']
    selectedUserBebras = users.find_one({'_id': ObjectId(userid)})['bebras1']
    selectedUserBebras2 = users.find_one({'_id': ObjectId(userid)})['bebras2']
    a1 = babras1.find_one({'user_id': selectedUser})['answer1']
    a2 = babras1.find_one({'user_id': selectedUser})['answer2']
    a3 = babras1.find_one({'user_id': selectedUser})['answer3']
    a4 = babras1.find_one({'user_id': selectedUser})['answer4']
    a5 = babras1.find_one({'user_id': selectedUser})['answer5']
    a6 = babras1.find_one({'user_id': selectedUser})['answer6']
    a7 = babras1.find_one({'user_id': selectedUser})['answer7']
    a8 = babras1.find_one({'user_id': selectedUser})['answer8']
    a9 = babras1.find_one({'user_id': selectedUser})['answer9']
    a10 = babras1.find_one({'user_id': selectedUser})['answer10']
    a11 = babras1.find_one({'user_id': selectedUser})['answer11']
    a12 = babras1.find_one({'user_id': selectedUser})['answer12']
    a13 = babras1.find_one({'user_id': selectedUser})['answer13']

    ba1 = bebras2.find_one({'user_id': selectedUser})['answer1']
    ba2 = bebras2.find_one({'user_id': selectedUser})['answer2']
    ba3 = bebras2.find_one({'user_id': selectedUser})['answer3']
    ba4 = bebras2.find_one({'user_id': selectedUser})['answer4']
    ba5 = bebras2.find_one({'user_id': selectedUser})['answer5']
    ba6 = bebras2.find_one({'user_id': selectedUser})['answer6']
    ba7 = bebras2.find_one({'user_id': selectedUser})['answer7']
    ba8 = bebras2.find_one({'user_id': selectedUser})['answer8']
    ba9 = bebras2.find_one({'user_id': selectedUser})['answer9']
    ba10 = bebras2.find_one({'user_id': selectedUser})['answer10']
    ba11 = bebras2.find_one({'user_id': selectedUser})['answer11']
    ba12 = bebras2.find_one({'user_id': selectedUser})['answer12']
    ba13 = bebras2.find_one({'user_id': selectedUser})['answer13']
    result = babras1.find_one({'user_id': selectedUser})['finalResult']
    result2 = bebras2.find_one({'user_id': selectedUser})['finalResult']

    approved = "Yes"
    if selectedUserBebras is 0:
        approved = "No"
    if selectedUserBebras2 is 0:
        approved = "No"
    return render_template('profile_page/studentCheck.html', selectedUser=selectedUser, selectedUserName=selectedUserName, selectedUserSurname=selectedUserSurname, result=result, result2=result2, approved=approved, 
        a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12, a13=a13,
        ba1=ba1, ba2=ba2, ba3=ba3, ba4=ba4, ba5=ba5, ba6=ba6, ba7=ba7, ba8=ba8, ba9=ba9, ba10=ba10, ba11=ba11, ba12=ba12, ba13=ba13)

@app.route('/UsersPage')
def UsersPage():
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    school = users.find_one({'email':session['email']})['school']
    userTable = users.find({'school':school, 'user_type': 'student'})
    userTableAdmin = users.find().sort('user_type')
    userType = users.find_one({'email':session['email']})['user_type']
    uType = "instructor"
    if userType == "admin":
        uType = "admin"
    return render_template('profile_page/UsersPage.html', name=name, surname=surname, userTable=userTable, userTableAdmin=userTableAdmin, uType=uType)

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
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    school = users.find_one({'email':session['email']})['school']
    userTable = users.find({'school':school, 'user_type': 'student'})
    return render_template('testTest.html', userTable=userTable)

@app.route('/result')
def result():
    babras1 = mongo.db.babras1
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']   
    result = babras1.find_one({'user_id': user_id})['finalResult']
    return render_template('bebras_test/bebras1Results.html', user_id=user_id, result=result)

@app.route('/bebras2Result')
def bebras2Result():
    bebras2 = mongo.db.bebras2
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']   
    result = bebras2.find_one({'user_id': user_id})['finalResult']
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
        babras1.update_one({'user_id':session['user_id']}, {'$set': {'answer1': q1, 'answer2': q2, 'answer3': q3, 'answer4': q4, 'answer5': q5, 'answer6': q6, 'answer7': q7, 'answer8': q8, 'answer9': q9, 'answer10': q10, 'answer11': q11, 'answer12': q12, 'answer13': q13, 'finalResult' : grade}})
        return redirect(url_for('result'))
    return render_template('bebras_test/bebras1.html')

@app.route('/bebras2', methods=['POST','GET'])
def bebras2():
    if request.method == 'POST':
        bebras2 = mongo.db.bebras2
        users = mongo.db.users
        user_id = users.find_one({'user_id':session['user_id']})['user_id']
        users.update_one({'user_id':session['user_id']}, {'$set': {'bebras2': 1}})
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
        bebras2.update_one({'user_id':session['user_id']}, {'$set': {'answer1': q1, 'answer2': q2, 'answer3': q3, 'answer4': q4, 'answer5': q5, 'answer6': q6, 'answer7': q7, 'answer8': q8, 'answer9': q9, 'answer10': q10, 'answer11': q11, 'answer12': q12, 'answer13': q13, 'finalResult' : grade}})
        return redirect(url_for('bebras2Result'))
    return render_template('bebras_test/bebras2.html')

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
    file_list = "\n".join(['<li><a href="%s">%s</a></li>' % (url_for('serve_gridfs_file', oid=str(file._id)), file.name) for file in files])

    return (file_list, render_template('files/uploadedFiles.html', files=files, file_list=file_list))

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
    app.run(debug=True)