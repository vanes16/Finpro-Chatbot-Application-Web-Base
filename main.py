import google_authen
import training_bot
import predict_bot
from flask import Flask, request, url_for, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

import smtplib
import ssl
from email.message import EmailMessage

from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
import json
import os
import datetime
import string
import random

app = Flask(__name__, template_folder='public',
            static_folder='public/style')

app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finpro.db'
app.config['UPLOAD_FOLDER'] = 'public/style/'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    hashcode = db.Column(db.String(120))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))
    username = db.Column(db.String(100), unique=True)


class chatLog(db.Model):
    __tablename__ = 'chatlog'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(1000))
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class NewsContent(db.Model):
    __tablename__ = 'newcontents'
    id = db.Column(db.Integer, primary_key=True)
    admin = relationship(Admin)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admin.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.String(200))
    filename = db.Column(db.String(400))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class SliderContent(db.Model):
    __tablename__ = 'slidercontents'
    id = db.Column(db.Integer, primary_key=True)
    admin = relationship(Admin)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admin.id'))
    title = db.Column(db.String(100))
    content = db.Column(db.String(100))
    filename = db.Column(db.String(400))
    updated_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)


class PromoContent(db.Model):
    __tablename__ = 'promo'
    id = db.Column(db.Integer, primary_key=True)
    admin = relationship(Admin)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admin.id'))
    filename = db.Column(db.String(400))
    updated_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)


class AboutContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = relationship(Admin)
    admin_id = db.Column(db.Integer, db.ForeignKey(
        'admin.id'))
    about = db.Column(db.String(400))
    history = db.Column(db.String(400))
    updated_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)


@ app.route('/')
def index():
    if session.get('logged_in'):
        slider = SliderContent.query.all()
        promo = PromoContent.query.all()
        news = NewsContent.query.all()
        name = session['username']
        role = session['role']
        return render_template('index.html', name=name, role=role, slider=slider, promo=promo, new=news)
    else:
        return render_template('login.html')


@ app.route('/about')
def about():
    if session.get('logged_in'):
        name = session['username']
        role = session['role']
        about = AboutContent.query.get(1)
        return render_template('about.html', name=name, role=role, about=about)
    else:
        return render_template('login.html')


@ app.route('/item_desc')
def item_desc():
    if session.get('logged_in'):
        id = request.args.get('id')
        if not id:
            return redirect(url_for('index'))
        else:
            name = session['username']
            role = session['role']
            news = NewsContent.query.get(id)
            return render_template('item-desc.html', news=news, role=role, name=name)
    else:
        return render_template('login.html')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username'].lower()
        e = request.form['email'].lower()
        p = request.form['password']

        datauser = User.query.filter_by(username=u).first()
        if datauser is not None:
            session['logged_in'] = False
            return render_template('login.html', message="User Already Exists")
        else:
            dataemail = User.query.filter_by(email=e).first()
            if dataemail is not None:
                session['logged_in'] = False
                return render_template('login.html', message="Email Already Exists")
            else:
                db.session.add(
                    User(username=u, email=e, password=p, hashcode="None"))
                db.session.commit()
                session['google'] = False
                session['logged_in'] = True

                getData = User.query.filter_by(username=u, password=p).first()
                admin = Admin.query.filter_by(username=u).first()

                session['username'] = getData.username
                if admin is not None:
                    session['role'] = "Admin"
                else:
                    session['role'] = "User"

                return redirect(url_for('index'))
    else:
        if session.get('logged_in'):
            return render_template('index.html')
        else:
            return render_template('login.html')


@ app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            return render_template('index.html')
        else:
            return render_template('login.html')
    else:
        u = request.form['username'].lower()
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()

        if data is not None:
            getData = User.query.filter_by(username=u).first()
            admin = Admin.query.filter_by(username=u).first()

            if admin is not None:
                session['role'] = "Admin"
            else:
                session['role'] = "User"

            session['username'] = getData.username
            session['logged_in'] = True
            session['google'] = False
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="Username Or Password Is Incorrect")


@app.route('/forgot-password', methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        email_sender = 'vandelucas24@gmail.com'
        email_password = 'wwxokskwrdwycxlh'

        u = request.form['username'].lower()
        check = User.query.filter_by(username=u).first()

        if check is not None:
            hashcode = ''.join(random.choices(
                string.ascii_letters + string.digits, k=24))
            check.hashcode = hashcode
            db.session.commit()
            subject = 'Reset Password Request PT XYZ Account'
            body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n https://bckwcs-5000.csb.app/" + check.hashcode
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = check.email
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, check.email, em.as_string())
            return render_template('login.html', message="Check Your Email")
        else:
            return render_template('login.html', message="Invalid Username")
    else:
        return render_template('forgot-password.html')


@app.route("/<string:hashcode>", methods=["GET", "POST"])
def hashcode(hashcode):
    check = User.query.filter_by(hashcode=hashcode).first()
    if check is not None:
        if request.method == 'POST':
            passw = request.form['password']
            check.password = passw
            check.hashcode = None
            db.session.commit()

            admin = Admin.query.filter_by(username=check.username).first()

            if admin is not None:
                session['role'] = "Admin"
            else:
                session['role'] = "User"

            session['username'] = check.username
            session['logged_in'] = True
            session['google'] = False
            return redirect(url_for('index'))
        else:
            return render_template('changepw.html', msg=hashcode)
    else:
        return render_template('login.html', message="Invalid Link To Change Password")


@ app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    session['logged_in'] = False
    return redirect(url_for('index'))


@ app.route('/google', methods=['GET'])
def google():
    return google_authen.google_authen()


@ app.route('/callback')
def callback():
    return google_authen.callback()


@app.route('/admin-index')
def adm_index():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            users = User.query.all()

            name = session['username']
            return render_template("admin-index.html", users=users, name=name)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin-list')
def adm_list():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            admin = Admin.query.all()

            name = session['username']
            return render_template("admin-list.html", admin=admin, name=name)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin-list-add', methods=['GET', 'POST'])
def adm_add():
    if request.method == 'POST':
        u = request.form['username']
        data = User.query.filter_by(
            username=u).first()

        if data is not None:
            admin = Admin.query.filter_by(user_id=data.id).first()

            if admin is not None:
                flash("Admin Account Already Available")
                return redirect(url_for('adm_list'))
            else:
                adm_add = Admin(user_id=data.id, username=u)
                db.session.add(adm_add)
                db.session.commit()
                flash("Sucess Add Admin Role")
                return redirect(url_for('adm_list'))
        else:
            flash("Fail to add, User not found")
            return redirect(url_for('adm_list'))

    else:
        if session.get('logged_in'):
            if session['role'] == "Admin":
                name = session['username']
                return render_template('admin-add.html', name=name)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))


@app.route('/admin-content')
def adm_content():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            news = NewsContent.query.all()
            name = session['username']
            return render_template("admin-content.html", news=news, name=name)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin-news-add', methods=['GET', 'POST'])
def news_add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        pic = request.files['pic']
        filename = secure_filename(pic.filename)

        admin = Admin.query.filter_by(username=session['username']).first()

        if not filename:
            flash("Fail To Add News Content , Cause No Files Uploaded")
        else:
            news_add = NewsContent(admin_id=admin.id,
                                   title=title, content=content, filename="./style/"+filename)

            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            db.session.add(news_add)

            db.session.commit()

            flash("News Content added.")
    else:
        if session.get('logged_in'):
            if session['role'] == "Admin":
                name = session['username']
                return render_template('admin-news-add.html', name=name)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return redirect(url_for('adm_content'))


@app.route('/admin-news-delete')
def news_delete():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            id = request.args.get('id')
            if not id:
                flash("No News Content ID Provided.")
            else:
                db.session.delete(NewsContent.query.get(id))
                db.session.commit()
                flash("Content deleted.")
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

    return redirect(url_for('adm_content'))


@app.route('/admin-news-edit', methods=['GET', 'POST'])
def news_edit():
    if request.method == 'POST':
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        news = NewsContent.query.get(request.form.get('id'))

        if not filename:
            if news.filename == "":
                flash("Fail To Edit News Content , Cause No Files Uploaded")
            else:
                news.admin_id = Admin.query.filter_by(
                    username=session['username']).first().id
                news.title = request.form.get('title')
                news.content = request.form.get('content')
                news.filename = news.filename
                db.session.commit()
                flash("News Content Edited.")

        else:
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            news.admin_id = Admin.query.filter_by(
                username=session['username']).first().id
            news.title = request.form.get('title')
            news.content = request.form.get('content')
            news.filename = "./style/"+filename
            db.session.commit()
            flash("News Content Edited.")
    else:
        if session.get('logged_in'):
            if session['role'] == "Admin":
                id = request.args.get('id')
                if not id:
                    flash("No News Content ID provided.")
                else:
                    name = session['username']
                    news = NewsContent.query.get(id)
                    return render_template('admin-news-edit.html', news=news, name=name)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return redirect(url_for('adm_content'))


@app.route('/admin-slider')
def adm_slider():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            slider = SliderContent.query.all()
            name = session['username']
            return render_template("admin-slider.html", slider=slider, name=name)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin-slider-edit', methods=['GET', 'POST'])
def slider_edit():
    if request.method == 'POST':
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        slider = SliderContent.query.get(request.form.get('id'))
        if not filename:
            if slider.filename == "":
                flash("Fail To Edit Slider Content , Cause No Files Uploaded")
            else:
                slider.admin_id = Admin.query.filter_by(
                    username=session['username']).first().id
                slider.title = request.form.get('title')
                slider.content = request.form.get('content')
                slider.filename = slider.filename
                slider.updated_date = datetime.datetime.utcnow()
                db.session.commit()
                flash("Slider Content Edited.")
        else:
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            slider.admin_id = Admin.query.filter_by(
                username=session['username']).first().id
            slider.title = request.form.get('title')
            slider.content = request.form.get('content')
            slider.filename = "./style/"+filename
            slider.updated_date = datetime.datetime.utcnow()
            db.session.commit()
            flash("Slider Content Edited.")
    else:
        if session.get('logged_in'):
            if session['role'] == "Admin":
                id = request.args.get('id')
                if not id:
                    flash("No Slider Content ID provided.")
                else:
                    name = session['username']
                    slider = SliderContent.query.get(id)
                    return render_template('admin-slider-edit.html', slider=slider, name=name)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return redirect(url_for('adm_slider'))


@app.route('/admin-promo')
def adm_promo():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            promo = PromoContent.query.all()
            name = session['username']
            return render_template("admin-promo.html", promo=promo, name=name)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin-promo-edit', methods=['GET', 'POST'])
def promo_edit():
    if request.method == 'POST':
        pic = request.files['pic']
        filename = secure_filename(pic.filename)
        promo = PromoContent.query.get(request.form.get('id'))

        if not filename:
            if promo.filename == "":
                flash("Fail To Edit Promo Content , Cause No Files Uploaded")
        else:
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            promo.admin_id = Admin.query.filter_by(
                username=session['username']).first().id
            promo.filename = "./style/"+filename
            promo.updated_date = datetime.datetime.utcnow()
            db.session.commit()
            flash("Promo Content Edited.")
    else:
        if session.get('logged_in'):
            if session['role'] == "Admin":
                id = request.args.get('id')
                if not id:
                    flash("No Promo Content ID provided.")
                else:
                    name = session['username']
                    promo = PromoContent.query.get(id)
                    return render_template('admin-promo-edit.html', promo=promo, name=name)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return redirect(url_for('adm_promo'))


@app.route('/admin-about', methods=['GET', 'POST'])
def about_edit():
    if request.method == 'POST':
        about = request.form.get('about')
        history = request.form.get('history')
        abouts = AboutContent.query.get(1)
        abouts.admin_id = Admin.query.filter_by(
            username=session['username']).first().id
        abouts.about = about
        abouts.history = history
        abouts.updated_date = datetime.datetime.utcnow()

        db.session.commit()
        flash("About Content Edited.")
    else:
        if session.get('logged_in'):
            if session['role'] == "Admin":
                name = session['username']
                about = AboutContent.query.all()
                return render_template('admin-about.html', about=about, name=name)
        else:
            return redirect(url_for('login'))

    return redirect(url_for('about_edit'))


@app.route('/admin-monitor')
def adm_monitor():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            chatlog = chatLog.query.all()
            name = session['username']
            a = db.session.query(chatLog.user_id).distinct().all()
            a = len(a)
            b = db.session.query(User.id).distinct().all()
            b = len(b)
            return render_template("admin-monitoring.html", name=name, chat=chatlog, a=a / b / 0.01)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/admin-monitor-delete')
def adm_monitor_delete():
    if session.get('logged_in'):
        if session['role'] == "Admin":

            db.session.query(chatLog).delete()
            db.session.commit()
            flash("Data Log deleted.")
            return redirect(url_for('adm_monitor'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/update', methods=['GET'])
def updateSys():
    if session.get('logged_in'):
        if session['role'] == "Admin":
            training_bot.exec_training_bot()
            flash("System updated")
            return redirect(url_for('adm_monitor'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route("/bot-resp")
def get_bot_response():
    if session.get('logged_in'):
        userText = request.args.get('userInput')
        response = predict_bot.botResponse(userText)

        if not session.get('google'):
            getUserID = User.query.filter_by(
                username=session["username"]).first()
            chatlog = chatLog(user_id=getUserID.id,
                              question=userText, answer=response)
            db.session.add(chatlog)
            db.session.commit()
        else:
            chatlog = chatLog(user_id="google",
                              question=userText, answer=response)
            db.session.add(chatlog)
            db.session.commit()
        return response
    else:
        return redirect(url_for('login'))


@app.route('/get-darkmode', methods=['POST'])
def getDataDarkMode():
    output = request.get_json()
    result = json.loads(output)

    session['darkmode'] = result
    return session['darkmode']


@app.route('/send-darkmode')
def sendDataDarkMode():
    if session['darkmode'] == "":
        session['darkmode'] = "light"
    return session['darkmode']


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
