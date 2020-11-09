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


def safe_fetch_content(request, name):
    """
        Check if the request object contains the desired object and enforce that the object
        is not empty.
    """

    obj = request.json.get(name, default=None)
    if not obj:
        abort(make_response(jsonify(message='MISSING_{}'.format(name.upper())), 400))

    name = name.upper()

    if type(obj) is str:
        if obj.strip() == '':
            abort(make_response(jsonify(message='EMPTY_STRING_{}'.format(name)), 400))
    elif type(obj) is list:
        if len(obj) == 0:
            abort(make_response(jsonify(message='EMPTY_LIST_{}'.format(name)), 400))
    return obj
