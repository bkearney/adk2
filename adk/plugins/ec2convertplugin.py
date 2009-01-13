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
from ec2 import EC2Plugin



class Ec2ConvertPlugin(EC2Plugin):
    def name(self):
        return "ec2convert"
        
    def describe(self):
        return "Convert an image into an ec2 format"      
                
    def dependencies(self):
        return ["init", "build"]
        
    def needs_to_run(self,appliance, settings):
        # Check that the input file is newer than at least one of the possible
        # output files.
        image_file = self.virt_image_path(appliance, settings)
        output_path = self.converted_file(0, appliance, settings)
        return self.check_time(image_file, output_path)        
        
    def run(self,appliance, settings):
        success = True 
        img = ImageParser.parse_file(self.virt_image_path(appliance, settings))
        count = 0
        directory = self.output_dir(appliance, settings)
        self.create_directory(directory)
        for name, disk in img.storage.iteritems():
            source_path = os.path.join(self.output_path(appliance, settings), disk.file)            
            success = ec2config.convert(source_path, "diskimage", \
                settings["temp_directory"], "yes", "yes", self.converted_file(count, appliance, settings))            
            count += 1                

def get_plugin():
    return Ec2ConvertPlugin()
    
