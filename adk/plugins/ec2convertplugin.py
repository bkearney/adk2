import os
import shutil
import logging
import random
import logging
from adk.adkplugin import ADKPlugin
import adk.appliance as Appliance
import virtinst.ImageParser as ImageParser
import ec2convert.ec2config as ec2config
import ec2convert.rpmcheck as rpmcheck
import ec2convert.fs as fs



class Ec2ConvertPlugin(ADKPlugin):
	def name(self):
		return "ec2convert"
		
	def dependencies(self):
		return ["init", "appliance"]
		
	def run(self,appliance, settings):
		success = True 
		target = Appliance.get_appliance(appliance)
		img = ImageParser.parse_file(self.virt_image_path(appliance, settings))
		count = 0
		for name, disk in img.storage.iteritems():
			count += 1
			imagefile = disk.file
			imagename = os.path.join(self.output_path(appliance, settings), appliance+"-ec2.disk" + str(count))
			tmpdir = settings["temp_directory"] + "/ec2-convert-" + (''.join(random.sample('123567890abcdefghijklmnopqrstuvwxyz', 8)))
			tmpimage = tmpdir + "-tmpimage"
			newimage = tmpimage + "/ec2-diskimage.img"
			fsutil = fs.loopbackdisk_image()

			os.mkdir(tmpdir)
			os.mkdir(tmpimage)

			logging.debug("Copying %s to %s" % (imagefile,tmpimage))
			shutil.copy(imagefile,newimage)

			#TODO: The ec2-converter code needs to be made into a bit 
			# more of a library
			fsutil.setup_fs(imagefile,tmpdir)

			rpmcheck.checkpkgs(tmpdir)
			config = ec2config.ec2_modify()
			config.makedev(tmpdir)
			config.fstab(tmpdir)
			config.rclocal_config(tmpdir)
			config.ssh_config(tmpdir)

			config.eth0_config(tmpdir)
			config.ami_tools(tmpdir)
			config.kernel_modules(tmpdir)
			fsutil.unmount(tmpdir)
			shutil.move(newimage,imagename)  
			fsutil.cleanup(tmpdir)    			


def get_plugin():
	return Ec2ConvertPlugin()
	
