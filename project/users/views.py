from flask import render_template, request, Blueprint, flash, redirect, url_for
from project.users.models import User
from project.users.forms import UserForm, LoginForm, EditForm, DeleteForm
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
    users = User.query.all()
    steamIDarray = [user.steamID for user in users]
    steamIDarray.sort()
    steamIDs = ",".join([str(ids) for ids in steamIDarray])
    payload = {'key': os.environ.get('API_KEY'), 'steamids': steamIDs}
    r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params=payload)
    p = r.json()
    players = p['response']['players']
    players.sort(key=lambda player: player['steamid'])
    l2p = []
    online = []
    away = []
    rest = []
    for i,v in enumerate(players):
        if players[i]['personastate'] == 1:
            online.append(users[i])
        elif players[i]['personastate'] == 6: 
            l2p.append(users[i])
        elif players[i]['personastate'] == 3:
            away.append(users[i])
        elif players[i]['personastate'] == 4:
            away.append(users[i])
        else:
            rest.append(users[i])
    return render_template('users/index.html', users=users, online=online, rest=rest, away=away, l2p=l2p)

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

                if not form.carry.data and not form.support2.data and not form.support1.data and not form.offlane.data and not form.mid.data:
                    flash({'text': "Please choose at least one position", 'status': 'danger'})
                    return render_template('users/signup.html', form=form)
                new_user = User(
                    username = form.username.data,
                    email = form.email.data,
                    steamID = form.steamID.data,
                    password = form.password.data,
                    mmr=form.mmr.data,
                    support2 = form.support2.data,
                    support1 = form.support1.data,
                    offlane = form.offlane.data,
                    mid = form.mid.data,
                    carry = form.carry.data
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
            flash({'text': "Incorrect username or password", 'status': 'warning'})                
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
    return render_template('users/edit.html', form=EditForm(), user=User.query.get(id))

@users_blueprint.route('/<int:id>/delete', methods=["GET", "DELETE"])
@login_required
@ensure_correct_user
def delete(id):
    found_user = User.query.get(id)
    form = DeleteForm(request.form)
    if request.method == b'DELETE':
        if form.validate():
            if bcrypt.check_password_hash(found_user.password, form.password.data):
                flash({ 'text': "You have successfully deleted '{}'".format(found_user.username), 'status': 'danger' })
                flash({ 'text': "Thank you for using our app!", 'status': 'success' })
                db.session.delete(found_user)
                db.session.commit()
                logout_user()
                return redirect(url_for('root'))
        flash({ 'text': "Wrong password, please try again.", 'status': 'danger'})    
    return render_template('users/delete.html', user=User.query.get(id), form=form)

@users_blueprint.route('/<int:id>', methods=['GET', 'PATCH'])
@login_required
def show(id):
    found_user = User.query.get(id)
    form = EditForm(request.form)
    if request.method == b'PATCH':
        if form.validate():
            if not form.carry.data and not form.support2.data and not form.support1.data and not form.offlane.data and not form.mid.data:
                flash({'text': "Please choose at least one position", 'status': 'danger'})
                return render_template('users/edit.html', form=form, user=found_user)
            if bcrypt.check_password_hash(found_user.password, form.password.data):
                found_user.username = form.username.data;
                found_user.email = form.email.data;
                found_user.steamID = form.steamID.data;
                found_user.support2 = form.support2.data;
                found_user.support1 = form.support1.data;
                found_user.carry = form.carry.data;
                found_user.mid = form.mid.data;
                found_user.offlane = form.offlane.data;
                found_user.mmr = form.mmr.data;
                found_user.discord = form.discord.data or None;
                db.session.add(found_user);
                db.session.commit();
                flash({ 'text': "Successfully updated profile!", 'status': 'success'})
                return redirect(url_for('users.show', id=id))
            flash({ 'text': "Wrong password, please try again.", 'status': 'danger'})
        return render_template('users/edit.html', form=form, user=found_user)
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


@users_blueprint.route('/<int:liker_id>/liker', methods=['POST', 'DELETE'])
@login_required
def liker(liker_id):
  liked = User.query.get(liker_id)
  if request.method == 'POST':
    current_user.liking.append(liked)
  else:
    current_user.liking.remove(liked)
  db.session.add(current_user)
  db.session.commit()
  return redirect(url_for('users.liking', id=current_user.id))

@users_blueprint.route('/<int:id>/liking', methods=['GET'])
@login_required
def liking(id):
    return render_template('users/liking.html', user=User.query.get(id), current_user=current_user)

@users_blueprint.route('/<int:id>/likers', methods=['GET'])
@login_required
def likers(id):
    return render_template('users/likers.html', user=User.query.get(id))  








