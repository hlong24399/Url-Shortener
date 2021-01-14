from flask import Flask, redirect, url_for, flash, render_template, request, session
from .config import Config
from .models import db, ShortUrl
from .cli import create_db
import datetime
import math as m
from collections import deque
import numpy as np
from sqlalchemy.exc import IntegrityError
from authlib.integrations.flask_client import OAuth

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

#set up flask
app = Flask(__name__)
app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)


#set up oauth
oauth = OAuth(app)
oauth.register(name ='google', server_metadata_url=CONF_URL, client_kwargs={'scope': 'openid email profile'})

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    redirect_url = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_url)

#authentication
@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    return redirect('/home')

#display home page
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

#display list page
@app.route('/list', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        if request.form['tpl_do'] == 'My SHORT url':
            queried_data = ShortUrl.query.all()
            return render_template('list.html', tplt_url = queried_data)
    else:
        queried_data = ShortUrl.query.all()
        return render_template('list.html', tplt_url = queried_data)

ALPHABET_62= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def urlshortener(ENCODED):
        out_64 = deque()
        next = int(ENCODED)
        while (next > 0):
            quotient = m.floor(next/62)
            remainder = next if quotient == 0 else next % 62
            out_64.appendleft(ALPHABET_62[remainder])
            next = quotient
        return ''.join(i for i in out_64)

def originalurl(KEY):
        x = KEY
        ar = np.arange(0,len(str(x)))[::-1]
        s = list(zip(x,ar))
        out_10 = sum(ALPHABET_62.index(i)*m.pow(62,j) for i,j in s )
        return out_10

@app.route('/shortening', methods=['GET', 'POST'])
def shortening():
    o_url_raw = str()
    if request.method == 'POST':
        temp = request.form['tplt_url']
        o_url_raw = temp
    temp_new_url = ShortUrl(original_url=o_url_raw, short_url=o_url_raw+"dummy",
    created_at=datetime.datetime.now())
    try:
        db.session.add(temp_new_url)
        db.session.commit()
    except IntegrityError:
        flash("Not able to add this due to some reason.")
        return redirect(url_for('home'))
    x = ShortUrl.query.order_by(-ShortUrl.id).first()
    x.short_url = urlshortener(x.id)
    db.session.commit()
    return render_template('show.html', tplt_short=x.short_url)

@app.route('/find/<shortcode>')
def searchURL(shortcode):
    p_key = originalurl(shortcode)
    found_user = ShortUrl.query.get(int(p_key))
    if found_user is None:
        flash("There is currently no record associated with that short url.")
        return redirect(url_for('home'))
    else:
        return render_template('search.html', tplt_original_url = found_user.original_url)

@app.route('/f', methods=['GET', 'POST'])
def searchURL_onscreen():
    if request.method == 'POST':
        x = request.form['tplt_findurl']
        return redirect(url_for('searchURL', shortcode = x))
    else:
        return redirect(url_for('home'))

@app.route('/test')
def test():
    testing = ShortUrl(short_url="adfs", original_url="wow",
     created_at=datetime.datetime.now())
    db.session.add(testing)
    db.session.commit()
    return render_template('test.html', tplt_data = ShortUrl.query.all())

#delete the id when needed
@app.route('/delete/<id>')
def delete(id):
    rec = ShortUrl.query.get(int(id))
    if rec is None:
        flash("No record to delete")
        return redirect(url_for('home'))
    else:
        db.session.delete(rec)
        db.session.commit()
        return redirect(url_for('listing'))
