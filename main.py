from flask import Flask, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    new_post = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        





@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blog.html', title="Build A Blog")