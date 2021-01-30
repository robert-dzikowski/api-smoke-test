# Introduction 
This repo contains smoke test which tests all endpoints found in OpenAPI v.3 spec file (it wasn't tested with older versions of OpenAPI).
  
# Getting Started
Install Python 3.7.

To install packages globally (for all users),
run 'pip install -r requirements.txt' in project root directory.

# Run
If your API needs authorization fill config.py with appropriate values.

python api-smoke-test\smoke_test.py name_of_a_spec_file [--auth] [--localhost].

--auth smoke tests uses authorization to make API requests.
API for which this smoke test was written uses authorization so the smoke test isn't 
well tested for APIs which don't use authorization.

--localhost API is runing on a local machine. 
In my case local API uses HTTP instead of HTTPS, so you should adapt my code to your needs.
