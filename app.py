from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from werkzeug.sansio.response import Response
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired
from flask_bootstrap import Bootstrap5
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from werkzeug.wrappers.response import Response
from werkzeug.exceptions import HTTPException

import os
from db import db, Users

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'top-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'app.db')
app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'doe'

Bootstrap5(app)
db.init_app(app)

basic_auth = BasicAuth(app)

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'} 
        ))


class MyAdminIndexView(AdminIndexView):
    
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated')
        else:
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class UserModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated')
        else:
            return True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())
    


admin = Admin(app, name='Administrator', index_view=MyAdminIndexView())
admin.add_view(UserModelView(Users,db.session))

with app.app_context():
    db.create_all()


class SignUpForm(FlaskForm):
    email = EmailField("Email", validators=[Email(), DataRequired()])
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField('Last Name')
    query = TextAreaField('Some features you would love to see on the app')
    submit = SubmitField('Join the waitlist')


@app.route('/', methods=['GET','POST'])
def index():

    form = SignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        user_exists = db.session.execute(db.select(Users).where(Users.email==email)).scalar()
        if user_exists:
            flash("User with these credentials already exists. Please check your inbox",'info')
            return redirect('/#signin')
        else:
            new_user = Users(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                query = form.query.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered. Please check your inbox for more details.','info')
            return redirect('/#signin')

    return render_template('index.html', form=form)

if __name__=='__main__':
    app.run('0.0.0.0')