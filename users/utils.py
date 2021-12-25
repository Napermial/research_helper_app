from itertools import tee
from django.contrib.auth import authenticate
import json
import jwt
import requests
from os import environ


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
    header = jwt.get_unverified_header(token)
    jwks = requests.get(''.join([environ.get("JWT_ISSUER"), '/.well-known/jwks.json'])).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')
    return jwt.decode(token, public_key, audience=environ.get("API_IDENTIFIER"), issuer=environ.get("JWT_ISSUER"),
                      algorithms=['RS256'])
