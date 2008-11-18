from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance

class ListPlugin(ADKPlugin):
	
	def plugin_name(self):
		return "list"
		
	def run(self,appliance, settings):
		success = True 
		if appliance == "appliances":
			for appliance in Appliance.get_appliances():
				print appliance
		elif appliance == "settings":
			for setting, value in settings.iteritems():
				print "%s => %s" % (setting, value)
		else:
			print ("%s is not a valid item to list" % appliance)
			
		
def get_plugin():
	return ListPlugin()
	
