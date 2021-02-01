# Introduction 
This repo contains smoke test which tests all endpoints found in OpenAPI v.3 spec file (it wasn't tested with older versions of OpenAPI). It was tested only with APIs that use authorization.
  
# Getting Started
Install Python 3.7.

To install packages globally (for all users),
run 'pip install -r requirements.txt' in project root directory.

# Run
python api-smoke-test\smoke_test.py name_of_a_spec_file [--auth] [--localhost]

If your API needs authorization fill config.py with appropriate values.

--auth smoke tests uses authorization to make API requests.

--localhost API is runing on a local machine. 
In my case local API uses HTTP instead of HTTPS, so you should adapt my code to your needs.
