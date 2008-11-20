from adk.adkplugin import ADKPlugin

class EC2Plugin(ADKPlugin):
    def name(self):
        return "ec2"
        
    def dependencies(self):
        return ["init", "appliance"]
        
def get_plugin():
    return EC2Plugin()
    
