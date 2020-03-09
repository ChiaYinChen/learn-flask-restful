"""User Database ORM models."""
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ..common.connection import db
from .base import Base


class User(Base):
    """Table for user."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)

    tweet = relationship('Tweet')

    def __repr__(self):
        return "id={}, username={}".format(
            self.id, self.username
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_all_user(cls):
        return cls.query.all()

    @staticmethod
    def authenticate(username, password):
        user = User.get_by_username(username)
        if user:
            # check password
            if user.check_password(password):
                return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        user = User.get_by_id(user_id)
        return user
