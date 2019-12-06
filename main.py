from flask import Flask, redirect, request, render_template, session, flash, escape
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def _init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login') 

app.secret_key = "randomness"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("user password not correct, or user does not exist", 'error')
        
            
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if len(username) < 3 or len(username) > 25 or username == '' or ' ' in username:
            name_error = "That's not a valid username"
        else:
            name_error = None
        if len(password) < 3 or len(password) > 25 or username == '' or ' ' in password:
            pass_error = "That's not a valid password"
        else:
            pass_error = None
        if verify != password:
            verify_error = "Passwords don't match"
        else:
            verify_error = None

       

        if not name_error and not pass_error and not verify_error:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                session['username'] = user.username

                return redirect('/newpost')
            else:
                flash('This user already exists')
                return render_template('signup.html')
        
        

        return render_template('signup.html', name_error=name_error, pass_error=pass_error, verify_error=verify_error)
    else:
        return render_template('signup.html')
        

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']
        

        if title == '':
            title_error = "Please fill in the title"
        else:
            title_error=None

        if body == '':
            body_error = "Please fill in the body"
        else:
            body_error=None
    
        if not title_error and not body_error:
            post = Blog(title=title, body=body, owner=owner)
            db.session.add(post)
            db.session.commit()
            return redirect('/blog')

        return render_template('newpost.html', title='Add a Post', title_error=title_error, body_error=body_error )
    return render_template('newpost.html', title='Add a Post')
   

@app.route('/logout', methods=['POST'])
def logout():
    del session['username']
    return redirect('/login')

@app.route('/post', methods=['GET'])
def post():

    
    return render_template ('post.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    encoded_error = request.args.get("error")

    id = request.args.get('id')
  
    if id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blogs=blogs, error=encoded_error and escape(encoded_error))
    else:
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body, error=encoded_error and escape(encoded_error))
    #return redirect('/blog?id=id', id=id)


@app.route('/', methods=['POST', 'GET'])
def index():
    
    return redirect('/login')

if __name__== '__main__':
    app.run()