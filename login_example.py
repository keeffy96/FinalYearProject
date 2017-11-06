from flask import Flask, render_template, url_for, request, session, redirect, send_file, make_response, abort
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from gridfs.errors import NoFile
from werkzeug import secure_filename
import bcrypt
import gridfs
import random

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pptx'])
db = MongoClient().connect_to_mongo
fs = gridfs.GridFS(db)
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
        user_id = school + str(random.randint(1,1000)) 
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
        instructorSchool = users.find_one({'email':session['email']})['school']        
        return render_template('profile_page/profile.html', name=name, surname=surname, instructorSchool=instructorSchool)

    elif 'user_id' in session:
        name = users.find_one({'user_id':session['user_id']})['name']
        surname = users.find_one({'user_id':session['user_id']})['surname']
        userid = users.find_one({'user_id':session['user_id']})['user_id']
        return render_template('profile_page/profile.html', name=name, surname=surname, userid=userid)

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

@app.route('/bebras1/', methods=['POST','GET'])
def bebras1():
    if request.method == 'POST':
        babras1 = mongo.db.babras1
        users = mongo.db.users
        user_id = users.find_one({'user_id':session['user_id']})['user_id']
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        answer3 = request.form['answer3']
        answer4 = request.form['answer4']
        answer5 = request.form['answer5']
        answer6 = request.form['answer6']
        babras1.insert({'user_id': user_id,'answer1': answer1, 'answer2': answer2, 'answer3': answer3, 'answer4': answer4, 'answer5': answer5, 'answer6': answer6})
        return redirect(url_for('profile'))

    return render_template('bebras_test/bebras1.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'), 404

@app.route('/test')
def test():
    return render_template('testTest.html')

@app.route('/sideBar')
def sideBar():
    return render_template('newTest.html')

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
            return redirect(url_for('serve_gridfs_file', oid=str(oid)))            
    return render_template('files/uploadFile.html')

@app.route('/files')
def list_gridfs_files():
    files = [fs.get_last_version(file) for file in fs.list()]
    file_list = "\n".join(['<li><a href="%s">%s</a></li>' % \
                            (url_for('serve_gridfs_file', oid=str(file._id)), file.name) \
                            for file in files])
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Files</title>
    </head>
    <body>
    <h1>Files</h1>
    <ul>
    %s
    </ul>
    <a href="%s">Upload new file</a>
    </body>
    </html>
    ''' % (file_list, url_for('upload_file'))

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