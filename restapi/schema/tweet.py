"""Schema for Tweet."""
from marshmallow import Schema, fields, validate


class TweetCreate(Schema):
    """Create input."""
    body = fields.String(
        required=True,
        validate=validate.Length(max=140)
    )
