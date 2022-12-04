import os
import smtplib
from datetime import date
from functools import wraps
from urllib.parse import urlparse, urljoin

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from forms import RegisterForm, CreatePostForm, LoginForm, CommentForm, ContactForm

# Directory to your .env file
load_dotenv('.../.env.txt')


def create_app_tools():
    app_ = Flask(__name__, static_folder='static')
    app_.config['SECRET_KEY'] = 'any_key_you_like'
    app_.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
    app_.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_ = SQLAlchemy(app_)
    Bootstrap(app_)
    ckeditor_ = CKEditor(app_)
    login_manager_ = LoginManager()
    login_manager_.init_app(app_)
    login_manager_.login_view = "login"
    gravatar_ = Gravatar(app_,
                         size=100,
                         rating='g',
                         default='retro',
                         force_default=False,
                         force_lower=False,
                         use_ssl=False,
                         base_url=None)
    return app_, db_, ckeditor_, login_manager_, gravatar_


def send_email(name, email, phone, message) -> None:

    # The gmail address that will send you the contacter's message and other information to your desired email address
    # You need to get an App Password for this account
    gmail = "some@gmail.com"

    # Load the password from environment file or enter here directly
    password_gmail = os.getenv("GMAIL_PASSWORD")
    connection_gmail = smtplib.SMTP("smtp.gmail.com", port=587)
    message_text = "Subject:Your Blog Contact!\n\n" \
                   f"Name: {name}\n" \
                   f"Phone: {phone}\n" \
                   f"Email: {email}\n" \
                   f"Message: {message}"

    with connection_gmail as connection:
        connection.starttls()
        connection.login(user=gmail, password=password_gmail)
        connection.sendmail(from_addr=gmail,
                            # The desired email address to send the information
                            to_addrs="any@gmail.com",
                            msg=message_text.encode('utf-8'))


app, db, ckeditor, login_manager, gravatar = create_app_tools()
Base = declarative_base()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="parent_post")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    posts = relationship("BlogPost", back_populates="author")

    comments = relationship("Comment", back_populates="comment_author")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    post_id = Column(Integer, ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


# USEFUL FUNCTIONS
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.id == 1:
            return f(*args, **kwargs)
        return abort(403)

    return decorated_function


db.create_all()


@app.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            flash('This email have already been signed up, try login instead.')
            return redirect(url_for('login', exist=user.email))

        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data, salt_length=8))
        login_user(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.args.get('exist')
    form = LoginForm(email=email) if email else LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            flash("Incorrect password!", 'error')
        else:
            flash("User with given email address does not exist.", 'error')
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    comments = requested_post.comments
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                body=form.body.data,
                author_id=current_user.id,
                post_id=post_id
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))
        else:
            flash('You need to login or register to comment.')
            return redirect(url_for('login'))
    return render_template("post.html", comments=comments, form=form, post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data
        send_email(name, email, phone, message)
        return render_template(f"contact.html", msg_sent=True, form=form)
    return render_template("contact.html", form=form)


@app.route("/new-post", methods=['GET', 'POST'])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(

            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
