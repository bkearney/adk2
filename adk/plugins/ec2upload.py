from adk.adkplugin import ADKPlugin
import os
import time
import logging
import virtinst.ImageParser as ImageParser
from ec2 import EC2Plugin

class EC2UploadPlugin(EC2Plugin):
    def name(self):
        return "ec2upload"
        
    def describe(self):
        return "Bundle and upload an image to EC2"              
        
    def dependencies(self):
        return ["ec2bundle"]

    def run(self,appliance, settings):
        img = ImageParser.parse_file(self.virt_image_path(appliance, settings))
        count = 0
        for name, disk in img.storage.iteritems():
    	    if count >= 1:
                raise ValueError, ("EC2 only supports one disk image")
                logging.error("EC2 only allows one disk, please edit your kickstart file")
            else:
                count += 1
                
        target = self.resolve_appliance(appliance)
        manifest_file = self.manifest_file(appliance, settings)
        s3_bucket = target.s3bucket
        aws_key = settings["aws_key"]
        aws_secret_key = settings["aws_secret_key"]
        self.exec_cmd("ec2-upload-bundle -b %s -m %s -a %s -s %s --retry" % (s3_bucket,manifest_file,aws_key,aws_secret_key))    
        
def get_plugin():
    return EC2UploadPlugin()
    
