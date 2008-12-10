from adk.adkplugin import ADKPlugin
import os
import time
import logging
import virtinst.ImageParser as ImageParser

class EC2Plugin(ADKPlugin):

    def output_dir(self, appliance, settings):
        return os.path.join(self.output_path(appliance, settings), "ec2")    
        
    def manifest_file(self, appliance, settings):  
        return os.path.join(self.output_dir(appliance, settings), appliance + "-ec2.disk0.manifest.xml") 
        
    def converted_file(self, count, appliance, settings):
        output_name = appliance+"-ec2.disk" + str(count)
        output_path = os.path.join(self.output_dir(appliance, settings), output_name)
        return output_path

    
