import json
import requests

TIMEOUT = 10.0  # Tells requests library to stop waiting for a response after given number of seconds


def get_resource(endpoint, timeout=TIMEOUT, headers=None, params=None):
    tries = 0
    while True:
        tries += 1
        try:
            resp = requests.get(endpoint, timeout=timeout,
                                headers=headers, params=params)
            return resp
        except (requests.exceptions.Timeout) as e:
            if tries >= 3:
                return create_408_response(
                    'requests library raised ' + type(e).__name__ + ' exception.')
# get_resource()


def create_408_response(error_msg: str):
    resp = requests.models.Response()
    resp.status_code = 408
    resp.reason = error_msg
    return resp


def get_resource_data(endpoint: str) -> dict:
    resp = get_resource(endpoint)
    resp.raise_for_status()
    data = resp.json()
    return data


def get_resource_content_string(endpoint):
    resp = get_resource(endpoint)
    resp.raise_for_status()
    content = bytes.decode(resp.content)
    return content


def create_resource(endpoint, headers=None, payload={}):
    if headers is None:
        resp = requests.post(endpoint, json=payload)
    else:
        resp = requests.post(endpoint, headers=headers, json=payload)
    return resp


def put_resource(endpoint, headers, payload):
    resp = requests.put(endpoint, headers=headers, json=payload)
    return resp


def delete_resource(endpoint):
    resp = requests.delete(endpoint)
    return resp
