import os

class ADKUtil:
    def virt_image_path(self, appliance, settings):
        return os.path.join(settings["output_directory"], appliance, "%s.xml" % appliance)
        
    def output_path(self, appliance, settings):
        return os.path.join(settings["output_directory"], appliance)
        
