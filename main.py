from flask import Flask, render_template, url_for, request, session, redirect, send_file, make_response, abort, Markup
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from gridfs.errors import NoFile
from werkzeug import secure_filename
import bcrypt
import gridfs
import random
import datetime

app = Flask(__name__)
app.secret_key = 'mysecret'

#Alowed file types for when uploading files
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pptx', 'docx'])

#MongoDB URI connection 
app.config['MONGO_URI'] = 'mongodb://keeffy96:password@ds115625.mlab.com:15625/mongologinexample'
mongo = PyMongo(app)

#Public pages

#Home Page
@app.route('/')
def home():
    return render_template('home_page/home.html')

#About Page
@app.route('/about')
def about():
    return render_template('home_page/about.html')

################################################################

#Sign Up pages

#Student Register
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
        return redirect(url_for('personalQuestions'))
    return render_template('user_authentication/studentRegister.html')

#Teacher Register
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

###########################################################

#Login Page

#Redirected to signIn and storing the users email or userID in session
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

#Checking the database for the entered user and encrypting their password
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    #login checking if the user is a teacher - due to email
    login = users.find_one({'email' : request.form['email']})
    #login1 checking if the user is a student - due to userID
    login1 = users.find_one({'user_id' : request.form['email']})
    incorrectDetails = "Invalid login, please try again"

    if login:
        #Retriveing the entered password and encrypting it
        #If statement checking if encrypted password is equal to password
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login['password']) == login['password'] :
            session['email'] = request.form['email']
            return redirect(url_for('signIn'))

    if login1:
        #Retriveing the entered password and encrypting it
        #If statement checking if encrypted password is equal to password
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login1['password']) == login1['password'] :
            session['user_id'] = request.form['email']
            return redirect(url_for('signIn'))
    return render_template('user_authentication/signIn.html', incorrectDetails=incorrectDetails)

#Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    return render_template('home_page/home.html')

################################################################

#User pages

#Users Home Page
@app.route('/profile', methods=['POST', 'GET'])
def profile():
    #Creating variables for database collections
    users = mongo.db.users
    babras1 = mongo.db.babras1
    postDB = mongo.db.post
    fs = gridfs.GridFS(mongo.db)
    testDB = mongo.db.test

    if 'email' in session:
        teacher = users.find_one({'email':session['email']})
        name = teacher['name']
        surname = teacher['surname']
        userid = teacher['email']
        school = teacher['school']
        userType = teacher['user_type']
        uType = "instructor"
        if userType == "admin":
            uType = "admin"
        
        userTable = postDB.find().sort("uploadedTime",-1).limit(5)

        #file search
        if request.method == 'POST':
            allFiles = fs.list()
            search = request.form['search'].title()
            inDB = list((s for s in allFiles if search in s))
            files = [fs.get_last_version(file) for file in inDB]
            length = len(files)
            return render_template('profile_page/homePage.html', length=length, files=files, name=name, surname=surname, userid=userid, school=school, userType=userType, uType=uType, userTable=userTable)
        return render_template('profile_page/homePage.html', name=name, surname=surname, userid=userid, school=school, userType=userType, uType=uType, userTable=userTable)
    
    elif 'user_id' in session:
        student = users.find_one({'user_id':session['user_id']})
        name = student['name']
        surname = student['surname']
        userid = student['user_id']
        school = student['school']
        bebrasCompleted = student['bebras1']
        bebrasCompleted2 = student['bebras2']
        userApproved = student['approved']
        b1_todo = 1
        b2_todo = 1
        approved = 1
        if userApproved is 0:
            approved = 0
        if bebrasCompleted is 0:
            b1_todo = 0
        if bebrasCompleted2 is 0:
            b2_todo = 0

        #file search
        if request.method == 'POST':
            allFiles = fs.list()
            search = request.form['search'].title()
            inDB = list((s for s in allFiles if search in s))
            files = [fs.get_last_version(file) for file in inDB]
            return render_template('profile_page/homePage.html', files=files, name=name, surname=surname, userid=userid, school=school, b1_todo=b1_todo, b2_todo=b2_todo, approved=approved)
        return render_template('profile_page/homePage.html', name=name, surname=surname, userid=userid, school=school, b1_todo=b1_todo, b2_todo=b2_todo, approved=approved)

    else:
        return redirect(url_for('signIn')) 

#Edit Profile for teachers to change various details
@app.route('/editProfile', methods=['POST', 'GET'])
def editProfile():
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        users.update_one({'email':session['email']}, {'$set': {'name': name, 'surname': surname}})
        return redirect(url_for('profile'))
    
    return render_template('profile_page/editProfile.html', name=name, surname=surname)

#Approve student page - displays a list of all student in class
@app.route('/UsersPage')
def UsersPage():
    users = mongo.db.users
    teacher = users.find_one({'email':session['email']})
    name = teacher['name']
    surname = teacher['surname']
    school = teacher['school']
    userTable = users.find({'school':school, 'user_type': 'student'})
    userTableAdmin = users.find().sort('user_type')
    userType = teacher['user_type']
    uType = "instructor"
    if userType == "admin":
        uType = "admin"
    return render_template('profile_page/UsersPage.html', name=name, surname=surname, userTable=userTable, userTableAdmin=userTableAdmin, uType=uType)

#Student page - teacher can select individual students and find out progression
@app.route('/studentProgress')
def studentProgress():
    users = mongo.db.users
    babras1 = mongo.db.babras1
    bebras2 = mongo.db.bebras2
    teacher = users.find_one({'email':session['email']})
    name = teacher['name']
    surname = teacher['surname']
    userid = request.args.get("_id")
    selectedStudent = users.find_one({'_id': ObjectId(userid)})
    selectedUser = selectedStudent['user_id']
    selectedUserName = selectedStudent['name']
    selectedUserSurname = selectedStudent['surname']
    selectedUserBebras = selectedStudent['bebras1']
    selectedUserBebras2 = selectedStudent['bebras2']
    bebras1 = babras1.find_one({'user_id': selectedUser})
    bebras2 = bebras2.find_one({'user_id': selectedUser})

    #Collecting all answers for bebras1 given by selecteded student
    a1 = bebras1['answer1']
    a2 = bebras1['answer2']
    a3 = bebras1['answer3']
    a4 = bebras1['answer4']
    a5 = bebras1['answer5']
    a6 = bebras1['answer6']
    a7 = bebras1['answer7']
    a8 = bebras1['answer8']
    a9 = bebras1['answer9']
    a10 = bebras1['answer10']
    a11 = bebras1['answer11']
    a12 = bebras1['answer12']
    a13 = bebras1['answer13']

    #Collecting all answers for bebras2 given by selecteded student
    ba1 = bebras2['answer1']
    ba2 = bebras2['answer2']
    ba3 = bebras2['answer3']
    ba4 = bebras2['answer4']
    ba5 = bebras2['answer5']
    ba6 = bebras2['answer6']
    ba7 = bebras2['answer7']
    ba8 = bebras2['answer8']
    ba9 = bebras2['answer9']
    ba10 = bebras2['answer10']
    ba11 = bebras2['answer11']
    ba12 = bebras2['answer12']
    ba13 = bebras2['answer13']
    result = bebras1['finalResult']
    result2 =bebras2['finalResult']

    completedTest1 = ""
    completedTest2 = ""

    if selectedUserBebras is 0:
        completedTest1 = "No"
    else:
        completedTest1 = "Yes"

    if selectedUserBebras2 is 0:
        completedTest2 = "No"
    else: 
        completedTest2 = "Yes"

    return render_template('profile_page/studentCheck.html', selectedUser=selectedUser, selectedUserName=selectedUserName, selectedUserSurname=selectedUserSurname, result=result, result2=result2, completedTest2=completedTest2, 
        a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12, a13=a13,
        ba1=ba1, ba2=ba2, ba3=ba3, ba4=ba4, ba5=ba5, ba6=ba6, ba7=ba7, ba8=ba8, ba9=ba9, ba10=ba10, ba11=ba11, ba12=ba12, ba13=ba13, name=name, surname=surname,
        completedTest1=completedTest1)

#Approve Student
@app.route('/toBeApproved')
def toBeApproved():
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    school = users.find_one({'email':session['email']})['school']
    userTable = users.find({'school':school, 'approved': 0})
    return render_template('profile_page/UsersPage.html', userTable=userTable, name=name, surname=surname)

#Update function - retrieves selected student and approves them to the class
@app.route('/update')
def update():
    users = mongo.db.users
    userid = request.args.get("_id")
    users.update_one({'_id': ObjectId(userid)}, {'$set': {'approved': 1}})
    return redirect(url_for('UsersPage'))

#Remove function - retrieves selected student and removes them from the class
@app.route('/remove')
def remove():
    users = mongo.db.users
    userid = request.args.get("_id")
    users.remove({'_id': ObjectId(userid)})
    return redirect(url_for('UsersPage'))

#Discussion forum
@app.route('/posts', methods=['POST', 'GET'])
def posts():
    postDB = mongo.db.post
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    userTable = postDB.find().sort("uploadedTime",-1)

    if request.method == 'POST':
        email = session['email']
        description = request.form['post']
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M")
        postDB.insert({'userID': email,'description': description, 'uploadedTime': time})
        userTable = postDB.find().sort("uploadedTime",-1)
        return render_template('profile_page/post.html', name=name, surname=surname, userTable=userTable)
    return render_template('profile_page/post.html', userTable=userTable, name=name, surname=surname)

#Search function which allows for users to search names of files 
@app.route('/search', methods=['POST', 'GET'])
def search():
    fs = gridfs.GridFS(mongo.db)
    testDB = mongo.db.test    

    if request.method == 'POST':
        allFiles = fs.list()
        search = request.form['search'].title()
        inDB = list((s for s in allFiles if search in s))
        files = [fs.get_last_version(file) for file in inDB]
        return render_template('search.html', inDB=inDB, files=files)

    return render_template('search.html')

############################################################

#Tests and surveys

#Collecting all answers entered by the student for bebras1 test 
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

#Collecting all answers entered by the student for bebras2 test 
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

#Retrieving result for bebras 1
@app.route('/result')
def result():
    babras1 = mongo.db.babras1
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']   
    result = babras1.find_one({'user_id': user_id})['finalResult']
    return render_template('bebras_test/bebrasResults.html', user_id=user_id, result=result)

#Retrieving result for bebras 2
@app.route('/bebras2Result')
def bebras2Result():
    bebras2 = mongo.db.bebras2
    users = mongo.db.users
    user_id = users.find_one({'user_id':session['user_id']})['user_id']   
    result = bebras2.find_one({'user_id': user_id})['finalResult']
    return render_template('bebras_test/bebrasResults.html', user_id=user_id, result=result)

#Student CSQuestions survey - retrieves them from form
@app.route('/csQuestions', methods=['POST','GET'])
def csQuestions():
    if request.method == 'POST':
        csQuestions = mongo.db.csQuestions
        users = mongo.db.users
        user_id = users.find_one({'user_id':session['user_id']})['user_id']
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
        q14 = request.form['q14']
        q15 = request.form['q15']
        q16 = request.form['q16']
        q17 = request.form['q17']
        csQuestions.insert({'user_id':session['user_id'],'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4, 'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9, 'q10':q10, 'q11':q11, 'q12':q12, 'q13':q13, 'q14':q14, 'q15':q15, 'q16':q16, 'q17':q17})
        return redirect(url_for('bebras1'))
    return render_template('survey/csQuestions.html')

#Student Personal Questions survey - retrieves them from form
@app.route('/personalQuestions', methods=['POST','GET'])
def personalQuestions():
    if request.method == 'POST':
        personalQuestions = mongo.db.personalQuestions
        users = mongo.db.users
        user_id = users.find_one({'user_id':session['user_id']})['user_id']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        q6 = request.form['q6']
        q7 = request.form['q7']
        q8 = request.form['q8']
        q9 = request.form.getlist('q9')
        q10 = request.form['q10']
        q11 = request.form['q11']
        q12 = request.form['q12']
        q13 = request.form.getlist('q13')
        q14 = request.form['q14']
        q15 = request.form['q15']
        q16 = request.form.getlist('q16')
        q17 = request.form['q17']
        q18 = request.form['q18']
        q19 = request.form.getlist('q19')
        q20 = request.form['q20']
        q21 = request.form['q21']
        q22 = request.form['q22']
        q23 = request.form.getlist('q23')
        q24 = request.form.getlist('q24')
        q25 = request.form['q25']
        q26 = request.form['q26']
        personalQuestions.insert({'user_id':session['user_id'],'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4, 'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9, 'q10':q10, 'q11':q11, 'q12':q12, 'q13':q13,
         'q14':q14, 'q15':q15, 'q16':q16, 'q17':q17, 'q18':q18, 'q19':q19, 'q20':q20, 'q21':q21, 'q22':q22, 'q23':q23, 'q24':q24, 'q25':q25, 'q26':q26})
        return redirect(url_for('csQuestions'))
    return render_template('survey/personalQuestions.html')

@app.route('/surveyResults')
def surveyResults():
    #personal questions
    pq = mongo.db.personalQuestions
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    genderMale = pq.find({'q1': 'Male'}).count()
    genderFemale = pq.find({'q1': 'Female'}).count()
    age1 = pq.find({'q2': '12'}).count()
    age2 = pq.find({'q2': '13'}).count()
    age3 = pq.find({'q2': '14'}).count()
    age4 = pq.find({'q2': '15'}).count()
    age5 = pq.find({'q2': '16'}).count()
    age6 = pq.find({'q2': '17'}).count()
    age7 = pq.find({'q2': '18+'}).count()
    year1 = pq.find({'q3': '1st Year'}).count()
    year2 = pq.find({'q3': '2nd Year'}).count()
    year3 = pq.find({'q3': '3rd Year'}).count()
    year4 = pq.find({'q3': '4th Year'}).count()
    year5 = pq.find({'q3': '5th Year'}).count()
    year6 = pq.find({'q3': '6th Year'}).count()
    nativeSpeakerYes = pq.find({'q4': 'Yes'}).count()
    nativeSpeakerNo = pq.find({'q4': 'No'}).count()
    ownsSmartphoneYes = pq.find({'q6': 'Yes'}).count()
    ownsSmartphoneNo = pq.find({'q6': 'No'}).count()
    smartphonehours1 = pq.find({'q8': 'Less than one hour'}).count()
    smartphonehours2 = pq.find({'q8': '1-3 hours'}).count()
    smartphonehours3 = pq.find({'q8': 'More than 3 hours'}).count()
    smartphonehours4 = pq.find({'q8': 'N/A'}).count()
    ownsLaptopYes = pq.find({'q10': 'Yes'}).count()
    ownsLaptopNo = pq.find({'q10': 'No'}).count()
    laptopHours1 = pq.find({'q12': 'Less than one hour'}).count()
    laptopHours2 = pq.find({'q12': '1-3 hours'}).count()
    laptopHours3 = pq.find({'q12': 'More than 3 hours'}).count()
    laptopHours4 = pq.find({'q12': 'N/A'}).count()
    ownsTabletYes = pq.find({'q14': 'Yes'}).count()
    ownsTabletNo = pq.find({'q14': 'No'}).count()
    tabletHours1 = pq.find({'q15': 'Less than one hour'}).count()
    tabletHours2 = pq.find({'q15': '1-3 hours'}).count()
    tabletHours3 = pq.find({'q15': 'More than 3 hours'}).count()
    tabletHours4 = pq.find({'q15': 'N/A'}).count()
    programExpYes = pq.find({'q17': 'Yes'}).count()
    programExpNo = pq.find({'q17': 'No'}).count()
    programExp1 = pq.find({'q18': 'Never programmed before'}).count()
    programExp2 = pq.find({'q18': 'I have done programming once or twice.'}).count()
    programExp3 = pq.find({'q18': 'I have done programming a number of times'}).count()
    programExp4 = pq.find({'q18': 'I have been programming for over a year'}).count()
    programOften1 = pq.find({'q20': 'Never'}).count()
    programOften2 = pq.find({'q20': 'Rarely'}).count()
    programOften3 = pq.find({'q20': 'Neutral'}).count()
    programOften4 = pq.find({'q20': 'Once in a while'}).count()
    programOften5 = pq.find({'q20': 'Daily'}).count()  
    webDevYes = pq.find({'q22': 'Yes'}).count()
    webDevNo = pq.find({'q22': 'No'}).count()
    mathLevel1 = pq.find({'q25': 'Foundation'}).count()
    mathLevel2 = pq.find({'q25': 'Ordinary'}).count()
    mathLevel3 = pq.find({'q25': 'Higher'}).count()
    parentITYes = pq.find({'q26': 'Yes'}).count()
    parentITNo = pq.find({'q26': 'No'}).count()
    parentITNS = pq.find({'q26': 'Not sure'}).count()

    #csQuestions
    cs = mongo.db.csQuestions
    result1 = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree']
    result2 = ['Yes', 'No', 'Maybe']
    result3 = ['Yes', 'No']
    q1 = []
    q3 = []
    q5 = []
    q7 = []
    q8 = []
    q9 = []
    q10 = []
    q11 = []
    q12 = []
    q13 = []
    q14 = []
    q15 = []
    q16 = []

    for i in range(len(result1)) :
        count7 = cs.find({'q7': result1[i]}).count()
        count8 = cs.find({'q8': result1[i]}).count()
        count9 = cs.find({'q9': result1[i]}).count()
        count10 = cs.find({'q10': result1[i]}).count()
        count11 = cs.find({'q11': result1[i]}).count()
        count12 = cs.find({'q12': result1[i]}).count()
        count13 = cs.find({'q13': result1[i]}).count()
        count14 = cs.find({'q14': result1[i]}).count()
        count15 = cs.find({'q15': result1[i]}).count()

        q7.append(count7)
        q8.append(count8)
        q9.append(count9)
        q10.append(count10)
        q11.append(count11)
        q12.append(count12)
        q13.append(count13)
        q14.append(count14)
        q15.append(count15)

    for i in range(len(result2)) :
        count1 = cs.find({'q1': result2[i]}).count()
        count3 = cs.find({'q3': result2[i]}).count()
        count5 = cs.find({'q5': result2[i]}).count()

        q1.append(count1)
        q3.append(count3)
        q5.append(count5)

    for i in range(len(result3)) :
        count16 = cs.find({'q16': result3[i]}).count()

        q16.append(count16)

    return render_template('profile_page/stats.html', name=name, surname=surname, genderMale=genderMale, genderFemale=genderFemale, age1=age1, age2=age2, age3=age3, age4=age4, age5=age5, age6=age6, age7=age7, nativeSpeakerYes=nativeSpeakerYes, nativeSpeakerNo=nativeSpeakerNo, 
        ownsSmartphoneYes=ownsSmartphoneYes, ownsSmartphoneNo=ownsSmartphoneNo,
        year1=year1, year2=year2, year3=year3, year4=year4, year5=year5, year6=year6, smartphonehours1=smartphonehours1, smartphonehours2=smartphonehours2, smartphonehours3=smartphonehours3, smartphonehours4=smartphonehours4, ownsLaptopYes=ownsLaptopYes, ownsLaptopNo=ownsLaptopNo, laptopHours1=laptopHours1,
        laptopHours2=laptopHours2, laptopHours3=laptopHours3, laptopHours4=laptopHours4, ownsTabletYes=ownsTabletYes, ownsTabletNo=ownsTabletNo, tabletHours1=tabletHours1, tabletHours2=tabletHours2, tabletHours3=tabletHours3, tabletHours4=tabletHours4,
        programExpYes=programExpYes, programExpNo=programExpNo, programOften1=programOften1, programOften2=programOften2, programOften3=programOften3, programOften4=programOften4, programOften5=programOften5, programExp1=programExp1, programExp2=programExp2, programExp3=programExp3, programExp4=programExp4, webDevYes=webDevYes, webDevNo=webDevNo, mathLevel1=mathLevel1, mathLevel2=mathLevel2,
        mathLevel3=mathLevel3, parentITYes=parentITYes, parentITNo=parentITNo, parentITNS=parentITNS,
        q1=q1, q3=q3, q5=q5, q7=q7, q8=q8, q9=q9, q10=q10, q11=q11, q12=q12, q13=q13, q14=q14, q15=q15, q16=q16)

####################################################################

#Routes relating to files

#Checking if the file uploaded is in the allowed extention variable
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadFiles', methods=['GET', 'POST'])
def upload_file():
    fs = gridfs.GridFS(mongo.db)
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            oid = fs.put(file, content_type=file.content_type, filename=filename)
            return render_template('files/uploadedFiles.html', name=name, surname=surname)            
    return render_template('files/uploadFile.html', name=name, surname=surname)

@app.route('/allfiles/<oid>')
def serve_gridfs_file(oid):
    fs = gridfs.GridFS(mongo.db)
    try:
        file = fs.get(ObjectId(oid))
        response = make_response(file.read())
        response.mimetype = file.content_type
        return response
    except NoFile:
        abort(404)

#Display all files in Database
@app.route('/files')
def files():
    fs = gridfs.GridFS(mongo.db)
    users = mongo.db.users
    name = users.find_one({'email':session['email']})['name']
    surname = users.find_one({'email':session['email']})['surname']
    files = [fs.get_last_version(file) for file in fs.list()]
    file_list = "\n".join(['<li><a href="%s">%s</a></li>' % \
        (url_for('serve_gridfs_file', oid=str(file._id)), file.name) \
        for file in files])
    return render_template('files/files.html',file_list=file_list, files=files, name=name, surname=surname)

##################################################################

#Lessons

#Module1
@app.route('/module1')
def module1():
    fs = gridfs.GridFS(mongo.db)
    testDB = mongo.db.test
    users = mongo.db.users
    if 'email' in session:
        name = users.find_one({'email':session['email']})['name']
        surname = users.find_one({'email':session['email']})['surname']
        school = users.find_one({'email':session['email']})['school']

    elif 'user_id' in session:
        name = users.find_one({'user_id':session['user_id']})['name']
        surname = users.find_one({'user_id':session['user_id']})['surname']
        school = users.find_one({'user_id':session['user_id']})['school']

    schoolModule = testDB.find_one({'school': school})
    module1 = testDB.find_one({'school': school})['module1']
    array = module1
    files = [fs.get_last_version(file) for file in array]
    return render_template('modules/module1.html' , files=files, name=name, surname=surname)

@app.route('/module2')
def module2():
    fs = gridfs.GridFS(mongo.db)
    testDB = mongo.db.test
    users = mongo.db.users
    if 'email' in session:
        name = users.find_one({'email':session['email']})['name']
        surname = users.find_one({'email':session['email']})['surname']
        school = users.find_one({'email':session['email']})['school']

    elif 'user_id' in session:
        name = users.find_one({'user_id':session['user_id']})['name']
        surname = users.find_one({'user_id':session['user_id']})['surname']
        school = users.find_one({'user_id':session['user_id']})['school']

    schoolModule = testDB.find_one({'school': school})
    module2 = testDB.find_one({'school': school})['module2']
    array = module2
    files = [fs.get_last_version(file) for file in array]
    return render_template('modules/module2.html', files=files, name=name, surname=surname)

@app.route('/module3')
def module3():
    fs = gridfs.GridFS(mongo.db)
    testDB = mongo.db.test
    users = mongo.db.users
    if 'email' in session:
        name = users.find_one({'email':session['email']})['name']
        surname = users.find_one({'email':session['email']})['surname']
        school = users.find_one({'email':session['email']})['school']

    elif 'user_id' in session:
        name = users.find_one({'user_id':session['user_id']})['name']
        surname = users.find_one({'user_id':session['user_id']})['surname']
        school = users.find_one({'user_id':session['user_id']})['school']

    schoolModule = testDB.find_one({'school': school})
    module3 = testDB.find_one({'school': school})['module3']
    array = module3
    files = [fs.get_last_version(file) for file in array]
    return render_template('modules/module3.html' , files=files, name=name, surname=surname)

#Generic template of files for each lesson
@app.route('/modules', methods=['POST','GET'])
def modules():
    testDB = mongo.db.test
    users = mongo.db.users
    school = "Kilcock"
    module1 = ['Algorithms_1_Lesson_Plan.docx', 'Algorithms_1_Lesson_Plan.pdf', 'Algorithms_2_Lesson_Plan.docx','Algorithms_2_Lesson_Plan.pdf','Cryptography_2_Lesson_Plan.pdf',
    'Cryptography_3_Lesson_Plan.docx','Cryptography_3_Lesson_Plan.pdf','Cryptography_4_Lesson_Plan.docx','Cryptography_4_Lesson_Plan.pdf','Cryptography_Lesson_Plan.docx','Cryptography_Lesson_Plan.pdf',
    'Intro_to_Comp_Thinking_Lesson_Plan.docx','Intro_to_Comp_Thinking_Lesson_Plan.pdf','Intro_to_Computer_Science_Lesson_Plan.docx','Intro_to_Computer_Science_Lesson_Plan.pdf','Introduction_to_Computational_Thinking.pptx',
    'Introduction_to_Computer_Science.pptx']
    module2 = ['Cat_and_Mouse_Teachers_Guide.docx','Cat_and_Mouse_Teachers_Guide.pdf','Cat_and_Mouse_Tutorial.docx','Cat_and_Mouse_Tutorial.pdf','Pong_Teachers_Guide.docx','Pong_Teachers_Guide.pdf','Pong_full.docx',
    'Pong_step-by-step_Tutorial.docx','Pong_step-by-step_Tutorial.pdf','Pong_tutorial.docx','Pong_tutorial.pdf','Scratch_Fruit_basket_game.pdf','Scratch_project.docx','Scratch_project.pdf','Start_an_Account.pdf']
    module3 = ['1_Introduction.pptx','2_Variables_and_Expressions.pptx','3_Strings.pptx','4_Keyboard_Input.pptx','Lab_1.docx','Lab_1.pdf','Lab_1_Teachers_Guide.docx','Lab_1_Teachers_Guide.pdf','Lab_2.docx','Lab_2.pdf',
    'Lab_2_Teachers_guide.docx','Lab_2_Teachers_guide.pdf','Python_project.docx','Python_project.pdf']
    testDB.insert({'school': school,'module1': module1, 'module2': module2, 'module3': module3})
    return redirect(url_for('profile'))

#Allows for the functionality of adding uploaded files to a paticular lesson
@app.route('/addModule1')
def addModule1():
    testDB = mongo.db.test
    users = mongo.db.users
    fs = gridfs.GridFS(mongo.db)
    school = users.find_one({'email':session['email']})['school']
    fileID = ObjectId(request.args.get('_id'))
    f = fs.get_last_version(_id=ObjectId(fileID))
    name = f.filename
    testDB.update_one({'school': school}, {'$push': {'module1': name }})
    return redirect(url_for('files'))

#Allows for the functionality of adding uploaded files to a paticular lesson
@app.route('/addModule2')
def addModule2():
    testDB = mongo.db.test
    users = mongo.db.users
    fs = gridfs.GridFS(mongo.db)
    school = users.find_one({'email':session['email']})['school']
    fileID = ObjectId(request.args.get('_id'))
    f = fs.get_last_version(_id=ObjectId(fileID))
    name = f.filename
    testDB.update_one({'school': school}, {'$push': {'module2': name }})
    return redirect(url_for('files'))

#Allows for the functionality of adding uploaded files to a paticular lesson
@app.route('/addModule3')
def addModule3(): 
    testDB = mongo.db.test
    users = mongo.db.users
    fs = gridfs.GridFS(mongo.db)
    school = users.find_one({'email':session['email']})['school']
    fileID = ObjectId(request.args.get('_id'))
    f = fs.get_last_version(_id=ObjectId(fileID))
    name = f.filename
    testDB.update_one({'school': school}, {'$push': {'module3': name }})
    return redirect(url_for('files'))

################################################################

#Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)