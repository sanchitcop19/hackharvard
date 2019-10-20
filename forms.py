from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, DecimalField, TextField, SelectField, BooleanField, RadioField, SubmitField
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
    age = DecimalField('age', validators=[DataRequired()])
    job = BooleanField('job')
    credit_amount = DecimalField('credit_amount', validators=[DataRequired()])
    duration = DecimalField('duration', validators=[DataRequired()])
    sex = SelectField('sex', choices=[('0', 'Female'), ('1', 'Male')])
    housing_own = BooleanField('housing_own')
    housing_rent = BooleanField('housing_rent')
    savings_moderate = BooleanField('savings_moderate')
    savings_quite_rich = BooleanField('savings_quite_rich')
    savings_rich = BooleanField('savings_rich')
    check_moderate = BooleanField('check_moderate')
    check_rich = BooleanField('check_rich')
    income = DecimalField('income', validators=[DataRequired()])
    rent = DecimalField('rent', validators=[DataRequired()])
    goal = DecimalField('goal', validators=[DataRequired()])
    country_from = CountryOriginSelectField('country_from', validators=[DataRequired()])
    country_to = CountryDestinationSelectField('country_to', validators=[DataRequired()])
    submit = SubmitField('Register as a Lendee')

class InvestForm(FlaskForm):
    invest = SubmitField('Invest!')

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
