import os
import logging
import appliance as Appliance

class ADKError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)

class UnknownApplianceError(ADKError):
    def __init__(self, msg):
        ADKError.__init__(self, msg)
        
class UnknownPluginError(ADKError):
    def __init__(self, msg):
        ADKError.__init__(self, msg)        


class Util:
    def virt_image_path(self, appliance, settings):
        return os.path.join(settings["output_directory"], appliance, "%s.xml" % appliance)
        
    def output_path(self, appliance, settings):
        return os.path.join(settings["output_directory"], appliance)
        
    def check_time(self, input, output):
        """Returns True if the input file is newer then the output file
           or if the output file does not exist"""
        should_run = True
        if (os.path.exists(output)):
            should_run = (os.stat(input).st_mtime) > (os.stat(output).st_mtime)
        return should_run

    def resolve_appliance(self, appliance_name, raise_error = True):
        target = Appliance.get_appliance(appliance_name)
        if (target is None) and raise_error:
            raise UnknownApplianceError("No appliance named %s was found" % appliance_name)
        return target 
        
    def create_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info("Creating directory '%s' " % directory)
            os.makedirs(directory)    
            
    def exec_cmd(self, cmd):
        logging.debug("Excuting '%s'" % cmd)
        os.system(cmd)
