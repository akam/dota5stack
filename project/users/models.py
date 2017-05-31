from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    steamID = db.Column(db.Text, unique=True)
    mmr = db.Column(db.Text)
    img_url = db.Column(db.Text, unique=True)
    discord = db.Column(db.Text, unique=True)
    carry = db.Column(db.Boolean)
    support1 = db.Column(db.Boolean)
    support2 = db.Column(db.Boolean)
    offlane = db.Column(db.Boolean)
    mid = db.Column(db.Boolean)
    password = db.Column(db.Text)

    def __init__(self, username, email, steamID, password, mmr, support2, support1, offlane, mid, carry):
        self.username = username
        self.email = email
        self.steamID = steamID
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.mmr = mmr
        self.carry = carry
        self.support1 = support1
        self.support2 = support2
        self.offlane = offlane
        self.mid = mid


    def __repr__(self):
        return "#{}: username: {} - email: {}".format(self.id, self.email, self.username)

