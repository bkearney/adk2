from adk.adkplugin import ADKPlugin
import shutil
import logging

class ClearPlugin(ADKPlugin):
    def name(self):
        return "clear"
    
    def describe(self):
        return "Clean up the environment"      
        
    def remove_directory(self, directory):
        shutil.rmtree(directory)

    def run(self,appliance, settings):
        
        if appliance not in ["cache"]:
            print ("%s is not a valid item to clear" % appliance)
            return False
                            
        if appliance == "cache":
            self.remove_directory(settings["cache_directory"])
        
        
def get_plugin():
    return ClearPlugin()
    
