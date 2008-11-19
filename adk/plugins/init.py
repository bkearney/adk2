from adk.adkplugin import ADKPlugin
import os
import logging

class InitPlugin(ADKPlugin):
	def name(self):
		return "init"
		
	def run(self,appliance, settings):
		for directory in ["log_directory", "appliance_directory"]:
			if directory in settings:
				dir_value = settings[directory]
				if not os.path.isdir(dir_value):
					logging.info("Creating directory %s " % directory)
					os.makedirs(dir_value)
		
		
def get_plugin():
	return InitPlugin()
	
