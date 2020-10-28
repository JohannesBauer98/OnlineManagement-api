from app import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_details = db.relationship('UserDetails', backref='user', )

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserDetails(db.Model):
    __tablename__ = "user_details"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<UserDetails {}'.format(self.firstname, self.lastname)
