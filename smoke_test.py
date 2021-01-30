import re
import sys
import yaml
import utils_auth as ua
from http_request_maker import HTTPRequestMaker
from my_exceptions import TestFail

AUTH_ARG = '--auth'
LOCAL_ARG = '--localhost'


def main():
    if len(sys.argv) < 2:
        print('Usage: python smoke_test.py name_of_the_spec_file [' + AUTH_ARG + '] [' + LOCAL_ARG + ']')
        sys.exit(1)

    spec_file = sys.argv[1]
    spec = parse_spec_file(spec_file)
    base_api_url = spec['servers'][0]['url']
    paths_dict = spec['paths']

    print('')
    print('Testing ' + spec['info']['title'])
    print('')

    endpoints_list = return_list_of_parameterless_get_methods(paths_dict)

    if len(endpoints_list) == 0:
        raise TestFail('Spec file ' + spec_file + ' does not contain any GET methods.')

    if authorization_is_necessary():
        token = get_auth_token()
    else:
        token = None

    maker = HTTPRequestMaker(base_api_url, token)

    print('Testing GET methods')
    maker.make_get_requests(endpoints_list)

    endpoints_with_params = return_list_of_get_methods_with_parameters(paths_dict)
    if len(endpoints_with_params) > 0:
        call_get_methods_with_parameters(endpoints_with_params, maker)

    endpoints_list = return_list_of_parameterless_post_methods(paths_dict)
    if len(endpoints_list) > 0:
        print('')
        print('Testing POST methods')
        maker.make_post_requests(endpoints_list)

    endpoints_with_params = return_list_of_post_methods_with_parameters(paths_dict)
    if len(endpoints_with_params) > 0:
        new_list = replace_parameters_with(endpoints_with_params, '1')
        maker.make_post_requests_with_parameters(new_list)

    endpoints_with_params = return_list_of_put_methods_with_parameters(paths_dict)
    if len(endpoints_with_params) > 0:
        new_list = replace_parameters_with(endpoints_with_params, '1')
        print('')
        print('Testing PUT methods')
        maker.make_put_requests_with_parameters(new_list)

    endpoints_with_params = return_list_of_delete_methods_with_parameters(paths_dict)
    if len(endpoints_with_params) > 0:
        new_list = replace_parameters_with(endpoints_with_params, '13013013013013')
        print('')
        print('Testing DELETE methods')
        maker.make_delete_requests_with_parameters(new_list)

    print_test_results(maker)
# main()


######################################## Support functions ########################################


def parse_spec_file(spec_file):
    # Load OpenAPI spec file and read yaml or json data
    with open(spec_file) as f:
        spec = yaml.safe_load(f.read())
    return spec


def authorization_is_necessary():
    result = False
    for arg in sys.argv:
        if arg == AUTH_ARG:
            result = True
    return result


def get_auth_token():
    localhost = False
    for arg in sys.argv:
        if arg == LOCAL_ARG:
            localhost = True

    if localhost:
        token = ua.get_authorization_token(local=True)
    else:
        token = ua.get_authorization_token()
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


def call_get_methods_with_parameters(endpoints_with_params, maker):
    new_list = replace_parameters_with(endpoints_with_params, '1')
    maker.make_get_requests_with_parameters(new_list)
    print('')
    print('Testing with non existing values of parameters:')
    new_list = replace_parameters_with(endpoints_with_params, '13013')
    maker.make_get_requests_with_parameters(new_list)


def print_test_results(maker):
    print('')
    if len(maker.failed_requests_list) > 0:
        print('FAILED REQUESTS:')
        for r in maker.failed_requests_list:
            print(r)
        print('')
        print('*** TEST FAIL ***')
    else:
        print('*** Test Pass ***')
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
