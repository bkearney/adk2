import settings 

class Appliance:
    appliances = None
    
    def __init__(self, name="", kickstart="", memory=0, cpus=0, version=None, release=None):
        self.name = name
        self.kickstart = kickstart
        self.memory = memory
        self.cpus = cpus
        self.version = version
        self.release = release      
        
    def __str__(self):
        return "Appliance '%s' kickstart: '%s'" % (self.name, self.kickstart)
    

def _get_appliances():
    if Appliance.appliances is None:
        load_appliances()
    return Appliance.appliances
        
def load_appliances():
    Appliance.appliances={}
    appl_data = settings.load_appliances()
    for appl, attributes in appl_data.iteritems():
        new_appl = Appliance(appl)
        new_appl.kickstart = attributes["kickstart"]
        new_appl.memory = attributes["memory"]      
        new_appl.cpus = attributes["cpus"]      
        new_appl.version = attributes["version"]        
        Appliance.appliances[appl]= new_appl
        
def get_appliance(name):
    if name in _get_appliances():
        return _get_appliances()[name]  
    else:
        return None
    
def get_appliances():
    return _get_appliances().values()

