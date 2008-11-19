from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import os
import pypungi.config
import pypungi.gather
import pykickstart.parser
import pykickstart.version
import sys


class GatherPlugin(ADKPlugin):
	def name(self):
		return "gather"
		
	def describe(self):
		return "Use pungi to pull down the source rpms for an appliance"
		
	def dependencies(self):
		return ["init"]
		
	def run(self,appliance, settings):
		success = True 
		target = Appliance.get_appliance(appliance)
		target_path = os.path.join(settings["output_directory"], target.name, "source")

		conf = pypungi.config.Config()

		# Set up the kickstart parser and pass in the kickstart file we were handed
		ksparser = pykickstart.parser.KickstartParser(pykickstart.version.makeVersion())
		ksparser.readKickstart(target.kickstart)

		conf.set('default', 'name', target.name)
		conf.set('default', 'destdir', target_path)		
		conf.set('default', 'version', str(target.version))		
		conf.set('default', 'iso_basename', target.name)
		conf.set('default', 'cachedir', settings["cache_directory"])
		mygather = pypungi.gather.Gather(conf, ksparser)
		mygather.getPackageObjects()
		mygather.getSRPMList()
		mygather.downloadSRPMs()
			
		
def get_plugin():
	return GatherPlugin()
	
