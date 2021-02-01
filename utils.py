import json
import requests

TIMEOUT = 5.0  # Tells requests library to stop waiting for a response after a given number of seconds


def create_resource(endpoint, headers, payload):
    resp = requests.post(endpoint, headers=headers, json=payload)
    return resp


def put_resource(endpoint, headers, payload):
    resp = requests.put(endpoint, headers=headers, json=payload)
    return resp


def get_resource(endpoint):
    try:
        resp = requests.get(endpoint, timeout=TIMEOUT)
        return resp
    except requests.exceptions.ReadTimeout:
        resp = requests.models.Response()
        resp.status_code = 408
        return resp


def get_resource_data(endpoint):
    resp = get_resource(endpoint)
    check_response_status_code(resp.status_code, 200,
                               "get_resource_data() returned status code " + str(resp.status_code))
    data = json.loads(resp.content)
    return data


def delete_resource(endpoint):
    resp = requests.delete(endpoint)
    return resp


def check_response_status_code(status_code, expected_status_code, error_message):
    assert status_code == expected_status_code, error_message
