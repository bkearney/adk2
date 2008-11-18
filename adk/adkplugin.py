class ADKPlugin:
	def name(self):
		return "none"
		
	def describe(self):
		return "I do unknown, but wonderful things"		
		
	def dependencies(self):
		return []
		
	def needs_to_run(self):
		return True
		
	def run(self,appliance, settings):
		return True
