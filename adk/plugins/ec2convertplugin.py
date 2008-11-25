import os
import shutil
import logging
import random
import logging
from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import virtinst.ImageParser as ImageParser
import ec2convert.ec2config as ec2config
import ec2convert.rpmcheck as rpmcheck
import ec2convert.fs as fs



class Ec2ConvertPlugin(ADKPlugin):
    def name(self):
        return "ec2convert"
        
    def describe(self):
        return "Convert an image into an ec2 format"      
                
    def dependencies(self):
        return ["init", "appliance"]
        
    def needs_to_run(self,appliance, settings):
        # Check that the input file is newer than at least one of the possible
        # output files.
        image_file = self.virt_image_path(appliance, settings)
        output_name = appliance+"-ec2.disk0"
        output_path = os.path.join(self.output_path(appliance, settings), output_name)
        return self.check_time(image_file, output_path)        
        
    def run(self,appliance, settings):
        success = True 
        img = ImageParser.parse_file(self.virt_image_path(appliance, settings))
        count = 0
        for name, disk in img.storage.iteritems():
            output_name = appliance+"-ec2.disk" + str(count)
            output_path = os.path.join(self.output_path(appliance, settings), output_name)
            source_path = os.path.join(self.output_path(appliance, settings), disk.file)            
            count += 1
            success = ec2config.convert(source_path, "diskimage", \
                settings["temp_directory"], "yes", "yes", output_path)            

def get_plugin():
    return Ec2ConvertPlugin()
    
