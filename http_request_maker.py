from enum import Enum
import utils
import utils_auth as ua

HEADERS = {
    'accept': '*/*',
    'Content-Type': 'application/json'
}


class HttpMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class HTTPRequestMaker:
    def __init__(self, api_url, token=None):
        self._api_url = api_url
        self._auth_token = token
        self.failed_requests_list = []

    def make_get_requests(self, request_list):
        self._make_requests(request_list, [200], HttpMethods.GET)

    def make_get_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [200, 400, 404], HttpMethods.GET)

    def make_get_requests_with_param_for_bugs(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [200, 404], HttpMethods.GET)

    def make_post_requests(self, request_list):
        self._make_requests(request_list, [200, 201, 204, 400], HttpMethods.POST)

    def make_post_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [200, 201, 204, 400, 404, 409], HttpMethods.POST)

    def make_put_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [204, 400, 404], HttpMethods.PUT)

    def make_delete_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [400, 404], HttpMethods.DELETE)

    def _make_requests(self, request_list, correct_statuses, http_method):
        for end_point in request_list:
            if http_method == HttpMethods.GET:
                print('Requesting GET ' + end_point, end="")
                response = self._send_get_request(end_point)
                status_code = response.status_code
            elif http_method == HttpMethods.POST:
                print('Requesting POST ' + end_point, end="")
                response = self._send_post_request(end_point)
                status_code = response.status_code
            elif http_method == HttpMethods.PUT:
                print('Requesting PUT ' + end_point, end="")
                response = self._send_put_request(end_point)
                status_code = response.status_code
            elif http_method == HttpMethods.DELETE:
                print('Requesting DELETE ' + end_point, end="")
                response = self._send_delete_request(end_point)
                status_code = response.status_code
            else:
                return
            print(' Duration: ' + str(response.elapsed.total_seconds()))

            request_succeeded = (status_code in correct_statuses)
            if not request_succeeded:
                self.failed_requests_list.append(
                    http_method.value + ' ' + end_point + ', sc: ' + str(status_code))
                print('FAIL: ' + end_point + ' request failed. Status code: ' + str(status_code))

    def _send_get_request(self, end_point):
        if self._auth_token is None:
            response = utils.get_resource(self._api_url + end_point)
        else:
            response = ua.get_protected_resource(
                endpoint=self._api_url + end_point, token=self._auth_token)
        return response

    def _send_post_request(self, end_point):
        if self._auth_token is None:
            response = utils.create_resource(self._api_url + end_point, HEADERS, payload={})
        else:
            response = ua.create_protected_resource(
                endpoint=self._api_url + end_point, token=self._auth_token)
        return response

    def _send_put_request(self, end_point):
        if self._auth_token is None:
            response = utils.put_resource(self._api_url + end_point, HEADERS, payload={})
        else:
            response = ua.put_protected_resource(
                endpoint=self._api_url + end_point, token=self._auth_token)
        return response

    def _send_delete_request(self, end_point):
        if self._auth_token is None:
            response = utils.delete_resource(self._api_url + end_point)
        else:
            response = ua.delete_protected_resource(
                endpoint=self._api_url + end_point, token=self._auth_token)
        return response
