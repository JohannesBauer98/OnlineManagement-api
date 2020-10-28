from app import app, db, login
from flask_login import UserMixin
import jwt
import time


from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader()
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_details = db.relationship('UserDetails', backref='user', )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
        except:
            return
        return User.query.get(data['id'])


class UserDetails(db.Model):
    __tablename__ = "user_details"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<UserDetails {}'.format(self.firstname, self.lastname)
