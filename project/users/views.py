from flask import render_template, request, Blueprint, flash, redirect, url_for
from project.users.models import User
from project.users.forms import UserForm, LoginForm
from project import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required
import os
import requests
from sqlalchemy import func
from functools import wraps
import datetime

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash({'text': "Not Authorized", 'status': 'danger'})
            return redirect(url_for('root'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/')
def index():
    return render_template('users/index.html')

@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == 'POST':
        user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
        if user:
            flash({'text': "Username already use", 'status': 'danger'})
            return render_template('users/signup.html', form=form)
        if form.validate():
            try:
                payload = {'key': os.environ.get('API_KEY'), 'steamids': form.steamID.data}
                r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params=payload)
                p = r.json()
                if not p['response']['players']:
                    flash({'text': "Invalid steamID", 'status': 'danger'})
                    return render_template('users/signup.html', form=form)
                url = p['response']['players'][0]['avatarfull']
                new_user = User(
                    username = form.username.data,
                    email = form.email.data,
                    steamID = form.steamID.data,
                    password = form.password.data,
                    mmr=form.mmr.data
                )
                new_user.img_url = url
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            except IntegrityError as e:
                flash({'text': "Email, or steamID already use", 'status': 'danger'})
                return render_template('users/signup.html', form=form)
            flash({ 'text': "You have successfully signed up!", 'status': 'success' })
            return redirect(url_for('root'))
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            found_user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
            if found_user:
                is_authenticated = bcrypt.check_password_hash(found_user.password, form.password.data)
                if is_authenticated:
                    login_user(found_user)
                    flash({'text': "Hello, {}!".format(found_user.username), 'status': 'success'})
                    return redirect(url_for('root'))                 
    return render_template('users/login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash({ 'text': "You have successfully logged out.", 'status': 'success' })
    return redirect(url_for('users.login'))

@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
  return render_template('users/edit.html', form=UserForm(), user=User.query.get(id))

@users_blueprint.route('/<int:id>')
@login_required
def show(id):
    found_user = User.query.get(id)
    payload = {'key': os.environ.get('API_KEY'), 'steamids': found_user.steamID}
    r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params=payload)
    dataJSON = r.json()
    last_online = datetime.date.fromtimestamp(int(dataJSON['response']['players'][0]['lastlogoff']))
    today = datetime.date.today()
    diff = today - last_online
    # .strftime('%d/%m/%Y')
    status = dataJSON['response']['players'][0]['personastate']
    if request.method == 'GET' or current_user.is_anonymous or current_user.get_id() != str(id):
        return render_template('users/show.html', user=found_user, data=dataJSON, diff=diff.days, last_online=last_online.strftime('%d/%m/%Y'), status=status)









