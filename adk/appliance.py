import settings 

class Appliance:
    appliances = None
    
    def __init__(self, name="", kickstart="", memory=0, cpus=0, version=None, \
                release=None, checksum=True, s3bucket=None, ec2ramdisk=None, ec2kernel=None):
        self.name = name
        self.kickstart = kickstart
        self.memory = memory
        self.cpus = cpus
        self.version = version
        self.release = release 
        self.checksum = checksum     
        self.s3bucket = s3bucket
        self.ec2ramdisk = ec2ramdisk
        self.ec2kernel = ec2kernel
        
    def __str__(self):
        return "Appliance '%s' kickstart: '%s'" % (self.name, self.kickstart)
    

def _get_appliances():
    if Appliance.appliances is None:
        load_appliances()
    return Appliance.appliances
    
def get_attribute(attributes, name, default_value = None):
    try:
        return attributes[name]
    except KeyError:
        return default_value
        
        
def load_appliances():
    Appliance.appliances={}
    appl_data = settings.load_appliances()
    for appl, attributes in appl_data.iteritems():
        new_appl = Appliance(appl)
        new_appl.kickstart = get_attribute(attributes, "kickstart")
        new_appl.memory = get_attribute(attributes, "memory")     
        new_appl.cpus = get_attribute(attributes, "cpus")   
        new_appl.version = get_attribute(attributes, "version")
        new_appl.checksum = get_attribute(attributes, "checksum", True)
        new_appl.s3bucket = get_attribute(attributes, "s3bucket")        
        new_appl.ec2ramdisk = get_attribute(attributes, "ec2ramdisk")             
        new_appl.ec2kernel = get_attribute(attributes, "ec2kernel")                     
        Appliance.appliances[appl]= new_appl
        
def get_appliance(name):
    if name in _get_appliances():
        return _get_appliances()[name]  
    else:
        return None
    
def get_appliances():
    return _get_appliances().values()

