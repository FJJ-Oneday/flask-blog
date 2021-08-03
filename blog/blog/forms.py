from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email
from flask_ckeditor import CKEditorField

from .models import Category


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField('login')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 255)])
    submit = SubmitField('register')


class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    comment_root = HiddenField('is_root')
    post_id = HiddenField('post_id')
    submit = SubmitField()


class PostForm(FlaskForm):

    title = StringField('title')
    body = CKEditorField('body')
    category = SelectField('category', default=1, coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.all()]