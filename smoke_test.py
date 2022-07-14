import os
import sys

sys.path.insert(0, os.getcwd())
import datetime
import re
import yaml
import utils
import utils_auth as ua
from http_request_maker import HTTPRequestMaker
from my_print import MyPrint
from my_exceptions import TestFail
import config

AUTH_ARG = '--auth'
LOCAL_ARG = '--localhost'
REQUEST_PARAM_ARG = '--request-param='
ONLY_GET_METHODS_ARG = '--only-get'  # The smoke test will only test GET methods


def main():
    if len(sys.argv) < 2:
        print('Usage: python api-smoke-test\smoke_test.py name_of_the_spec_file '
              '[' + AUTH_ARG + '] [' + LOCAL_ARG + '] [' + REQUEST_PARAM_ARG +
              '] [' + ONLY_GET_METHODS_ARG + '] ')
        sys.exit(1)

    spec_file = sys.argv[1]
    if spec_file.startswith('http'):
        content = utils.get_resource_content_string(spec_file)
        spec = yaml.safe_load(content)
    else:
        spec = parse_spec_file(spec_file)
    base_api_url = spec['servers'][0]['url']
    paths_dict = spec['paths']

    print('')
    print('Testing ' + spec['info']['title'])
    print('')

    endpoints_list = return_list_of_parameterless_get_methods(paths_dict)
    endpoints_with_params = return_list_of_get_methods_with_parameters(paths_dict)

    if len(endpoints_list) == 0 and len(endpoints_with_params) == 0:
        raise TestFail('Spec file ' + spec_file + ' does not contain any GET methods.')

    if authorization_is_necessary():
        token = get_auth_token()
    else:
        token = None

    maker = HTTPRequestMaker(base_api_url, token)

    print('Testing GET methods')
    maker.make_get_requests(endpoints_list)

    req_param = get_request_param_arg()

    if len(endpoints_with_params) > 0:
        call_get_methods_with_parameters(endpoints_with_params, maker, req_param)

    if not only_make_get_requests():
        endpoints_list = return_list_of_parameterless_post_methods(paths_dict)
        if len(endpoints_list) > 0:
            print('')
            print('Testing POST methods')
            maker.make_post_requests(endpoints_list)

        endpoints_with_params = return_list_of_post_methods_with_parameters(paths_dict)
        if len(endpoints_with_params) > 0:
            new_list = replace_parameters_with(endpoints_with_params, req_param)
            maker.make_post_requests_with_parameters(new_list)

        endpoints_with_params = return_list_of_put_methods_with_parameters(paths_dict)
        if len(endpoints_with_params) > 0:
            new_list = replace_parameters_with(endpoints_with_params, req_param)
            print('')
            print('Testing PUT methods')
            maker.make_put_requests_with_parameters(new_list)

        endpoints_with_params = return_list_of_delete_methods_with_parameters(paths_dict)
        if len(endpoints_with_params) > 0:
            new_list = replace_parameters_with(endpoints_with_params, '13013013013013')
            print('')
            print('Testing DELETE methods')
            maker.make_delete_requests_with_parameters(new_list)
    # if not only_make_get_requests()

    print_test_results(maker, spec['info']['title'])

    # Exit with error code is needed by Azure to show test as failed
    if len(maker.failed_requests_list) > 0:
        sys.exit(1)

    if config.WARNING_FAIL and len(maker.warning_requests_list) > 0:
        sys.exit(1)
# main()


######################################## Support functions ########################################


def parse_spec_file(spec_file):
    # Load OpenAPI spec file and read yaml or json data
    with open(file=spec_file, encoding='utf-8') as f:
        content = f.read()
        spec = yaml.safe_load(content)
    return spec


def authorization_is_necessary():
    result = False
    for arg in sys.argv:
        if arg == AUTH_ARG:
            result = True
    return result


def only_make_get_requests():
    result = False
    for arg in sys.argv:
        if arg == ONLY_GET_METHODS_ARG:
            result = True
    return result


def get_request_param_arg():
    tenant_id = '1'
    for arg in sys.argv:
        if arg.startswith(REQUEST_PARAM_ARG):
            tenant_id = arg.split('=')[1]
    return tenant_id


def get_auth_token():
    localhost = False
    for arg in sys.argv:
        if arg == LOCAL_ARG:
            localhost = True

    if localhost:
        token = ua.get_authorization_token(local=True)
    else:
        token = ua.get_auth_token_secret()  # ua.get_authorization_token()
        token = token['access_token']
    return token


def return_list_of_parameterless_get_methods(paths):
    result = _return_list_of_parameterless_methods(paths, 'get')
    return result


def return_list_of_parameterless_post_methods(paths):
    result = _return_list_of_parameterless_methods(paths, 'post')
    return result


def _return_list_of_parameterless_methods(paths, method):
    result = []
    for key in paths:
        if '{' not in key and method in paths[key].keys():
            result.append(key)
    return result


def return_list_of_get_methods_with_parameters(paths):
    result = _return_list_of_methods_with_parameters(paths, 'get')
    return result


def return_list_of_post_methods_with_parameters(paths):
    result = _return_list_of_methods_with_parameters(paths, 'post')
    return result


def return_list_of_put_methods_with_parameters(paths):
    result = _return_list_of_methods_with_parameters(paths, 'put')
    return result


def return_list_of_delete_methods_with_parameters(paths):
    result = _return_list_of_methods_with_parameters(paths, 'delete')
    return result


def replace_parameters_with(endpoints_list, replacement):
    new_list = []
    for el in endpoints_list:
        new_list.append(re.sub('{[a-zA-Z]*}', replacement, el))
    return new_list


def call_get_methods_with_parameters(endpoints_with_params, maker, param):
    new_list = replace_parameters_with(endpoints_with_params, param)
    maker.make_get_requests_with_parameters(new_list)
    print('')
    print('Testing with non existing values of parameters:')
    new_list = replace_parameters_with(endpoints_with_params, '13013')
    maker.make_get_requests_with_parameters(new_list)


def print_test_results(maker, api_title):
    mp = MyPrint()
    print('')
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('Date: ' + date)
    print(api_title)
    timestamp = str(datetime.datetime.now()).replace(' ', 'T')
    header3 = '<system-out><![CDATA['

    if len(maker.failed_requests_list) > 0 or len(maker.warning_requests_list) > 0:
        header = '<testsuite errors="1" failures="0" skipped="0" tests="1" timestamp="' + timestamp + '">'
        header2 = '<testcase status="failed" name="' + api_title + '">'
        header21 = '<error message="Test failed"></error>'
        mp.append_result_str(header + header2 + header21 + header3)
        if len(maker.warning_requests_list) > 0:
            mp.my_print('')
            mp.my_print('REQUESTS WHICH EXCEEDED WARNING TIMEOUT:')
            for r in maker.warning_requests_list:
                mp.my_print(r)
            mp.my_print('')
            if len(maker.failed_requests_list) == 0:
                mp.my_print('*** Test result: Warning ***')
        if len(maker.failed_requests_list) > 0:
            mp.my_print('FAILED REQUESTS:')
            for r in maker.failed_requests_list:
                mp.my_print(r)
            mp.my_print('')
            mp.my_print('!!! TEST FAIL !!!')
    else:
        header = '<testsuite errors="0" failures="0" skipped="0" tests="1" timestamp="' + timestamp + '">'
        header2 = '<testcase status="passed" name="' + api_title + '">'
        mp.append_result_str(header + header2 + header3)
        mp.my_print('*** Test Pass ***')

    end = ']]></system-out></testcase></testsuite>'
    mp.append_result_str(end)
    filename = api_title.replace(" ", "_") + '_test_results.xml'
    mp.save_result_str_to_file(filename)
    print('')
    print('')
    print('')


def _return_list_of_methods_with_parameters(paths, method):
    result = []
    for key in paths:
        if '{' in key and method in paths[key].keys():
            result.append(key)
    return result


if __name__ == '__main__':
    main()
