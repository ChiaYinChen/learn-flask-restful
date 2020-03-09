"""Util function."""
from flask_restful import reqparse


def user_parser():
    """User argument parsing."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'password',
        type=min_length_str(5),
        required=True,
        help='{error_msg}'
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='required email'
    )
    return parser


def tweet_parser():
    """Tweet argument parsing."""
    parser = reqparse.RequestParser()
    parser.add_argument(
        'body',
        type=str,
        required=True,
        help='required body'
    )
    return parser


def min_length_str(min_length):
    """Check password length."""
    def validate(s):
        if s is None:
            raise Exception('Password required.')
        if not isinstance(s, (int, str)):
            raise Exception('Password format error.')
        s = str(s)
        if len(s) >= min_length:
            return s
        raise Exception(
            f'String must be at least {min_length} characters long.'
        )
    return validate
