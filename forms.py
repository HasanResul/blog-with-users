from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[InputRequired()]
                        , render_kw={'style': 'margin-bottom: 20px'})
    subtitle = StringField("Subtitle", validators=[InputRequired()]
                           , render_kw={'style': 'margin-bottom: 20px'})
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()]
                          , render_kw={'style': 'margin-bottom: 20px'})
    body = CKEditorField("Blog Content", validators=[InputRequired()]
                         , render_kw={'style': 'margin-bottom: 20px'})
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name = StringField(label='Name: ', validators=[InputRequired()]
                       , render_kw={'style': 'margin-bottom: 20px'})
    email = StringField(label='Email: ', validators=[InputRequired(), Email()]
                        , render_kw={'style': 'margin-bottom: 20px'})
    password = PasswordField(label='Password: ', validators=[InputRequired(), Length(min=8)]
                             , render_kw={'style': 'margin-bottom: 20px'})
    submit = SubmitField(label="Sign Me Up !"
                         , render_kw={'style': 'margin-bottom: 20px'})


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()]
                        , render_kw={'style': 'margin-bottom: 20px'})
    password = PasswordField("Password", validators=[InputRequired()]
                             , render_kw={'style': 'margin-bottom: 20px'})
    submit = SubmitField("Let Me In!"
                         , render_kw={'style': 'margin-bottom: 20px'})


class CommentForm(FlaskForm):
    body = CKEditorField("Comment", validators=[InputRequired()]
                         , render_kw={'style': 'margin-bottom: 20px'})
    submit = SubmitField("Submit Comment"
                         , render_kw={'style': 'margin: 20px 0 20px;'})


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()]
                       , render_kw={'style': 'margin-bottom: 20px'})
    email = StringField(label='Email: ', validators=[InputRequired(), Email()]
                        , render_kw={'style': 'margin-bottom: 20px'})
    phone = StringField("Phone", validators=[InputRequired()]
                        , render_kw={'style': 'margin-bottom: 20px'})
    message = StringField("Message", validators=[InputRequired()],
                          render_kw={'style': 'height: 10ch; margin-bottom: 20px'})
    submit = SubmitField("Contact")
