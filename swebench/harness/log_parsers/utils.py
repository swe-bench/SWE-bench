import re
from swebench.harness.constants.constants import EvalType, FAIL_ONLY_REPOS
from swebench.harness.test_spec.test_spec import TestSpec


def ansi_escape(text: str) -> str:
    """
    Remove ANSI escape sequences from text
    """
    pattern = re.compile(
        r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])',
        re.VERBOSE,
    )
    return pattern.sub('', text)


def get_eval_type(test_spec: TestSpec) -> str:
    if test_spec.repo in FAIL_ONLY_REPOS:
        return EvalType.FAIL_ONLY
    return EvalType.PASS_AND_FAIL
