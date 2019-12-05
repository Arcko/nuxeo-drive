from os import getenv


# The server URL against to run tests
NXDRIVE_TEST_NUXEO_URL = getenv("NXDRIVE_TEST_NUXEO_URL", "http://localhost:8080/nuxeo")

# The user having administrator rights
NXDRIVE_TEST_USERNAME = getenv("NXDRIVE_TEST_USERNAME", "Administrator")

# The password associated to the username
NXDRIVE_TEST_PASSWORD = getenv("NXDRIVE_TEST_PASSWORD", "Administrator")

# The remote path where to store data. Must exist before running tests.
WS_DIR = getenv("NXDRIVE_TEST_PATH", "/default-domain/workspaces")