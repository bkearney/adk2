import os
import yaml
from util import *

def load_settings():
    try:
        config_file = os.environ["ADK_SETTINGS"]
        settings = yaml.load(open(config_file))
        settings["config_file"] = config_file
    except KeyError:
        raise ADKError("ADK_SETTINGS environment variable is not set")
        
    return settings
