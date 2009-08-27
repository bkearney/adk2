from adk.adkplugin import ADKPlugin
import os
import sys
import imgcreate
import logging
import time


class LiveCDPlugin(ADKPlugin):
    def name(self):
        return "livecd"
        
    def describe(self):
        return "Create a livecd from a kickstart file."      
        
    def dependencies(self):
        return ["kickstart"]
        
    # Return true if the kickstart file is newer
    # then the virt-image.xml file
    def needs_to_run(self,appliance, settings):
        #target = self.resolve_appliance(appliance)
        #ksfile = target.kickstart
        #outfile = self.virt_image_path(appliance, settings)
        #if (target.generated_kickstart()):
        #    return self.check_time(settings["appliance_file"], outfile)
        #else:
        #    return self.check_time(ksfile, outfile)
        return True
        
        
    def run(self,appliance, settings):
        
        success = True 
        target = self.resolve_appliance(appliance)

        name = imgcreate.build_name(target.kickstart, "livecd-")
        fs_label = imgcreate.build_name(target.kickstart, 
                                        "livecd-",
                                        maxlen = imgcreate.FSLABEL_MAXLEN,
                                        suffix = "%s-%s" %(os.uname()[4], time.strftime("%Y%m%d%H%M")))

        logging.info("Using label '%s' and name '%s'" % (fs_label, name))

        ks = imgcreate.read_kickstart(target.kickstart)

        creator = imgcreate.LiveImageCreator(ks, name, fs_label)
        creator.tmpdir = os.path.abspath(settings["temp_directory"])
        #Should these be options?
        creator.skip_compression = False
        creator.skip_minimize = False
        
        try:
            creator.mount(None, os.path.abspath(settings["cache_directory"]))
            creator.install()
            creator.configure()
            creator.unmount()
            creator.package()
        except imgcreate.CreatorError, e:
            logging.error(u"Error creating Live CD : %s" % e)
            return False
        finally:
            creator.cleanup()
        return True
        
        
def get_plugin():
    return LiveCDPlugin()
    
