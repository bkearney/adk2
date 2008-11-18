import appliance as Appliance
import settings as Settings
import sys

class ADK:
	
	def __init__(self):
		self.load_plugins()
		self.settings = Settings.load_settings()
		
	def load_plugins(self):
		# TODO: Make this dynamic
		plugin_list = ["appliance", "cobbler", "ec2", "init", "list", "gather", "srciso"]
		self.plugins={}
		for plug in plugin_list:
			plugin_module = __import__("plugins.%s" % (plug), globals(), locals(), [plug])
			new_plugin = plugin_module.get_plugin()
			self.plugins[new_plugin.plugin_name()]= new_plugin
		
		
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
		for plugin in build_chain:
			if plugin.needs_to_run():
				print("Executing %s" % plugin.plugin_name())
				plugin.run(appliance, self.settings)
			else:
				print("Skipping %s" % plugin.plugin_name())
		
	
def main():
	"""
	Command Line entry
	"""	
	adk = ADK()
	cmd = sys.argv[1]
	appl = None
	if len(sys.argv) > 2:
		appl = sys.argv[2]
	adk.build(cmd, appl)


if __name__ == "__main__":
    sys.exit(main())
