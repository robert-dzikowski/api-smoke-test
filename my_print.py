import os
from pathlib import Path

RESULTS_DIR = os.getcwd() + os.path.sep + 'reports'


class MyPrint:
    def __init__(self):
        self._result_str = ""

    def my_print(self, msg):
        print(msg)
        self._result_str += msg + "\n"

    def save_result_str_to_file(self, filename):
        _create_test_results_dir(RESULTS_DIR)
        with open(RESULTS_DIR + os.path.sep + filename, 'w') as f:
            f.write(self._result_str)

    def append_result_str(self, string):
        self._result_str += string + "\n"


def _create_test_results_dir(dirname):
    Path(dirname).mkdir(exist_ok=True)
