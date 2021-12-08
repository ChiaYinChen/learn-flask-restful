"""Schema for User."""
from marshmallow import Schema, fields, validate


class UserBase(Schema):
    """Base User schema."""
    username = fields.Str()
    email = fields.Str()


class UserCreate(UserBase):
    """Create input."""
    password = fields.String(
        required=True,
        validate=validate.Length(min=5, max=16)
    )


class User(UserBase):
    """Output."""
    pass
