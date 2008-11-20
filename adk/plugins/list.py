from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance

class ListPlugin(ADKPlugin):
    
    def name(self):
        return "list"
        
    def describe(self):
        return "Provide data about the running environment"
        
    def run(self,appliance, settings):
        success = True 
        spacer = "  "
        if appliance == "appliances":
            for appliance in Appliance.get_appliances():
                print spacer + str(appliance)
        elif appliance == "settings":
            for setting, value in settings.iteritems():
                print spacer + "%s => %s" % (setting, value)
        elif appliance == "plugins":
            adk = settings["adk"]
            for plugin_name, plugin in adk.plugins.iteritems():
                print spacer + "%s => %s" % (plugin_name, plugin.describe())                
        else:
            print ("%s is not a valid item to list" % appliance)
            
        
def get_plugin():
    return ListPlugin()
    
