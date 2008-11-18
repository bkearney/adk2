import os
import yaml

def load_settings():
	adk_home = os.environ["ADK_HOME"]
	config_file = os.path.join(adk_home, "adk.yml")
	settings = yaml.load(open(config_file))
	settings["adk_home"]= adk_home
	settings["config_file"] = config_file
	return settings
	
	
def load_appliances():
	adk_home = os.environ["ADK_HOME"]
	config_file = os.path.join(adk_home, "appliances.yml")
	return yaml.load(open(config_file))
