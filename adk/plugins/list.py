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
        print appliance
        
        if appliance not in ["appliances", "settings", "plugins", None]:
            print ("%s is not a valid item to list" % appliance)
            return False
            
        if appliance == "appliances" or appliance is None:
            for appl in Appliance.get_appliances():
                print spacer + str(appl)
        if appliance == "settings" or appliance is None:
            for setting, value in settings.iteritems():
                print spacer + "%s => %s" % (setting, value)
        if appliance == "plugins" or appliance is None:
            adk = settings["adk"]
            for plugin_name, plugin in adk.plugins.iteritems():
                print spacer + "%s => %s" % (plugin_name, plugin.describe())                
        return True
            
        
def get_plugin():
    return ListPlugin()
    
