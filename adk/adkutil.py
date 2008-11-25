import os

class ADKUtil:
    def virt_image_path(self, appliance, settings):
        return os.path.join(settings["output_directory"], appliance, "%s.xml" % appliance)
        
    def output_path(self, appliance, settings):
        return os.path.join(settings["output_directory"], appliance)
        
    def check_time(self, input, output):
        """Returns True if the input file is newer then the output file
           or if the output file does not exist"""
        should_run = True
        if (os.path.exists(output)):
            should_run = (os.stat(input).st_mtime) > (os.stat(output).st_mtime)
        return should_run
