import os
import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import sys
sys.path.append('api_smoke_test')
import config

TIMEOUT = 3.0  # Tells requests library to stop waiting for a response after a given number of seconds


def get_authorization_token(local=False):
    """
    Returns authorization token of API_USER.
    :param local: if True API runs on localhost and needs some parameters to be set
    :return: dict
    """
    if local:
        password = config.API_USER_LOCAL_PASS
    else:
        password = config.API_USER_PASS

    token = get_auth_token_of_user(config.API_USER, password, local)
    return token


def get_auth_token_of_user(email, password, local=False):
    if local:
        set_env_for_local_oauthlib()
        TOKEN_URL = config.token_local
    else:
        TOKEN_URL = config.token_staging
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=config.CLIENT_ID))
    token = oauth.fetch_token(
        token_url=TOKEN_URL, username=email, password=password,
        client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    return token


def get_protected_resource(endpoint, token):
    resp = _get_protected_resource(endpoint, config.CLIENT_ID, token)
    return resp


def _get_protected_resource(endpoint, client_id, token):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.get(endpoint, timeout=TIMEOUT)
        return resp
    except requests.exceptions.ReadTimeout:
        resp = requests.models.Response()
        resp.status_code = 408
        return resp


def create_protected_resource(endpoint, token, payload=None):
    if payload is None:
        payload = {}
    resp = _create_protected_resource(endpoint, config.CLIENT_ID, token, payload)
    return resp


def _create_protected_resource(endpoint, client_id, token, body):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.post(url=endpoint, json=body, timeout=TIMEOUT)
        return resp
    except requests.exceptions.ReadTimeout:
        resp = requests.models.Response()
        resp.status_code = 408
        return resp


def put_protected_resource(endpoint, token, payload=None):
    if payload is None:
        payload = {}
    resp = _put_protected_resource(endpoint, config.CLIENT_ID, token, payload)
    return resp


def _put_protected_resource(endpoint, client_id, token, body):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.put(url=endpoint, json=body, timeout=TIMEOUT)
        return resp
    except requests.exceptions.ReadTimeout:
        resp = requests.models.Response()
        resp.status_code = 408
        return resp


def delete_protected_resource(endpoint, token):
    try:
        client = OAuth2Session(config.CLIENT_ID, token=token)
        resp = client.delete(endpoint, timeout=TIMEOUT)
        return resp
    except requests.exceptions.ReadTimeout:
        resp = requests.models.Response()
        resp.status_code = 408
        return resp


def set_env_for_local_oauthlib():
    # This has to be set if you your API uses HTTP instead of HTTPS
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
