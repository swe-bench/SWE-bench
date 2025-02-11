# Constants - Task Instance Installation Environment
SPECS_PHPSPREADSHEET = {
    "4313": {
        "docker_specs": { "php_version": "8.3.16" },
        "base_docker_specs": { "php_version": "8.3.16" },
        "install": ["composer update", "composer install"],
        "test_cmd": [
            "./vendor/bin/phpunit --testdox --colors=never tests/PhpSpreadsheetTests/Writer/Ods/IndentTest.php"
        ],
    }
}

MAP_REPO_VERSION_TO_SPECS_PHP = {
    "phpoffice/phpspreadsheet": SPECS_PHPSPREADSHEET,
}

# Constants - Repository Specific Installation Instructions
MAP_REPO_TO_INSTALL_PHP = {}
