from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import os
import pypungi
import pykickstart.parser
import pykickstart.version
import sys


class SrcIsoPlugin(ADKPlugin):
    def name(self):
        return "srciso"
        
    def describe(self):
        return "Build source isos for the appliance"                
        
    def dependencies(self):
        return ["init", "gather"]
        
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
        conf.set('pungi', 'arch', 'source')       
        conf.set('pungi', 'cachedir', settings["cache_directory"])
        conf.set('pungi', 'iso_basename', target.name)        
        conf.set('pungi', 'force', str(True))
        conf.set('pungi', 'version', str(target.version))     
        mypungi = pypungi.Pungi(conf, ksparser)
        mypungi.topdir = os.path.join(conf.get('pungi', 'destdir'),
                                      conf.get('pungi', 'version'),
                                      "source", 'SRPMS')
        mypungi.doCreaterepo(comps=False)
        mypungi.doCreateIsos(split=False)
        
            
        
def get_plugin():
    return SrcIsoPlugin()
    
