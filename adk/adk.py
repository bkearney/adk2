import appliance as Appliance
import settings as Settings
import debug
import logging
import optparse
import os
from util import *
import sys

class ADK(Util):
    
    def __init__(self, force=False):
        self.load_plugins()
        self.settings = Settings.load_settings()
        self.settings["adk"] = self
        self.settings["force"] = force
        self.force = force 
        
    def load_plugins(self):
        # TODO: Make this dynamic
        plugin_list = ["appcreator", "cobbler", "clear", "init", "list", \
        "gather", "srciso", "ec2convertplugin",  "ec2register", "ec2bundle", \
        "kickstart", "ec2upload", "vmx"]
        self.plugins={}
        for plug in plugin_list:
            logging.debug("Loading plugin: %s " % plug)
            plugin_module = __import__("plugins.%s" % (plug), globals(), locals(), [plug])
            new_plugin = plugin_module.get_plugin()
            self.plugins[new_plugin.name()]= new_plugin
        
        
    def process_chain(self, plugin_name, chain=[]):
        try:
            plugin = self.plugins[plugin_name]
        except KeyError:
            raise UnknownPluginError("No plugin named %s was found" % plugin_name)
        if plugin not in chain:
            #check to see if any of my dependencies are already in there
            position = 0
            for dep in plugin.dependencies():
                dep_plugin = self.plugins[dep]
                self.process_chain(dep, chain)                    
                if dep_plugin in chain:
                    dep_position = chain.index(dep_plugin) + 1
                    if dep_position > position:
                        position = dep_position 
            logging.debug("inserting %s at position %s" % (plugin.name(), str(position)))
            chain.insert(position, plugin)  
                
        return chain

    def store_args(self, args):
        for x in range(len(args)):
            self.settings["arg%s" % x] = args[x]
            
    def build(self, target, appliance, args):
        build_chain = self.process_chain(target)
        self.store_args(args)
        try:
            if logging.getLogger().isEnabledFor(logging.INFO):
                msg = "Execution Chain is : ["
                
                cnt = 0
                for item in build_chain:    
                    if cnt != 0:
                        msg += " => "
                    cnt += 1                        
                    msg += ("%s" % str(item))
                msg += "]"
                    
                logging.info(msg)
                        
            for plugin in build_chain:
                if self.force or plugin.needs_to_run(appliance, self.settings):
                    logging.info("Executing %s for %s" % (plugin.name(), appliance))
                    plugin.run(appliance, self.settings)
                else:
                    logging.info("Skipping %s" % plugin.name())
        except UnknownApplianceError:
            logging.error("No appliance named %s was found" % appliance)
            
    def build_all(self, cmd):
        for appl in Appliance.get_appliances():
            self.build(cmd, appl.name)
            self.load_plugins()
    
def parse_options(args):
    usage = "Usage: %prog [options] PLUGIN APPLIANCE [OTHER OPTIONS]\n\n\
    Where PLUGIN can be seen by calling 'adk list plugins' \n\
    and APPLIANCE can be seen by calling 'adk list appliances'"

    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option("", "--force", action="store_true", dest="force",
                  default=False, help="Force all steps to run")
                      
    debug.setup_logging(parser)
    (options, args) = parser.parse_args()
        
    return options, args
        
def main():
    """
    Command Line entry
    """ 
    
    if os.geteuid() != 0:
        print >> sys.stderr, "You must run the adk as root"
        return 1
            
    # Parse the options
    args = sys.argv
    options, args = parse_options(args) 
    
    if len(args) == 0:
        print "You must specify a plugin. Run 'adk list plugins' for an example"
        return 1
        
    cmd = args.pop(0)
    logging.debug("Plugin: %s" % cmd)
    appl = None
    if len(args) > 0:
        logging.debug("Appliance: %s" % cmd)        
        appl = args.pop(0)
        
    try:
        adk = ADK(options.force)           
        if appl == "ALL":
            adk.build_all(cmd)
        else:
            adk.build(cmd, appl, args)
    except ADKError, e:
        print e.msg
        return 1


if __name__ == "__main__":
    sys.exit(main())
