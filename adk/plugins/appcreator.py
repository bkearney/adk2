from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import os
import sys
import shutil
import optparse
import appcreate
import imgcreate
import logging


class AppcreatorPlugin(ADKPlugin):
	def name(self):
		return "appliance"
		
	def dependencies(self):
		return ["init"]
		
	def run(self,appliance, settings):
		success = True 
		target = Appliance.get_appliance(appliance)
		vmem = int(target.memory)
		vcpus = int(target.cpus)
		appname = target.name
		#TODO How pass these in
		format = "raw"
		package = "none"
		include = ""
		
		ks = imgcreate.read_kickstart(target.kickstart)
		creator = appcreate.ApplianceImageCreator(ks, appname, format, vmem, vcpus)		
		creator.tmpdir = settings["temp_directory"]
		creator.checksum = True	
		try:
			creator.mount("NONE", settings["cache_directory"])
			creator.install()
			creator.configure()
			creator.unmount()
			creator.package(settings["output_directory"], package, include)
		except imgcreate.CreatorError, e:
			logging.error("Unable to create appliance : %s" % e)
			return 1
		finally:
			creator.cleanup()
		
		
def get_plugin():
	return AppcreatorPlugin()
	
