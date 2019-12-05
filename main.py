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
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
        




@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
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
            post = Blog(title=title, body=body)
            db.session.add(post)
            db.session.commit()
            return redirect('/blog')

        return render_template('new_post.html', title='Add a Post', title_error=title_error, body_error=body_error )
    return render_template('new_post.html', title='Add a Post')
   

@app.route('/post', methods=['GET'])
def post():

    
    return render_template ('post.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    id = request.args.get('id')
  
    if id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blogs=blogs)
    else:
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body)
    #return redirect('/blog?id=id', id=id)


@app.route('/', methods=['POST', 'GET'])
def index():

    return redirect('/blog')

if __name__== '__main__':
    app.run()