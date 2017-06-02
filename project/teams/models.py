from project import db

class Team(db.Model):

    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.Text, unique=True)
    name = db.Column(db.Text, unique=True)
    num_players = db.Column(db.Integer)

    def __init__(self, prefix, name, num_players):
        self.prefix = prefix
        self.name = name
        self.num_players = num_players
