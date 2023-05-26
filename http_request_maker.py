from enum import Enum
import utils
import utils_auth as ua
import config

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
    def __init__(self, api_url, token=None, headrs=None):
        self._api_url = api_url
        self._auth_token = token
        self.headers = HEADERS if (headrs is None) else headrs
        self.failed_requests_list = []
        self.warning_requests_list = []

    def make_get_requests(self, request_list):
        self._make_requests(request_list, [200, 204, 400], HttpMethods.GET)

    def make_get_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [
                            200, 204, 400, 404], HttpMethods.GET)

    def make_get_requests_with_param_for_bugs(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [
                            200, 204, 404], HttpMethods.GET)

    def make_post_requests(self, request_list):
        self._make_requests(
            request_list, [200, 201, 202, 204, 400, 404], HttpMethods.POST)

    def make_post_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [
                            200, 201, 202, 204, 400, 404, 409], HttpMethods.POST)

    def make_put_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list, [
                            200, 204, 400, 404], HttpMethods.PUT)

    def make_delete_requests_with_parameters(self, requests_with_parameters_list):
        self._make_requests(requests_with_parameters_list,
                            [400, 404], HttpMethods.DELETE)

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
            elapsed_time = response.elapsed.total_seconds()
            print(' Duration: ' + str(elapsed_time))

            request_succeeded = (status_code in correct_statuses)
            if not request_succeeded:
                self.failed_requests_list.append(
                    http_method.value + ' ' + end_point + ', sc: ' + str(status_code))
                print('FAIL: ' + end_point +
                      ' request failed. Status code: ' + str(status_code))
                print('')
            else:
                if http_method == HttpMethods.GET:
                    self._add_to_warning_list_if_exceeded_warning_timeout(
                        elapsed_time, end_point)
                else:
                    self._add_to_warning_list_if_exceeded_warning_timeout_post(
                        elapsed_time, end_point, http_method)

    def _add_to_warning_list_if_exceeded_warning_timeout(self, elapsed_time, end_point):
        if elapsed_time > config.WARNING_TIMEOUT:
            self.warning_requests_list.append('GET ' + end_point)

    def _add_to_warning_list_if_exceeded_warning_timeout_post(
            self, elapsed_time, end_point, http_method):
        if elapsed_time > config.WARNING_TIMEOUT_POST:
            self.warning_requests_list.append(
                http_method.value + ' ' + end_point)

    def _send_get_request(self, end_point):
        if self._auth_token is None:
            response = utils.get_resource(
                self._api_url + end_point, headers=self.headers)
        else:
            response = ua.get_protected_resource(
                endpoint=self._api_url + end_point, token=self._auth_token,
                headers=self.headers)
        return response

    def _send_post_request(self, end_point):
        if self._auth_token is None:
            response = utils.create_resource(
                self._api_url + end_point, self.headers, payload={})
        else:
            response = ua.create_protected_resource(
                endpoint=self._api_url + end_point, token=self._auth_token)
        return response

    def _send_put_request(self, end_point):
        if self._auth_token is None:
            response = utils.put_resource(
                self._api_url + end_point, self.headers, payload={})
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
