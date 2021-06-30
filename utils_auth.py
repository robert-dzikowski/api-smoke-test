import datetime
import os
import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import api_smoke_test.config as config


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
    try:
        token = oauth.fetch_token(
            token_url=TOKEN_URL, username=email, password=password,
            client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    except Exception as e:
        print('Fetching token caused exception, type: ' + str(type(e)))
        print(str(e))
        raise
    return token


def get_protected_resource(endpoint, token):
    resp = _get_protected_resource(endpoint, config.CLIENT_ID, token)
    return resp


def _get_protected_resource(endpoint, client_id, token, get_timeout=config.TIMEOUT):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.get(endpoint, timeout=get_timeout)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _create_error_response(get_timeout)
        return error_resp


def create_protected_resource(endpoint, token, payload=None):
    if payload is None:
        payload = {}
    resp = _create_protected_resource(endpoint, config.CLIENT_ID, token, payload)
    return resp


def _create_protected_resource(endpoint, client_id, token, body, post_timeout=config.TIMEOUT_POST):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.post(url=endpoint, json=body, timeout=post_timeout)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _create_error_response(post_timeout)
        return error_resp


def put_protected_resource(endpoint, token, payload=None):
    if payload is None:
        payload = {}
    resp = _put_protected_resource(endpoint, config.CLIENT_ID, token, payload)
    return resp


def _put_protected_resource(endpoint, client_id, token, body, put_timeout=config.TIMEOUT_POST):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.put(url=endpoint, json=body, timeout=put_timeout)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _create_error_response(put_timeout)
        return error_resp


def patch_protected_resource(endpoint, token):
    resp = _patch_protected_resource(endpoint, config.CLIENT_ID, token)
    return resp


def _patch_protected_resource(endpoint, client_id, token, patch_timeout=config.TIMEOUT_POST):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.patch(url=endpoint, timeout=patch_timeout)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _create_error_response(patch_timeout)
        return error_resp


def delete_protected_resource(endpoint, token, delete_timeout=config.TIMEOUT_POST):
    try:
        client = OAuth2Session(config.CLIENT_ID, token=token)
        resp = client.delete(endpoint, timeout=delete_timeout)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _create_error_response(delete_timeout)
        return error_resp


def set_env_for_local_oauthlib():
    # This has to be set if you your API uses HTTP instead of HTTPS
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def _create_error_response(timeout):
    error_resp = _create_408_response()
    error_resp = _set_elapsed_time_in_response(error_resp, timeout)
    return error_resp


def _create_408_response():
    resp = requests.models.Response()
    resp.status_code = 408
    resp._content = '{"errors":"requests.exceptions.Timeout"}'
    return resp


def _set_elapsed_time_in_response(response, timeout):
    response.elapsed = datetime.timedelta(seconds=timeout)
    return response
