from pathlib import Path
import json
import os
import pdb
import copy
from swebench.harness.log_parsers.python import parse_log_django


if __name__ == '__main__':
    # reproduce the log parsing of django_16950 with gold patch
    log_file_data = "tests/test_log_data/django_16950_log_output.txt"
    with open(log_file_data, 'r') as f:
        content = f.read()
    report = parse_log_django(content)
    print(report)

