from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, DecimalField, TextField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
import pycountry

# Set your classes here.
class CountryOriginSelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountryOriginSelectField, self).__init__(*args, **kwargs)
        self.choices = [(None, "Origin Country")] + [(country.alpha_2, country.name) for country in pycountry.countries]

class CountryDestinationSelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountryDestinationSelectField, self).__init__(*args, **kwargs)
        self.choices = [(None, "Destination Country")] + [(country.alpha_2, country.name) for country in pycountry.countries]

class RegisterLendeeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    income = DecimalField('income', validators=[DataRequired()])
    rent = DecimalField('rent', validators=[DataRequired()])
    goal = DecimalField('goal', validators=[DataRequired()])
    country_from = CountryOriginSelectField('country_from', validators=[DataRequired()])
    country_to = CountryDestinationSelectField('country_to', validators=[DataRequired()])


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
