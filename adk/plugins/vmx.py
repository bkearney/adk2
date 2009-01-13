import os
import shutil
import logging
import random
import logging
from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import virtconv.formats as formats

class VMXPlugin(ADKPlugin):
    def name(self):
        return "vmx"
        
    def describe(self):
        return "Convert an image into a vmx format"      
                
    def dependencies(self):
        return ["build"]
        
    def output_dir(self, appliance, settings):
        return os.path.join(self.output_path(appliance, settings), "vmware")    
        
    def output_file(self, name, suffix, appliance, settings):
        unixname = name.replace(" ", "-")
        return os.path.join(self.output_dir(appliance, settings), "%s%s" % (unixname, suffix))          
        
    def needs_to_run(self,appliance, settings):
        # Check that the input file is newer than at least one of the possible
        # output files.
        target = self.resolve_appliance(appliance)        
        image_file = self.virt_image_path(appliance, settings)
        output_path = self.output_file(target.name, "vmx", appliance, settings)
        return self.check_time(image_file, output_path)        
        
    def run(self,appliance, settings):
        success = True 
        target = self.resolve_appliance(appliance)           
        virt_image_path = self.virt_image_path(appliance, settings)
        inp = formats.find_parser_by_file(virt_image_path)
        outp = formats.parser_by_name("vmx")        
        vmdef = inp.import_file(virt_image_path)
        output_dir = self.output_dir(appliance, settings)
        output_file = self.output_file(target.name, "vmx", appliance, settings)
           
        try:
            for d in vmdef.disks.values():
                format = "vmdk"

                if d.path and format != "none":
                    logging.info("Converting disk \"%s\" to type %s..." %
                        (d.path, format))

                d.convert(self.output_path(appliance, settings), output_dir, format)

        except Exception, e:
            logging.error("Couldn't convert disks: %s" % e)

        try:
            outp.export_file(vmdef, output_file)
        except ValueError, e:
            logging.error("Couldn't export to file \"%s\": %s" % output_file, e)   
            
        return success

def get_plugin():
    return VMXPlugin()
    
