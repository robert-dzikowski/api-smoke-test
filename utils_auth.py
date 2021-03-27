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

    # web_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2MTQ5NzcwMjQsImV4cCI6MTYxNDk4MDYyNCwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5tYXBsZWxlYWYuYW5vdmEuZGV2IiwiYXVkIjpbInBlcm1pc3Npb25zLWFwaSIsInRlbmFudG1hbmFnZXItYXBpIiwidHJhbnNmb3JtZmlsZWltcG9ydGVyLWFwaSIsImRldmljZXMtYXBpIiwiYXNzZXRzLWFwaSJdLCJjbGllbnRfaWQiOiJtYXBsZS1sZWFmLXdlYi1hcHAiLCJzdWIiOiI4YjI3YjA5ZS0wOTI3LTQ3OWQtODFjZS0yZWVkMmQxMmVhNzYiLCJhdXRoX3RpbWUiOjE2MTQ5Njg1NjEsImlkcCI6ImxvY2FsIiwicm9sZSI6WyJEaWdpdGFsaXphdGlvbi5TdXBwb3J0IiwiRGlzdHJpYnV0b3IuVXNlciIsIlRlbGVtZXRyeU9wZXJhdGlvbnMuU3VwcG9ydCIsIlRlbGVtZXRyeVNlcnZpY2UtTWFpbnRlbmFuY2UuU3VwcG9ydCIsIlRyYW5zZm9ybS5Db25zdWx0YW50Il0sInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJwZXJtaXNzaW9ucy1hcGkiLCJ0ZW5hbnRtYW5hZ2VyLWFwaSIsInRyYW5zZm9ybWZpbGVpbXBvcnRlci1hcGkiLCJkZXZpY2VzLWFwaSIsImFzc2V0cy1hcGkiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl19.BI_hNro9U-fyMxQpmO79TVTqDKq3FR_GJf5_se3fqZOl8kcBSEcGFzWbEwKj9Z9dGB0b7rAK3-ctjNB6Re5ETLYIMMNKtp13LpECDoyAkAW_qXyVhDFXc_lRXytyfW0nyH5dgUBNwqBbJE_rGvTUc6gQG2gfDIZ6SIpxAgV9cEe-pRyMylu18JvK_I0kkEnC8sB667VuPsBofH61R69RnVCggFz9icj6iVFXxXFl0CoUQnN39bohvuUss_vit7NCG-FHH_CntZ4VMf_tx3qvo0Na4bBESFnw9iUhFQW4tfHID5AznRBRn14Sq6IEJlKgUL3JVqcHI4nRN3MXpc1O5w'
    # token = {'access_token': web_token, 'expires_in': 3600, 'token_type': 'Bearer', 'scope': ['assets-api', 'devices-api', 'digitalization-api', 'openid', 'permissions-api', 'profile', 'roles', 'tenantmanager-api', 'transformfileimporter-api', 'usermanagement-api']}  # , 'expires_at': 1614950149.8913505}
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
        resp = client.get(endpoint, timeout=config.TIMEOUT)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _set_408_in_the_response()
        return error_resp


def create_protected_resource(endpoint, token, payload=None):
    if payload is None:
        payload = {}
    resp = _create_protected_resource(endpoint, config.CLIENT_ID, token, payload)
    return resp


def _create_protected_resource(endpoint, client_id, token, body):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.post(url=endpoint, json=body, timeout=config.TIMEOUT_POST)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _set_408_in_the_response()
        return error_resp


def put_protected_resource(endpoint, token, payload=None):
    if payload is None:
        payload = {}
    resp = _put_protected_resource(endpoint, config.CLIENT_ID, token, payload)
    return resp


def _put_protected_resource(endpoint, client_id, token, body):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.put(url=endpoint, json=body, timeout=config.TIMEOUT_POST)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _set_408_in_the_response()
        return error_resp


def patch_protected_resource(endpoint, token):
    resp = _patch_protected_resource(endpoint, config.CLIENT_ID, token)
    return resp


def _patch_protected_resource(endpoint, client_id, token):
    try:
        client = OAuth2Session(client_id, token=token)
        resp = client.patch(url=endpoint, timeout=config.TIMEOUT_POST)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _set_408_in_the_response()
        return error_resp


def delete_protected_resource(endpoint, token):
    try:
        client = OAuth2Session(config.CLIENT_ID, token=token)
        resp = client.delete(endpoint, timeout=config.TIMEOUT_POST)
        return resp
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        error_resp = _set_408_in_the_response()
        return error_resp


def set_env_for_local_oauthlib():
    # This has to be set if you your API uses HTTP instead of HTTPS
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def _set_408_in_the_response():
    resp = requests.models.Response()
    resp.status_code = 408
    return resp
