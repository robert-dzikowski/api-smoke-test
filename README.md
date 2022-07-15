# Introduction 
This repo contains smoke test which tests all endpoints found in OpenAPI v.3 spec file (it wasn't tested with older versions of OpenAPI). 
It was tested with Spotify API (https://github.com/sonallux/spotify-web-api).
  
# Getting Started
Install Python 3.9 or newer.

To install packages globally (for all users),
run 'pip install -r requirements.txt' in project root directory.

# Run
python api-smoke-test\smoke_test.py name_of_a_spec_file [--auth] [--localhost] [--only-get] [--request-param=] 

or

python api-smoke-test\smoke_test.py url_of_a_spec_file [--auth] ...

--auth Smoke test needs authorization to make API requests. Also you need to fill config.py with appropriate values.

--localhost API is runing on a local machine. 
In my case local API uses HTTP instead of HTTPS, so you should adapt my code to your needs.

--only-get Test only GET methods.

--request-param= Set value for requests parameters, 
e.g. if --request-param=7 then for /albums/{id} endpoint test will send request to /albums/7.


# TODO
Add ability to select authorization method: 
- client id and secret (default, used by Spotify API)
- client id and secret, user name and password
