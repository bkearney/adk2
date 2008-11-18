class ADKPlugin:
	def plugin_name(self):
		return "none"
		
	def dependencies(self):
		return []
		
	def needs_to_run(self):
		return True
		
	def run(self,appliance, settings):
		return True
