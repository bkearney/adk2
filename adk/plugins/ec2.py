from adk.adkplugin import ADKPlugin
import os
import time
import logging
import virtinst.ImageParser as ImageParser

class EC2Plugin(ADKPlugin):
    def name(self):
        return "ec2"
        
    def describe(self):
        return "Bundle and upload an image to EC2"              
        
    def dependencies(self):
        return ["init","ec2convert"]

    def run(self,appliance, settings):
        img = ImageParser.parse_file(self.virt_image_path(appliance, settings))
        count = 0
        for name, disk in img.storage.iteritems():
    	    if count >= 1:
                raise ValueError, ("EC2 only supports one disk image")
                logging.error("EC2 only allows one disk, please edit your kickstart file")
            else:
                count += 1

	ec2_disk = os.path.join(self.output_path(appliance, settings),appliance + "-ec2.disk0")
	manifest_file = "/tmp/" + appliance + "-ec2-disk0.manifest.xml"
	aws_key = settings["aws_key"]
	aws_cert = settings["aws_cert"]
	aws_private_key = settings["aws_private_key"]
	aws_account_number = settings["aws_account_number"]
	aws_secret_key = settings["aws_secret_key"]
	s3_bucket = time.strftime(appliance + "-%m%d%H%M%S", time.gmtime())
	try:
	    os.system("ec2-bundle-image -i %s -c %s -k %s -u %s -r i386" % (ec2_disk,aws_cert,aws_private_key,aws_account_number))
	    os.system("ec2-upload-bundle -b %s -m %s %s -a %s -s %s %s" % (s3_bucket,ec2_disk,manifest_file,aws_key,aws_secret_key,manifest_file))
	finally:
	    os.system("ec2-register -C %s -K %s %s/%s" % (aws_cert,aws_private_key,s3_bucket,manifest_file))
        
def get_plugin():
    return EC2Plugin()
    
