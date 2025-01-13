import re

from pathlib import Path
from swebench.harness.constants import (
    END_TEST_OUTPUT,
    MAP_REPO_VERSION_TO_SPECS,
    START_TEST_OUTPUT,
    TEST_XVFB_PREFIX,
)
from swebench.harness.utils import get_modified_files
from unidiff import PatchSet


# MARK: Test Command Creation Functions
def get_test_cmds_calypso(instance) -> list:
    test_paths = [x.path for x in PatchSet(instance['test_patch'])]
    test_cmds = []
    for test_path in test_paths:
        if re.search(r"__snapshots__/(.*).js.snap$", test_path):
            # Jest snapshots are not run directly
            test_path = "/".join(test_path.split("/")[:-2])

        # Determine which testing script to use
        if any([test_path.startswith(x) for x in ["client", "packages"]]):
            pkg = test_path.split("/")[0]
            if instance['version'] in [
                '10.10.0', '10.12.0', '10.13.0',
                '10.14.0', '10.15.2', '10.16.3'
            ]:
                test_cmds.append(f"./node_modules/.bin/jest --verbose -c=test/{pkg}/jest.config.js '{test_path}'")
            elif instance['version'] in [
                '6.11.5', '8.9.1', '8.9.3', '8.9.4', '8.11.0', '8.11.2',
                '10.4.1', '10.5.0', '10.6.0', '10.9.0',
            ]:
                test_cmds.append(f"./node_modules/.bin/jest --verbose -c=test/{pkg}/jest.config.json '{test_path}'")
            else:
                test_cmds.append(f"npm run test-{pkg} --verbose '{test_path}'")
        elif any([test_path.startswith(x) for x in ["test/e2e"]]):
            test_cmds.extend([
                "cd test/e2e",
                f"NODE_CONFIG_ENV=test npm run test {test_path}",
                "cd ../..",
            ])

    return test_cmds


MAP_REPO_TO_TEST_CMDS = {
    "Automattic/wp-calypso": get_test_cmds_calypso,
}


def get_test_cmds(instance) -> list:
    if instance["repo"] in MAP_REPO_TO_TEST_CMDS:
        return MAP_REPO_TO_TEST_CMDS[instance["repo"]](instance)
    test_cmd = MAP_REPO_VERSION_TO_SPECS[instance["repo"]][instance["version"]]["test_cmd"]
    return [test_cmd] if isinstance(test_cmd, str) else test_cmd


# MARK: Utility Functions

def get_download_img_commands(instance) -> list:
    cmds = []
    for i in instance.get("image_assets", {}).get("test_patch", []):
        folder = Path(i["path"]).parent
        cmds.append(f"mkdir -p {folder}")
        cmds.append(f"curl -o {i['path']} {i['url']}")
        cmds.append(f"chmod 777 {i['path']}")
    return cmds


# MARK: Script Creation Functions

def make_repo_script_list_js(specs, repo, repo_directory, base_commit, env_name) -> list:
    """
    Create a list of bash commands to set up the repository for testing.
    This is the setup script for the instance image.
    """
    setup_commands = [
        f"git clone -o origin https://github.com/{repo} {repo_directory}",
        f"cd {repo_directory}",
        f"git reset --hard {base_commit}",
        f"chmod -R 777 {repo_directory}",  # So nonroot user can run tests
        # Remove the remote so the agent won't see newer commits.
        f"git remote remove origin",
    ]
    if "install" in specs:
        setup_commands.extend(specs["install"])
    return setup_commands


def make_env_script_list_js(instance, specs, env_name) -> list:
    """
    Creates the list of commands to set up the environment for testing.
    This is the setup script for the environment image.
    """
    reqs_commands = []
    if "apt-pkgs" in specs:
        reqs_commands += [
            "apt-get update",
            f"apt-get install -y {' '.join(specs['apt-pkgs'])}"
        ]
    return reqs_commands


def make_eval_script_list_js(instance, specs, env_name, repo_directory, base_commit, test_patch) -> list:
    """
    Applies the test patch and runs the tests.
    """
    HEREDOC_DELIMITER = "EOF_114329324912"
    test_files = get_modified_files(test_patch)
    # Reset test files to the state they should be in before the patch.
    if test_files:
        reset_tests_command = f"git checkout {base_commit} {' '.join(test_files)}"
    else:
        reset_tests_command = f'echo "No test files to reset"'
    
    apply_test_patch_command = (
        f"git apply --verbose --reject - <<'{HEREDOC_DELIMITER}'\n{test_patch}\n{HEREDOC_DELIMITER}"
    )
    test_commands = get_test_cmds(instance)
    eval_commands = [
        f"cd {repo_directory}",
        f"git config --global --add safe.directory {repo_directory}",  # for nonroot user
        f"cd {repo_directory}",
        # This is just informational, so we have a record
        # f"git status",
        # f"git show",
        # f"git -c core.fileMode=false diff {base_commit}",
        reset_tests_command,
        *get_download_img_commands(instance),
        apply_test_patch_command,
        f": '{START_TEST_OUTPUT}'",
        *test_commands,
        f": '{END_TEST_OUTPUT}'",
        reset_tests_command,
    ]
    return eval_commands
