from swebench.harness.test_spec.common import make_env_script_list_common, make_eval_script_list_common, make_repo_script_list_common


# MARK: Script Creation Functions

def make_repo_script_list_php(specs, repo, repo_directory, base_commit, env_name) -> list:
    return make_repo_script_list_common(specs, repo, repo_directory, base_commit, env_name)


def make_env_script_list_php(instance, specs, env_name) -> list:
    return make_env_script_list_common(instance, specs, env_name)


def make_eval_script_list_php(instance, specs, env_name, repo_directory, base_commit, test_patch) -> list:
    return make_eval_script_list_common(instance, specs, env_name, repo_directory, base_commit, test_patch)
