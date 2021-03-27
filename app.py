from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, RadioField, SubmitField, HiddenField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import os
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
#import cv2
import time
from datetime import timedelta
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime
from flask_avatars import Avatars
from imgurpython import ImgurClient
from datetime import datetime
from api import client_id,client_secret,access_token,refresh_token,album,iconAlbum

app = Flask(__name__)
app.secret_key=

avatars = Avatars(app)

app.config['MYSQL_HOST'] = 
app.config['MYSQL_USER'] = 
app.config['MYSQL_PASSWORD'] = 
app.config['MYSQL_DB'] = 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['AVATARS_SAVE_PATH'] = os.path.join(basedir, 'avatars')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('home.html')

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=20)])
    email = StringField('Email', [validators.Length(min=6, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM user WHERE Username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['Password']
            admin = data['Admin']
            session['icon'] = data['icon']

            if sha256_crypt.verify(password_candidate, password):

                session['logged_in'] = True
                session['Username'] = username
                session['Admin'] = admin

                flash('You are now logged in', 'success')
                return render_template('dashboard.html')
            else:
                error = 'Invalid login'
                return render_template('home.html', error=error)

            cur.close()
        else:
            error = 'Username not found'
            return render_template('home.html', error=error)

    return render_template('dashboard.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM user WHERE Username = %s", [session['Username']])

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No user Found'
        return render_template('dashboard.html', msg=msg, articles=articles)

    cur.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        try:

            cur.execute("INSERT INTO user(Email, Username, Password) VALUES(%s, %s, %s)", (email, username, password))

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('register', form=form))

    return render_template('register.html', form=form)

@app.route('/img/<path:filename>')
def send_file(filename):

    cur = mysql.connection.cursor()

    mysql.connection.commit()

    cur.execute("SELECT icon FROM user WHERE Username = %s", [session['Username']])
    icon = cur.fetchall()
    for e in icon:
        iconn = e['icon']

    cur.close()

    return send_from_directory('avatars', filename = iconn)

@app.route('/img/<path:filename>')
def sendimage(filename):

    return send_from_directory(UPLOAD_FOLDER, filename = filename)

@app.route('/profile')
def profile():

    cur = mysql.connection.cursor()

    cur.execute("SELECT Email, Description, icon FROM user WHERE Username = %s", [session['Username']])

    userdata = cur.fetchall()

    for e in userdata:
        session.email = e['Email']
        session.description = e['Description']

        if session.description == '':
            session.description = 'Not avaiable'

    mysql.connection.commit()

    cur.close()

    return render_template('profile.html', userdata=userdata)

class Profile(Form):
    pass

@app.route('/aprofile/<string:name>/')
def aprofile(name):

    cur = mysql.connection.cursor()

    cur.execute("SELECT Email, icon, Description FROM user WHERE Username = %s", [name])

    data = cur.fetchone()

    mysql.connection.commit()

    cur.close()

    return render_template('aprofile.html', data=data)

@app.route('/aprofile2/<string:name>/', methods=['GET', 'POST'])
def aprofile2(name):

    form = Aprofile2(request.form)

    cur = mysql.connection.cursor()

    cur.execute("SELECT Userid, Username, Email, icon, Description FROM user WHERE Username = %s", [name])

    data = cur.fetchone()

    mysql.connection.commit()

    cur.close()

    if request.method == 'POST' and form.uid.data:

        cur = mysql.connection.cursor()

        try:

            cur.execute("DELETE FROM user where Userid = %s", [form.uid.data])

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('The user is deleted', 'success')

        return redirect(url_for('swview'))

    return render_template('aprofile2.html', data=data, form=form)

class Aprofile2(Form):
    uid = HiddenField()

@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(app.config['AVATARS_SAVE_PATH'], filename)

@app.route('/icon', methods=['GET', 'POST'])
def icon():

    if request.method == 'POST' and request.files.get('file'):
        file = request.files.get('file')
        tempfilename = avatars.save_avatar(file)
        session['tempfilename'] = tempfilename
        return redirect(url_for('crop'))

    return render_template('icon.html')

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        filenames = avatars.crop_avatar(session['tempfilename'], x, y, w, h)

        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        localpath = os.path.join(app.config['AVATARS_SAVE_PATH'], filenames[2])
        image = imgurUpload(client, iconAlbum, session['Username'], 'avatars', 'avatars', localpath)
        image_url = image['link']

        try:

            cur = mysql.connection.cursor()

            cur.execute("UPDATE user set icon = (%s) where Username = (%s)", (image_url, session['Username']))

            mysql.connection.commit()

            cur.close()

            session['icon'] = image_url

            flash('Icon is changed', 'success')

            try:

                os.remove(os.path.join(app.config['AVATARS_SAVE_PATH'], filenames[0]))
                os.remove(os.path.join(app.config['AVATARS_SAVE_PATH'], filenames[1]))
                os.remove(os.path.join(app.config['AVATARS_SAVE_PATH'], filenames[2]))
                os.remove(os.path.join(app.config['AVATARS_SAVE_PATH'], session['tempfilename']))

            except:

                pass

        except:

            cur.rollback()

            flash('Update fail', 'error')

        return redirect(url_for('profile'))

    return render_template('crop.html')

@app.route('/change', methods=['GET', 'POST'])
def change():
    form = changeform(request.form)

    if request.method == 'POST' and form.validate() and form.email.data:

        email = form.email.data

        cur = mysql.connection.cursor()

        try:

            cur.execute("UPDATE user set Email = (%s) where Username = (%s)", (email, session['Username']))

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('Email is updated', 'success')


    if request.method == 'POST' and form.validate() and form.password.data:

        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        try:

            cur.execute("UPDATE user set Password = (%s) where Username = (%s)", (password, session['Username']))

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('Password is updated', 'success')

    if request.method == 'POST' and form.validate() and form.description.data:

        description = form.description.data

        cur = mysql.connection.cursor()

        try:

            cur.execute("UPDATE user set Description = (%s) where Username = (%s)", (description, session['Username']))

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('Description is updated', 'success')

        return redirect(url_for('change', form=form))

    return render_template('change.html', form=form)

class changeform(Form):
    email = StringField('Email', [validators.optional(),validators.Length(min=6, max=100)])
    password = PasswordField('Password', [
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    description = TextAreaField('Description', [validators.optional(), validators.length(max=1000)])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = Upload(request.form)

    cur = mysql.connection.cursor()

    cur.execute("SELECT Email, Description, icon FROM user WHERE Username = %s", [session['Username']])

    userdata = cur.fetchall()

    if request.method == 'POST' and form.validate():

        if 'file' not in request.files:
            flash('It is empty', 'error')
            return redirect(request.url)
        file = request.files['file']
        #print(file)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(time.time())+secure_filename(file.filename)
            imagepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(imagepath)
            wname = form.wname.data
            description = form.description.data

            try:

                client = ImgurClient(client_id, client_secret, access_token, refresh_token)
                image = imgurUpload(client, album, wname, wname, description, imagepath)
                image_url = image['link']

            except:

                flash('image upload failed', 'error')

            try:

                cur = mysql.connection.cursor()

                cur.execute("INSERT INTO works(Author, Wname, iname, aname, Description) VALUES(%s, %s, %s, %s, %s)", ( [session['Username']], wname, image_url, 'temp', description))

                mysql.connection.commit()

                cur.close()

                flash('image is uploaded', 'success')
                send_from_directory(UPLOAD_FOLDER, filename = filename)

            except:

                cur.rollback()

            try:

                os.remove(imagepath)

            except:

                pass

            return redirect(url_for('upload', form=form, userdata=userdata))

    return render_template('upload.html', form=form, userdata=userdata)

class Upload(Form):
    wname = StringField('Title', [validators.Length(min=1, max=100)])
    clist = [('fantasy','Fantasy'),('real','Real'),('anime','Anime'),('unknown','Unknown')]
    description = TextAreaField('Description', [validators.optional(), validators.length(max=1000)])

@app.route('/edit/<string:id>/', methods=['GET', 'POST'])
def edit(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM works WHERE id = %s", [id])

    work = cur.fetchone()

    mysql.connection.commit()

    cur.close()

    form = Edit(request.form)

    if request.method == 'POST' and form.validate():

        name = form.wname.data
        description = form.description.data

        if name != "":

            cur = mysql.connection.cursor()

            try:

                cur.execute("UPDATE works set Wname = (%s) where id = (%s)", (name, [id]))

            except:

                cur.rollback()

            work = cur.fetchone()

            mysql.connection.commit()

            cur.close()

        if description != "":

            cur = mysql.connection.cursor()

            try:

                cur.execute("UPDATE works set Description = (%s) where id = (%s)", (description, [id]))

            except:

                cur.rollback()

            work = cur.fetchone()

            mysql.connection.commit()

            cur.close()

        flash('Work information is updated', 'success')

        return redirect(url_for('edit', id=id))

    if form.wid.data:

        cur = mysql.connection.cursor()

        try:

            cur.execute("DELETE FROM works where id = %s", [form.wid.data])

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('Work work.Wname is deleted', 'success')

        return render_template('uview.html')

    return render_template('edit.html', form=form, work=work, id=id)

class Edit(Form):
    wname = StringField('Title', [validators.optional(),validators.Length(min=1, max=100)])
    #clist = [('',''),('fantasy','Fantasy'),('real','Real'),('anime','Anime'),('unknown','Unknown')]
    description = TextAreaField('Description', [validators.optional(), validators.length(max=1000)])
    wid = HiddenField()

@app.route('/wview', methods=['GET', 'POST'])
def wview():

    form = Wview(request.form)

    try:

        cur = mysql.connection.cursor()

        #result = cur.execute("SELECT * FROM works")

        result = cur.execute("SELECT a.icon, b.* FROM `user` as a, `works` as b where a.Username = b.Author ORDER BY b.id DESC")

        mysql.connection.commit()

        wdata = cur.fetchall()

        cur.close()

        if result > 0:
            return render_template('wview.html', wdata=wdata, form=form)
        else:
            msg = 'No work Found'
            return render_template('wview.html', msg=msg, form=form)

    except:

        flash("database error","error")

    return redirect(url_for('wview.html', form=form))

class Wview(Form):

    order = SelectField('Order: ', choices = [('Title','Name')])
    clist = [('',''),('fantasy','Fantasy'),('real','Real'),('anime','Anime'),('unknown','Unknown')]

@app.route('/work/<string:id>/', methods=['GET', 'POST'])
def work(id):

    cur = mysql.connection.cursor()

    try:

        cur.execute("SELECT * FROM works WHERE id = %s", [id])

        work = cur.fetchone()

    except:

        flash('There is database error', 'error')

    try:

        cur.execute("SELECT * FROM user WHERE Username = %s", [work['Author']])

        creater = cur.fetchone()

    except:

        flash('There is database error', 'error')

    try:

        cur.execute("SELECT a.icon, b.* FROM `user` as a, `comment` as b where b.wid = %s and a.Username = b.postuser", [id])

        comment = cur.fetchall()

    except:

        flash('There is database error', 'error')

    mysql.connection.commit()

    cur.close()

    form = Comment(request.form)

    if form.content.data and form.validate():

        cur = mysql.connection.cursor()

        try:

            cur.execute("INSERT INTO comment(wid, postuser, content) values(%s, %s, %s)", (id, session['Username'], form.content.data))

        except:
                cur.rollback()

        mysql.connection.commit()

        cur.close()

        form.content.data = ""

        return redirect(url_for('work', id=id))

    if form.pid.data and form.commentid.data:

        cur = mysql.connection.cursor()

        try:

            cur.execute("DELETE FROM comment where commentid = %s and postuser = %s", (form.commentid.data, form.pid.data))

        except:
                cur.rollback()

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('work', id=id))

    return render_template('work.html', work=work, creater=creater, form=form, comment=comment)

@app.route('/work2/<string:id>/', methods=['GET', 'POST'])
def work2(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM works WHERE id = %s", [id])

    work = cur.fetchone()

    cur.execute("SELECT * FROM user WHERE Username = %s", [work['Author']])

    creater = cur.fetchone()

    cur.execute("SELECT a.icon, b.* FROM `user` as a, `comment` as b where b.wid = %s and a.Username = b.postuser", [id])

    comment = cur.fetchall()

    mysql.connection.commit()

    cur.close()

    form2 = Work2(request.form)


    if request.method == 'POST' and form2.wid.data:

        cur = mysql.connection.cursor()

        try:

            cur.execute("DELETE FROM works where id = %s", [form2.wid.data])

        except:

            cur.rollback()

        mysql.connection.commit()

        cur.close()

        flash('The tiem is deleted', 'success')

        return redirect(url_for('swview2'))

    form = Comment(request.form)

    if form.content.data and form.validate():

        cur = mysql.connection.cursor()

        try:

            cur.execute("INSERT INTO comment(wid, postuser, content) values(%s, %s, %s)", (id, session['Username'], form.content.data))

        except:
                cur.rollback()

        mysql.connection.commit()

        cur.close()

        form.content.data = ""

        return redirect(url_for('work2', id=id))

    if form.pid.data and form.commentid.data:

        cur = mysql.connection.cursor()

        try:

            cur.execute("DELETE FROM comment where commentid = %s and postuser = %s", (form.commentid.data, form.pid.data))

        except:
                cur.rollback()

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('swview2', id=id))

    return render_template('work2.html', work=work, creater=creater, form=form, comment=comment, form2=form2)

class Work2(Form):
    wid = HiddenField()

@app.route('/swview', methods=['GET', 'POST'])
def swview():

    form = Swview(request.form)

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM user")

    mysql.connection.commit()

    wdata = cur.fetchall()

    if result > 0:
        return render_template('swview.html', form=form, wdata=wdata)
    else:
        msg = 'No wusers Found'
        return render_template('swview.html', form=form, msg=msg)

    cur.close()

class Swview(Form):
    uid = HiddenField()

@app.route('/swview2', methods=['GET', 'POST'])
def swview2():

    form = Swview(request.form)

    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM works")

    mysql.connection.commit()

    wdata = cur.fetchall()

    if result > 0:
        return render_template('swview2.html', form=form, wdata=wdata)
    else:
        msg = 'No wusers Found'
        return render_template('swview2.html', form=form, msg=msg)

    cur.close()

class Swview2(Form):
    uid = HiddenField()

@app.route('/uview')
def uview():

    cur = mysql.connection.cursor()

    #result = cur.execute("SELECT * FROM works where Author = %s",([session['Username']]))

    result = cur.execute("SELECT a.icon, b.* FROM `user` as a, `works` as b where a.Username = b.Author and Author = %s",([session['Username']]))

    mysql.connection.commit()

    wdata = cur.fetchall()

    cur.execute("SELECT Email, Description, icon FROM user WHERE Username = %s", [session['Username']])

    userdata = cur.fetchall()

    if result > 0:
        return render_template('uview.html', wdata=wdata, userdata=userdata)
    else:
        msg = 'No work Found'
        return render_template('uview.html', msg=msg, userdata=userdata)

    cur.close()

@app.route('/uwork/<string:id>/', methods=['GET', 'POST'])
def uwork(id):
    cur = mysql.connection.cursor()

    try:

        cur.execute("SELECT * FROM works WHERE id = %s", [id])

        work = cur.fetchone()

    except:

        flash('There is database error', 'error')

    try:

        cur.execute("SELECT * FROM user WHERE Username = %s", [work['Author']])

        creater = cur.fetchone()

    except:

        flash('There is database error', 'error')

    try:

        cur.execute("SELECT * FROM comment where wid = %s", [id])

        comment = cur.fetchall()

    except:

        flash('There is database error', 'error')

    mysql.connection.commit()

    cur.close()

    form = Comment(request.form)

    if form.content.data and form.validate():

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO comment(wid, postuser, usericon, content) values(%s, %s, %s, %s)", (id, session['Username'], session['icon'], form.content.data))

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('uwork', id=id))

    if form.pid.data and form.commentid.data:

        cur = mysql.connection.cursor()

        cur.execute("DELETE FROM comment where commentid = %s and postuser = %s", (form.commentid.data, form.pid.data))

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('uwork', id=id))

    return render_template('uwork.html', work=work, creater=creater, form=form, comment=comment)

class Comment(Form):

    content = TextAreaField('Comment', [validators.length(max=1000)])
    pid = HiddenField()
    commentid = HiddenField()

def imgurUpload(client_data, album , name, title, description, uimagepath):
    config = {
        'album':  album,
        'name': name,
        'title': title,
        'description': description
    }

    image = client_data.upload_from_path(uimagepath, config=config, anon=False)

    return image

if __name__ == '__main__':
    #app.secret_key='1234'
    app.run()
