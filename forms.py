from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, DecimalField, TextField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.

class RegisterLendeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    income = DecimalField('income', validators=[DataRequired()])
    rent = DecimalField('rent', validators=[DataRequired()])
    goal = DecimalField('goal', validators=[DataRequired()])


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
