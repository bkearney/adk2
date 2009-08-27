import os
import tempfile
import logging
import adk.appliance as Appliance
from adk.adkplugin import ADKPlugin
from Cheetah.Template import Template



class KickstartGenPlugin(ADKPlugin):
    def name(self):
        return "kickstart"
        
    def describe(self):
        return "Generate a kickstart file from the provided metadata"          
        
    def dependencies(self):
        return ["init"]
        
    def run(self,appliance, settings):
        target = self.resolve_appliance(appliance)
        if (target.generated_kickstart()):
			t = Template(file=settings["kickstart_template"])
			t.ks = target.kickstart_meta
			ksname = "%s.ks" % appliance
			kspath = os.path.join(settings["temp_directory"],ksname)
			logging.info("Creating kickstart file at %s " % kspath)
			f = open(kspath, 'w')
			f.write(str(t))
			f.close()
			target.kickstart=kspath 
        
def get_plugin():
    return KickstartGenPlugin()
    
