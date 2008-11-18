from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import os
import pypungi.config
import pypungi.gather
import pypungi.pungi
import pykickstart.parser
import pykickstart.version
import sys


class SrcIsoPlugin(ADKPlugin):
	def plugin_name(self):
		return "srciso"
		
	def dependencies(self):
		return ["init", "gather"]
		
	def run(self,appliance, settings):
		success = True 
		target = Appliance.get_appliance(appliance)
		target_path = os.path.join(settings["output_directory"], target.name, "source")
		print target_path

		conf = pypungi.config.Config()

		# Set up the kickstart parser and pass in the kickstart file we were handed
		ksparser = pykickstart.parser.KickstartParser(pykickstart.version.makeVersion())
		ksparser.readKickstart(target.kickstart)

		conf.set('default', 'name', target.name)
		conf.set('default', 'destdir', target_path)		
		conf.set('default', 'arch', 'source')		
		conf.set('default', 'cachedir', settings["cache_directory"])
		conf.set('default', 'iso_basename', target.name)		
		conf.set('default', 'force', str(True))
		conf.set('default', 'version', str(target.version))		
		mypungi = pypungi.pungi.Pungi(conf)
		mypungi.topdir = os.path.join(conf.get('default', 'destdir'),
									  conf.get('default', 'version'),
									  "source", 'SRPMS')
		mypungi.doCreaterepo(comps=False)
		mypungi.doCreateIsos(split=False)
		
			
		
def get_plugin():
	return SrcIsoPlugin()
	
