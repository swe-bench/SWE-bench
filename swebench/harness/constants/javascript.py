# Constants - Commonly Used Commands
TEST_XVFB_PREFIX = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
XVFB_DEPS = [
    "python3", "python3-pip", "xvfb", "x11-xkb-utils", "xfonts-100dpi",
    "xfonts-75dpi", "xfonts-scalable", "xfonts-cyrillic", "x11-apps", "firefox"
]
X11_DEPS = [
    "libx11-xcb1", "libxcomposite1", "libxcursor1", "libxdamage1", "libxi6", 
    "libxtst6", "libnss3", "libcups2", "libxss1", "libxrandr2", "libasound2",
    "libatk1.0-0", "libgtk-3-0", "x11-utils",
]

# Constants - Task Instance Installation Environment
SPECS_CALYPSO = {
    **{k: {
        "apt-pkgs": ["libsass-dev", "sassc"],
        "install": ["npm install --unsafe-perm"],
        "test_cmd": "npm run test-client",
        "docker_specs": {
            "node_version": k,
        }
    } for k in [
        '0.8',
        '4.2.3', '4.3.0',
        '5.10.1', '5.11.1',
        '6.1.0', '6.7.0', '6.9.0', '6.9.1', '6.9.4', '6.10.0', '6.10.2', '6.10.3', '6.11.1', '6.11.2', '6.11.5',
        '8.9.1', '8.9.3', '8.9.4', '8.11.0', '8.11.2',
        '10.4.1', '10.5.0', '10.6.0', '10.9.0', '10.10.0', '10.12.0', '10.13.0', '10.14.0', '10.15.2', '10.16.3',
    ]}
}

TEST_CHART_JS_TEMPLATE = "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start {} --single-run --coverage --grep --auto-watch false"
SPECS_CHART_JS = {
    **{k: {
        "install": [
            "pnpm install",
            "pnpm run build",
        ],
        "test_cmd": [
            "pnpm install",
            "pnpm run build",
            f"{TEST_XVFB_PREFIX} su chromeuser -c \"{TEST_CHART_JS_TEMPLATE.format('./karma.conf.cjs')}\""
        ],
        "docker_specs": {
            "node_version": "21.6.2",
            "pnpm_version": "7.9.0",
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            }
        },
    } for k in ['4.0', '4.1', '4.2', '4.3', '4.4']},
    **{k: {
        "install": ["npm install"],
        "test_cmd": [
            "npm install",
            "npm run build",
            f"{TEST_XVFB_PREFIX} su chromeuser -c \"{TEST_CHART_JS_TEMPLATE.format('./karma.conf.js')}\""
        ],
        "docker_specs": {
            "node_version": "21.6.2",
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            }
        }
    } for k in ['3.0', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8']},
    **{k: {
        "install": [
            "npm install",
            "npm install -g gulp-cli"
        ],
        "test_cmd": [
            "npm install",
            "gulp build",
            TEST_XVFB_PREFIX + ' su chromeuser -c "gulp test"'
        ],
        "docker_specs": {
            "node_version": "21.6.2",
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            }
        }
    } for k in ['2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9']}
}
for v in SPECS_CHART_JS.keys():
    SPECS_CHART_JS[v]["apt-pkgs"] = XVFB_DEPS

SPECS_MARKED = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": "./node_modules/.bin/jasmine --no-color --config=jasmine.json",
        "docker_specs": {
            "node_version": "12.22.12",
        }
    } for k in [
        '0.3', '0.5', '0.6', '0.7', '1.0', '1.1',
        '1.2', '2.0', '3.9', '4.0', '4.1', '5.0'
    ]}
}
for v in ['4.0', '4.1', '5.0']:
    SPECS_MARKED[v]["docker_specs"]["node_version"] = "20.16.0"

SPECS_P5_JS = {
    **{k: {
        "apt-pkgs": X11_DEPS,
        "install": [
            "npm install",
            "PUPPETEER_SKIP_CHROMIUM_DOWNLOAD='' node node_modules/puppeteer/install.js",
            "./node_modules/.bin/grunt yui",
        ],
        "test_cmd": (
            """sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js\n"""
            "stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force"
        ),
        "docker_specs": {
            "node_version": "14.17.3",
        }
    } for k in [
        "0.10", "0.2", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9",
        "1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7",
        "1.8", "1.9",
    ]
    },
}
for k in ['0.4', '0.5', '0.6',]:
    SPECS_P5_JS[k]["install"] = [
        "npm install",
        "./node_modules/.bin/grunt yui",
    ]

SPECS_REACT_PDF = {
    **{k: {
        "apt-pkgs": ["pkg-config", "build-essential", "libpixman-1-0", "libpixman-1-dev", "libcairo2-dev", "libpango1.0-dev",
                "libjpeg-dev", "libgif-dev", "librsvg2-dev"] + X11_DEPS,
        "install": [
            "npm i -g yarn",
            "yarn install"
        ],
        "test_cmd": 'NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color',
        "docker_specs": {
            "node_version": "18.20.4"
        }
    } for k in ['1.0', '1.1', '1.2', '2.0']}
}
for v in ['1.0', '1.1', '1.2']:
    SPECS_REACT_PDF[v]["docker_specs"]["node_version"] = "8.17.0"
    SPECS_REACT_PDF[v]["install"] = [
        "npm install",
        "npm install cheerio@1.0.0-rc.3"
    ]
    SPECS_REACT_PDF[v]["test_cmd"] = "./node_modules/.bin/jest --no-color"

MAP_REPO_VERSION_TO_SPECS_JS = {
    "Automattic/wp-calypso": SPECS_CALYPSO,
    "chartjs/Chart.js": SPECS_CHART_JS,
    "markedjs/marked": SPECS_MARKED,
    "processing/p5.js": SPECS_P5_JS,
    "diegomura/react-pdf": SPECS_REACT_PDF,
}

# Constants - Repository Specific Installation Instructions
MAP_REPO_TO_INSTALL_JS = {}
