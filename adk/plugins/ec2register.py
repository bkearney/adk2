from adk.adkplugin import ADKPlugin
import os
import time
import logging
import virtinst.ImageParser as ImageParser
from ec2 import EC2Plugin

class EC2RegisterPlugin(EC2Plugin):
    def name(self):
        return "ec2register"
        
    def describe(self):
        return "Bundle and upload an image to EC2"              
        
    def dependencies(self):
        return ["init","ec2upload"]
        
    def run(self,appliance, settings):
        target = self.resolve_appliance(appliance)
        s3_bucket = target.s3bucket
        manifest_file = self.manifest_file(appliance, settings)
        aws_cert = settings["aws_cert"]
        aws_private_key = settings["aws_private_key"]
        os.system("ec2-register -C %s -K %s %s/%s" % (aws_cert,aws_private_key,s3_bucket,manifest_file))
        
def get_plugin():
    return EC2RegisterPlugin()
    
