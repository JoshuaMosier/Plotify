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

import pandas as pd
import csv
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
    token = startup.getAccessToken()
    if len(token) == 0:
        return redirect(url_for('index'))
    access_token = token[0]
    artists = plotify_data.get_top_genres(access_token)
    genres = [item[1] for item in artists][:10]
    username,prof_pic = plotify_data.get_username(access_token)
    stracks = plotify_data.get_top_tracks(access_token,'short_term')
    sartists = plotify_data.get_top_artists(access_token,'short_term')
    mtracks = plotify_data.get_top_tracks(access_token,'medium_term')
    martists = plotify_data.get_top_artists(access_token,'medium_term')
    ltracks = plotify_data.get_top_tracks(access_token,'long_term')
    lartists = plotify_data.get_top_artists(access_token,'long_term')
    years,count = plotify_data.get_track_data(access_token,'long_term')
    legend = 'Tracks by Year'
    return render_template('index.html',username=username,genres=genres,stracks=stracks,sartists=sartists,mtracks=mtracks,martists=martists,ltracks=ltracks,lartists=lartists,prof_pic=prof_pic,values=count, labels=years, legend=legend)

@app.route('/bubble')
def bubble():
    return render_template('bubble.html')

# app.py
@app.route('/test')
def test():
    token = startup.getAccessToken()
    if len(token) == 0:
        return redirect(url_for('index'))
    access_token = token[0]
    artists = plotify_data.get_top_genres(access_token)
    data = pd.DataFrame.from_records(artists)
    data.columns = ['id','name','count']
    return data.to_csv(index=False)

if __name__ == '__main__':
    app.run(debug=True)