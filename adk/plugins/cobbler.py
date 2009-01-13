import os
import xmlrpclib
import virtinst.ImageParser as ImageParser
import adk.appliance as Appliance
from adk.adkplugin import ADKPlugin


class CobblerPlugin(ADKPlugin):
    def name(self):
        return "cobbler"
        
    def describe(self):
        return "Push an appliance to cobbler for provisioning"          
        
    def dependencies(self):
        return ["init", "build"]
        
    def run(self,appliance, settings):
        # Get the disk files     
        image = ImageParser.parse_file(self.virt_image_path(appliance, settings))
        disks = []
        for name, disk in image.storage.iteritems():
            imagefile = os.path.join(self.output_path(appliance, settings), disk.file)
            disks.append(imagefile)
        all_disks = ",".join(disks)
        
        # Convert the memory to megebytes
        memory_in_mb = image.domain.memory / 1024
        
        # Translate the architecture
        arch = image.domain.boots[0].arch
        if arch == 'i686':
            arch = 'x86'
            
        # Log into cobbler
        server = settings["cobbler_hostname"]
        login = settings["cobbler_user"]
        password = settings["cobbler_password"]        
        
        cobbler_uri = "http://%s/cobbler_api_rw" % server
        remote =  xmlrpclib.Server(cobbler_uri)
        token = remote.login(login,password)
        
        # Create and update the image
        image_id = remote.new_image(token)
        remote.modify_image(image_id, "name",appliance,token)
        remote.modify_image(image_id, "virt_ram",memory_in_mb,token) 
        remote.modify_image(image_id, "virt_cpus",image.domain.vcpu,token)         
        remote.modify_image(image_id, "virt_type","auto",token)                 
        remote.modify_image(image_id, "image_type","virt-clone",token)                         
        remote.modify_image(image_id, "file",all_disks,token)         
        remote.modify_image(image_id, "virt_bridge","",token)   
        remote.modify_image(image_id, "network_count",image.domain.interface,token)           
        remote.modify_image(image_id, "arch",arch,token)               
        remote.save_image(image_id,token)
        
def get_plugin():
    return CobblerPlugin()
    
