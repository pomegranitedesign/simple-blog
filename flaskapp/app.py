# Created by Dmitriy Shin on June 22, 2020
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# Create database
db = SQLAlchemy(app)


# Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())

    def __repr__(self):
        return 'Blog post ' + str(self.id) + ': ' + self.title


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        # This will only be valid for the current session
        db.session.add(new_post)
        db.session.commit()  # This will save the data for the future work
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.created_at).all()
        return render_template('posts.html', all_posts=all_posts)


@app.route('/posts/delete/<int:postID>')
def delete_post(postID: int):
    post = BlogPost.query.get_or_404(postID)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:postID>', methods=['GET', 'POST'])
def edit_post(postID: int):
    post = BlogPost.query.get_or_404(postID)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    return render_template('create.html')


@app.route('/post/<int:postID>')
def get_single_post(postID: int):
    post = BlogPost.query.get_or_404(postID)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
