from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import os
import sys
import shutil
import appcreate
import imgcreate
import logging


class AppcreatorPlugin(ADKPlugin):
    def name(self):
        return "appliance"
        
    def describe(self):
        return "Create a virtual-machine image from a kickstart file."      
        
    def dependencies(self):
        return ["init"]
        
    # Return true if the kickstart file is newer
    # then the virt-image.xml file
    def needs_to_run(self,appliance, settings):
        should_run = True
        target = Appliance.get_appliance(appliance)
        ksfile = target.kickstart
        outfile = self.virt_image_path(appliance, settings)
        if (os.path.exists(outfile)):
            should_run = (os.stat(ksfile).st_mtime) > (os.stat(outfile).st_mtime)
        return should_run
        
        
    def run(self,appliance, settings):
        success = True 
        target = Appliance.get_appliance(appliance)
        vmem = int(target.memory)
        vcpus = int(target.cpus)
        appname = target.name
        #TODO How pass these in
        format = "raw"
        package = "none"
        include = ""
        
        ks = imgcreate.read_kickstart(target.kickstart)
        creator = appcreate.ApplianceImageCreator(ks, appname, format, vmem, vcpus)     
        creator.tmpdir = settings["temp_directory"]
        creator.checksum = True 
        try:
            creator.mount("NONE", settings["cache_directory"])
            creator.install()
            creator.configure()
            creator.unmount()
            creator.package(settings["output_directory"], package, include)
        except imgcreate.CreatorError, e:
            logging.error("Unable to create appliance : %s" % e)
            return 1
        finally:
            creator.cleanup()
        
        
def get_plugin():
    return AppcreatorPlugin()
    
