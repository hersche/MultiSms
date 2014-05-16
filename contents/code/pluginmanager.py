'''
Created on 08.03.2010

@author: skamster
'''
import os, sys
class PluginManager(object):
    '''
    classdocs
    '''
    def __init__(self, path, package, parentObject):
        self.pluginsList = []
        #moduleList = []
        if(os.path.isdir(path)):
            dirList=os.listdir(path)
            sys.path.append(path)
            for fname in dirList:
                if fname.endswith(".py"):
                    try:
                        if fname[:-3] != "__init__":
                            print "try a import of "+path+fname[:-3]
                            if package == "":
                                module = __import__(fname[:-3])
                                print str(module)
                                print str(parentObject)
                            else:
                                module = __import__(package+"."+fname[:-3])
                                #moduleList.append(module)
                                #print str(module.object)
                                #print str(parentObject)
                                #module.register()
                            
                    except Exception:
                        print "fail!"
                        raise
            for singlePlugin in parentObject.__subclasses__():
                print "make objectS!"
                objecting = singlePlugin()
                self.pluginsList.append(objecting)
    def getPluginClassList(self):
        return self.pluginsList
    def getPluginByName(self, pluginname):
        try:
            for plugin in self.pluginsList:
                if(plugin.getObjectname()==pluginname):
                    print "match!"
                    return plugin
        except Exception:
            print "no success by get plugin "+pluginname