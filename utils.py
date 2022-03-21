import json
import requests

TIMEOUT = 10.0  # Tells requests library to stop waiting for a response after a given number of seconds


def get_resource(endpoint, timeout=TIMEOUT, headers=None):
    tries = 0
    while tries < 2:
        try:
            tries += 1
            if headers is None:
                resp = requests.get(endpoint, timeout=timeout)
            else:
                resp = requests.get(endpoint, timeout=timeout, headers=headers)
            return resp
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            if tries >= 2:
                return create_408_response()

    return create_408_response()
# get_resource()


def create_408_response():
    resp = requests.models.Response()
    resp.status_code = 408
    return resp


def get_resource_data(endpoint):
    resp = get_resource(endpoint)
    check_response_status_code(resp.status_code, 200,
                               "get_resource_data() returned status code " + str(resp.status_code))
    data = json.loads(resp.content)
    return data


def get_resource_content_string(endpoint):
    resp = get_resource(endpoint)
    check_response_status_code(resp.status_code, 200,
                               "get_resource_content_string() returned Status Code " + str(resp.status_code))
    content = bytes.decode(resp.content)
    return content


def create_resource(endpoint, headers, payload):
    resp = requests.post(endpoint, headers=headers, json=payload)
    return resp


def put_resource(endpoint, headers, payload):
    resp = requests.put(endpoint, headers=headers, json=payload)
    return resp


def delete_resource(endpoint):
    resp = requests.delete(endpoint)
    return resp


def check_response_status_code(status_code, expected_status_code, error_message):
    assert status_code == expected_status_code, error_message
