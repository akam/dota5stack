from project import db, bcrypt
from flask_login import UserMixin


LikersLikee = db.Table('likes',
                        db.Column('id',
                                    db.Integer,
                                    primary_key=True),
                        db.Column('likee_id',
                                    db.Integer,
                                    db.ForeignKey('users.id', ondelete="cascade")),
                        db.Column('liker_id',
                                    db.Integer,
                                    db.ForeignKey('users.id', ondelete="cascade")),
                        db.CheckConstraint('liker_id != likee_id', name="no_self_like"))

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
    likers = db.relationship("User",
                                secondary=LikersLikee,
                                primaryjoin=(LikersLikee.c.liker_id == id),
                                secondaryjoin=(LikersLikee.c.likee_id == id),
                                backref=db.backref('liking', lazy='dynamic'),
                                lazy='dynamic')

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

    def is_liked_by(self, user):
        return bool(self.likers.filter_by(id=user.id).first())

    def is_liking(self, user):
        return bool(self.liking.filter_by(id=user.id).first())