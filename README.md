# Introduction 
This repo contains smoke test which tests all endpoints found in OpenAPI v.3 spec file (it wasn't tested with older versions of OpenAPI). 
It was tested with Spotify API (https://github.com/sonallux/spotify-web-api).
  
# Getting Started
Install Python 3.9 or newer.

To install packages globally (for all users),
run 'pip install -r requirements.txt' in project root directory.

# Run
python api-smoke-test\smoke_test.py name_of_a_spec_file [--auth] [--localhost]

or

python api-smoke-test\smoke_test.py url_of_a_spec_file [--auth] [--localhost]

If your API needs authorization fill config.py with appropriate values.

--auth smoke tests uses authorization to make API requests.

--localhost API is runing on a local machine. 
In my case local API uses HTTP instead of HTTPS, so you should adapt my code to your needs.

# TODO
Add ability to select authorization method: 
- client id and secret (default, used by Spotify API)
- client id, secret, user name and password
