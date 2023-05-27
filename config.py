CLIENT_ID = ''
CLIENT_SECRET = ''
API_USER = ''
API_USER_PASS = ''

# Password of API_USER for localhost environment
API_USER_LOCAL_PASS = ''

# url of token endpoint used by oauthlib
token_staging = ''
token_local = ''

TIMEOUT = 10.0  # Tells requests library to stop waiting for a response after given number of seconds
TIMEOUT_POST = 20.0  # Timeout for POST requests
WARNING_TIMEOUT = 2.0
WARNING_TIMEOUT_POST = 4.0
WARNING_FAIL = False  # Fail test if warning timeouts were exceeded

# HTTPRequestMaker configuration.
# Allowed HTTP status codes.
# autopep8: off
GET_SC        = [200, 204, 400]
GET_SC_PARAMS = [200, 204, 400, 404]
POST_SC        = [200, 201, 202, 204, 400, 404]
POST_SC_PARAMS = [200, 201, 202, 204, 400, 404, 409]
PUT_SC_PARAMS = [200, 204, 400, 404]
DELETE_SC_PARAMS = [400, 404]
# autopep8: on
