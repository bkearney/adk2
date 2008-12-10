from adk.adkplugin import ADKPlugin
import os
import time
import logging
import virtinst.ImageParser as ImageParser
from ec2 import EC2Plugin

class EC2BundlePlugin(EC2Plugin):
    def name(self):
        return "ec2bundle"
        
    def describe(self):
        return "Bundle an image for EC2"              
        
    def dependencies(self):
        return ["ec2convert"]
        
    def needs_to_run(self,appliance, settings):
        # Check that the input file is newer than at least one of the possible
        # output files.   
        converted_file = self.converted_file(0, appliance, settings)    
        manifest_file = self.manifest_file(appliance, settings)
        return self.check_time(converted_file, manifest_file)         

    def run(self,appliance, settings):
        img = ImageParser.parse_file(self.virt_image_path(appliance, settings))
        count = 0
        target = self.resolve_appliance(appliance)
        for name, disk in img.storage.iteritems():
    	    if count >= 1:
                raise ValueError, ("EC2 only supports one disk image")
                logging.error("EC2 only allows one disk, please edit your kickstart file")
            else:
                count += 1

        directory = self.output_dir(appliance, settings)
        ec2_disk = self.converted_file(0, appliance, settings)
        aws_cert = settings["aws_cert"]
        aws_private_key = settings["aws_private_key"]
        aws_account_number = settings["aws_account_number"]
        cmd = "ec2-bundle-image -i %s -c %s -k %s -u %s -r i386 -d %s " % (ec2_disk,aws_cert,aws_private_key,aws_account_number, directory)
        if target.ec2kernel is not None:
            cmd += " --kernel %s" % target.ec2kernel
        if target.ec2ramdisk is not None:
            cmd += " --ramdisk %s" % target.ec2ramdisk
        print cmd
        os.system(cmd)
        
        return True
        
def get_plugin():
    return EC2BundlePlugin()
    
