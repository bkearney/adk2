import os
import yaml

class Appliance(yaml.YAMLObject):
    yaml_tag = u'!Appliance'    
    appliances = None

    def __new__(cls, name="", kickstart="", memory=0, cpus=0, version=None, \
                release=None, checksum=True, s3bucket=None, ec2ramdisk=None, ec2kernel=None, kickstart_meta = None):
        obj = yaml.YAMLObject.__new__(cls)
        obj.name = name
        obj.kickstart = kickstart
        obj.memory = memory
        obj.cpus = cpus
        obj.version = version
        obj.release = release
        obj.checksum = checksum
        obj.s3bucket = s3bucket
        obj.ec2ramdisk = ec2ramdisk
        obj.ec2kernel = ec2kernel
        obj.kickstart_meta = kickstart_meta
        return obj

    def __str__(self):
        if (not self.generated_kickstart()):
            ks = self.kickstart
        else:
            ks = "auto generated"
        return "Appliance '%s' kickstart: '%s'" % (self.name, ks)

    def generated_kickstart(self):
        return self.kickstart_meta is not None

class KickstartMeta(yaml.YAMLObject):
    yaml_tag = u'!KickstartMeta'
    def __new__(cls, rootpw="", packages=[], repos=[], partitions=[], excludes=[]):
        obj = yaml.YAMLObject.__new__(cls)        
        obj.rootpw = rootpw
        obj.packages = packages
        obj.repos = repos
        obj.partions = packages
        obj.excludes = excludes
        return obj

class Repo(yaml.YAMLObject):
    yaml_tag = u'!Repo'
   
    def __new__(cls, name="", mirrorlist=None, baseurl=None):
        obj = yaml.YAMLObject.__new__(cls)            
        obj.name = name
        obj.mirrorlist = mirrorlist
        obj.baseurl = baseurl
        return obj
        
class Partition(yaml.YAMLObject):
    yaml_tag = u'!Partition'

    def __new__(cls, root="", type="ext3", size="1000", disk="sda" ):      
        obj = yaml.YAMLObject.__new__(cls)   
        obj.root = root
        obj.type = type
        obj.size = size
        obj.disk = disk
        return obj

    def __str__(self):
        return "Partition '%r' type: '%r' size: '%r' disk: '%r'" % (self.root, self.kickstart, self.size, self.disk)         

# This custom loader allows us to parse the appliance syntax
# and not interfere with any other yaml parsing.
class ApplianceLoader(yaml.Loader):
    def __init__(self, stream):
        yaml.Loader.__init__(self, stream)        


# Public functions for loading up the appliances
def load_appliances():
    Appliance.appliances={}
    try:
        config_file = os.environ["ADK_APPLIANCES"]
        # Set up the YAML parser to understand the appliance file.
        yaml.add_path_resolver(u'!Appliance', [],None, ApplianceLoader)
        yaml.add_path_resolver(u'!KickstartMeta', ["kickstart_meta"],None, ApplianceLoader)
        yaml.add_path_resolver(u'!Repo', ["kickstart_meta", "repos", (yaml.SequenceNode, False)],None, ApplianceLoader)
        yaml.add_path_resolver(u'!Partition', ["kickstart_meta", "partitions", (yaml.SequenceNode, False)],None, ApplianceLoader)
        # Load the file
        for appliance in yaml.load_all(open(config_file, "r"), ApplianceLoader):
            Appliance.appliances[appliance.name] = appliance     
    except KeyError:
        raise ADKError("ADK_APPLIANCES environment variable is not set")


def _get_appliances():
    if Appliance.appliances is None:
        load_appliances()
    return Appliance.appliances

def get_appliance(name):
    if name in _get_appliances():
        return _get_appliances()[name]
    else:
        return None
        
def get_appliances():
    return _get_appliances().values()


