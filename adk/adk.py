import appliance as Appliance
import settings as Settings
import debug
import logging
import optparse
import os
import sys

class ADK:
	
	def __init__(self):
		self.load_plugins()
		self.settings = Settings.load_settings()
		self.settings["adk"] = self
		
	def load_plugins(self):
		# TODO: Make this dynamic
		plugin_list = ["appcreator", "cobbler", "ec2", "init", "list", "gather", "srciso"]
		self.plugins={}
		for plug in plugin_list:
			logging.debug("Loading plugin: %s " % plug)
			plugin_module = __import__("plugins.%s" % (plug), globals(), locals(), [plug])
			new_plugin = plugin_module.get_plugin()
			self.plugins[new_plugin.name()]= new_plugin
		
		
	def process_chain(self, plugin_name, chain=[]):
		plugin = self.plugins[plugin_name]
		if plugin not in chain:
			#check to see if any of my dependencies are already in there
			position = 0
			for dep in plugin.dependencies():
				dep = self.plugins[dep]
				if dep in chain:
					dep_position = chain.index(dep) + 1
					if dep_position > position:
						position = dep_position 
			chain.insert(position, plugin)	
			
			#Now add the dependencies
			for dep in plugin.dependencies():
				self.process_chain(dep, chain)			
				
		return chain
		
	def build(self, target, appliance):
		build_chain = self.process_chain(target)
		
		if logging.getLogger().isEnabledFor(logging.INFO):
			msg = "Execution Chain is : ["
			
			cnt = 0
			for item in build_chain:	
				if cnt != 0:
					msg += " => "
				cnt += 1						
				msg += ("%s" % str(item))
			msg += "]"
				
			logging.info(msg)
					
		for plugin in build_chain:
			if plugin.needs_to_run():
				logging.info("Executing %s" % plugin.name())
				plugin.run(appliance, self.settings)
			else:
				logging.info("Skipping %s" % plugin.name())
		
	
def parse_options(args):
	usage = "Usage: %prog [options] PLUGIN APPLIANCE \n\n\
    Where PLUGIN can be seen by calling 'adk list plugins' \n\
    and APPLIANCE can be seen by calling 'adk list appliances'"

	parser = optparse.OptionParser(usage=usage)
	debug.setup_logging(parser)
	(options, args) = parser.parse_args()
    	
	return options, args
		
def main():
	"""
	Command Line entry
	"""	
	
	if os.geteuid() != 0:
		print >> sys.stderr, "You must run the adk as root"
		return 1
			
	adk = ADK()
	args = sys.argv
	options, args = parse_options(args)	
	cmd = args[0]	
	logging.debug("Plugin: %s" % cmd)
	appl = None
	if len(args) > 1:
		logging.debug("Appliance: %s" % cmd)		
		appl = args[1]
	adk.build(cmd, appl)


if __name__ == "__main__":
    sys.exit(main())
