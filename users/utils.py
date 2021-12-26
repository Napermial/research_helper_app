from itertools import tee
from django.contrib.auth import authenticate
import json
from jwt import algorithms, get_unverified_header, decode
import requests
from os import environ
from .models import User


def pairwise(seq):
    """:returns the next iterator of the sequence"""
    a, b = tee(seq)
    next(b)
    return zip(a, b)


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = get_unverified_header(token)
    jwks = requests.get(''.join([environ.get("JWT_ISSUER"), '.well-known/jwks.json'])).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')
    return decode(token, public_key, audience=environ.get("API_IDENTIFIER"), issuer=environ.get("JWT_ISSUER"),
                  algorithms=['RS256'])


def get_user_from_token(decoded):
    user_name = jwt_get_username_from_payload_handler(decoded)
    user = User.objects.filter(username=user_name)
    if user.exists():
        return user.first()
    user = User.objects.create_user(username=user_name)
    user.save()
    return user
