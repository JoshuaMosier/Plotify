from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, redirect, jsonify
from flask_wtf import Form
from passlib.hash import sha256_crypt
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from operator import itemgetter

import os
import plotify_data
app = Flask(__name__)

#SQAlchemy Configurations
app.config['SECRET_KEY'] = 'secret123'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask import Flask, redirect, request
import startup

@app.route('/')
def index():
    response = startup.getUser()
    return redirect(response)

@app.route('/callback/')
def callback():
    startup.getUserToken(request.args['code'])
    return redirect(url_for('main'))

@app.route('/main')
def main():
    response = startup.getUser()
    token = res = startup.getAccessToken()
    username = plotify_data.get_username(token[0])
    return render_template('index.html',test=token,test2=startup.getUser(),test3=username)

if __name__ == '__main__':
    app.run(debug=True)