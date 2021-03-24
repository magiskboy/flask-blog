from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    name = StringField(
        label='Name',
        validators=[DataRequired(), Length(min=2, max=50)],
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()],
    )
    confirm_password = PasswordField(
        label='Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()],
    )
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')


class UpdateAccountForm(FlaskForm):
    name = StringField(
        label='Name',
        validators=[DataRequired(), Length(min=2, max=50)],
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
    )
    picture = FileField(
        label='Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])],
    )
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField(
        label='Title',
        validators=[DataRequired()],
    )
    content = TextAreaField(
        label='Content',
        validators=[DataRequired()],
    )
    submit = SubmitField(label='Post')
