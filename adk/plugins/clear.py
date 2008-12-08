from adk.adkplugin import ADKPlugin
import os
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
        clear_targets = ["cache", "output", "all" ]
        if appliance not in clear_targets:
            print ("%s is not a valid item to clear. Select one of: [%s]." % (appliance, ", ".join(clear_targets)))
            return False
                            
        if appliance == "cache" or appliance== "all":
            if os.path.exists(settings["cache_directory"]):
                self.remove_directory(settings["cache_directory"])
                
        if appliance == "output" or appliance== "all":
            if os.path.exists(settings["output_directory"]):
                self.remove_directory(settings["output_directory"])                
        
        
def get_plugin():
    return ClearPlugin()
    
