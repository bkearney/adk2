from adk.adkplugin import ADKPlugin

class CobblerPlugin(ADKPlugin):
    def name(self):
        return "cobbler"
        
    def dependencies(self):
        return ["init", "appliance"]
        
def get_plugin():
    return CobblerPlugin()
    
