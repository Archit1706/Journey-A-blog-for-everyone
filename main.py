from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail


app = Flask(__name__)
db = SQLAlchemy(app)

mail = Mail(app)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server']

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='587',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_password']
)


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Posts(db.Model):
    '''
    srno, title, slug, content, date, postedBy
    '''
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    postedBy = db.Column(db.String(50), nullable=False)


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template('index.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


# @app.route("/post")
@app.route("/post/<string:post_slug>", methods=["GET"])
def post_func(post_slug):

    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html', params=params, post=post)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone=phone,
                         message=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            'New Message from ' + name,
            sender=email,
            recipients=params['gmail_user'],
            body=message + "\n" + phone
        )
    return render_template('contact.html', params=params)


app.run(debug=True)