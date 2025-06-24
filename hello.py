from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
# flask-WTF 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Flask-SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db object instantiated from the class SQLAlchemy
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

# 138-487-654

@app.route('/', methods=['GET', 'POST'])
def index():
    # form get & post
    """ name = None """
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(f'Looks like you have changed your name!')
        session['name'] = form.name.data # The variable is now placed in the user session as session['name'] so that it is remembered beyond the request
        """ name = form.name.data
        form.name.data = '' """
        return redirect(url_for('index'))
    # return render_template('index.html', current_time=datetime.utcnow())
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
    """ render_template now obtains the name argument directly from the session 
    using session.get('name'). Using get() to request a dictionary key avoids 
    an exception for keys that aren’t found. The get() method returns a default 
    value of None for a missing key. """

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# flask - WFT
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Role and User model definition
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username