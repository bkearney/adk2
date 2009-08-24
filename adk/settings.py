import os
import yaml
from util import *

def load_settings():
    try:
        config_file = os.environ["ADK_SETTINGS"]
        settings = yaml.load(open(config_file, "r"))
        settings["config_file"] = config_file
        settings["appliance_file"] = os.environ["ADK_APPLIANCES"]
    except KeyError:
        raise ADKError("ADK_SETTINGS environment variable is not set")
        
    return settings
