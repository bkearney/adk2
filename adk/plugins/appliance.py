from adk.adkplugin import ADKPlugin

class AppliancePlugin(ADKPlugin):
	def plugin_name(self):
		return "appliance"
		
	def dependencies(self):
		return ["init"]
		
		
def get_plugin():
	return AppliancePlugin()
	
