from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogspot4me@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/")
def index():
    return redirect('/blog')

@app.route("/blog")
def blog_index():
    if not request.args.get('id'):
        posts = Blog.query.all()
        return render_template("blog.html", title="Blog", posts=posts)
    else:
        post_id = request.args.get('id')
        post = Blog.query.get(post_id)
        return render_template("post.html", post=post)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost_index():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

        new_blog_route = '/blog?id=' + str(new_blog.id)
        return redirect(new_blog_route)
    else:
        return render_template("newpost.html", title="New Post")

    

if __name__ == '__main__':
    app.run()