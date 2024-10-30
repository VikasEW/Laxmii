from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TelField, SubmitField
from wtforms.validators import Email, DataRequired, Length
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'top-secret'
Bootstrap5(app)

class SignUpForm(FlaskForm):
    email = EmailField("Enter your email...", validators=[Email(), DataRequired()])
    first_name = StringField("Your first name...", validators=[DataRequired()])
    number = TelField('Phone Number', validators=[Length(11,11,'Enter a valid UK phone number')])
    submit = SubmitField('Join the waitlist')


@app.route('/', methods=['GET','POST'])
def index():

    form = SignUpForm()

    if form.validate_on_submit():
        pass

    return render_template('index.html', form=form)