"""Common string operations."""
import re
from unidecode import unidecode
from flask import abort, make_response, jsonify


_punctuation_regex = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delimitation=u'-'):
    """Return slug item by removing all text punctuation and replacing spaces with  '-'"""
    result = []
    for word in _punctuation_regex.split(text.lower()):
        result.extend(unidecode(word).split())
    return str(delimitation.join(result))


def is_empty(obj):
    return len(obj) == 0


def safe_fetch_content(request, name, fallback=None):
    """
        Check if the request object contains the desired object and enforce that the object
        is not empty.
    """

    obj = request.json.get(name)
    if obj is None:
        if not fallback:
            abort(make_response(jsonify(message='MISSING_{}'.format(name.upper())), 400))
        return fallback

    name = name.upper()

    if type(obj) is str:
        if obj.strip() == '':
            if not fallback:
                abort(make_response(jsonify(message='EMPTY_STRING_{}'.format(name)), 400))
            return fallback
    elif type(obj) is list:
        if len(obj) == 0:
            if not fallback:
                abort(make_response(jsonify(message='EMPTY_LIST_{}'.format(name)), 400))
            return fallback
    return obj
