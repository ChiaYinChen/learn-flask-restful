"""Tweet Database ORM models."""
from sqlalchemy import ForeignKey, func

from ..common.connection import db
from .base import Base


class Tweet(Base):
    """Table for tweet."""

    __tablename__ = 'tweet'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE')
    )
    body = db.Column(db.String(140))
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )

    def __repr__(self):
        return "user_id={}, tweet={}".format(
            self.user_id, self.body
        )

    def as_dict(self):
        t = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        t['created_at'] = t['created_at'].isoformat()
        return t
