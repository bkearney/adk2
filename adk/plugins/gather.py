from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import os
import pypungi.config
import pykickstart.parser
import pykickstart.version
import sys


class GatherPlugin(ADKPlugin):
    def name(self):
        return "gather"
        
    def describe(self):
        return "Use pungi to pull down the source rpms for an appliance"
        
    def dependencies(self):
        return ["init", "kickstart"]
        
		
    def get_pungi(self, conf, ksparser):
        # Try the new API, fall back to the old
        mypungi = None
        try:
            import pypungi.gather
            mypungi = pypungi.gather.Gather(conf, ksparser)            
        except:
            from pypungi import Pungi
            mypungi = Pungi(conf, ksparser)
            mypungi._inityum()	    
         
        return mypungi
		
    def run(self,appliance, settings):
        success = True 
        target = Appliance.get_appliance(appliance)
        target_path = os.path.join(settings["output_directory"], target.name, "source")

        conf = pypungi.config.Config()

        # Set up the kickstart parser and pass in the kickstart file we were handed
        ksparser = pykickstart.parser.KickstartParser(pykickstart.version.makeVersion())
        ksparser.readKickstart(target.kickstart)

        conf.set('pungi', 'name', target.name)
        conf.set('pungi', 'destdir', target_path)     
        conf.set('pungi', 'version', str(target.version))     
        conf.set('pungi', 'iso_basename', target.name)
        conf.set('pungi', 'force', str(True))        
        conf.set('pungi', 'cachedir', settings["cache_directory"])
        conf.set('pungi', 'debuginfo', "True")
        

        mypungi = self.get_pungi(conf, ksparser)
        mypungi.getPackageObjects()
        mypungi.createSourceHashes()
        mypungi.getSRPMList()
        mypungi.downloadSRPMs()
        
def get_plugin():
    return GatherPlugin()
    
