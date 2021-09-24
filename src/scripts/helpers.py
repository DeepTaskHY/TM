import os
import time
import json
import rospkg


# Constants
PACKAGE_PATH = rospkg.RosPack().get_path('tm')
CONFIGURATION_PATH = os.path.join(PACKAGE_PATH, 'configuration.json')


# Load configuration
with open(CONFIGURATION_PATH) as json_file:
    configuration = json.load(json_file)


def get_test_configuration(test_name: str) -> dict:
    return configuration['tests'][test_name]


# Timestamp string
def timestamp() -> str:
    return str(time.time())
