#!/usr/bin/python

from PyKDE4.kdeui import KApplication, KMessageBox
from PyKDE4.kdecore import ki18n, KCmdLineArgs, KAboutData, i18n, KCmdLineOptions
from PyQt4.QtCore import SIGNAL
from pluginmanager import PluginManager
import sys, os, ConfigParser
import providerplugins.Provider
class kontactwrapper():
    
    def file2String(self, path):
        if(os.path.isfile(path)):
            f = open(path, 'r')
            return f.read()
        else:
            KMessageBox.error(None, i18n("No path on this file"), i18n("No path"))
            raise RuntimeError("No path")

    def getRightPlugin(self, pluginname):
        if(pluginname != ""):
            plugin = self.providerPluginManager.getPluginByName(str(pluginname))
            if plugin != None:
                return plugin
            else:
                list = self.providerPluginManager.getPluginClassList()
                if len(list) > 0:
                    return list[0] 
        else:
            list = self.providerPluginManager.getPluginClassList()
            if len(list) > 0:
                return list[0]

    def __init__(self, args):
        self.getLogin()
        self.providerPluginManager = PluginManager("providerplugins","providerplugins", providerplugins.Provider.Provider)
        aboutData = KAboutData (
            "Wrapper", 
            "blubb", 
            ki18n("Wrapper for kontact"), 
            "sdaf", 
            ki18n("Displays a KMessageBox popup"), 
            KAboutData.License_GPL, 
            ki18n("(c) 2010"), 
            ki18n("This is a wrapper for kontact to access the multimobileservice"), 
            "http://puzzle.ch", 
            "hersche@puzzle.ch"
        )
 
        KCmdLineArgs.init(sys.argv, aboutData)
        
        cmdoptions = KCmdLineOptions()
        cmdoptions.add("nr <speed>", ki18n("The phone nr"))
        cmdoptions.add("smsfile <file>", ki18n("The smsfile"))
        cmdoptions.add("smstext <text>", ki18n("The smstext"))
        cmdoptions.add("plugin <string>", ki18n("The pluginname"))
        KCmdLineArgs.addCmdLineOptions(cmdoptions)
        app = KApplication()
        lineargs = KCmdLineArgs.parsedArgs()
        plugin = self.getRightPlugin(lineargs.getOption("plugin"))
        plugin.addNr(lineargs.getOption("nr"))
        if lineargs.getOption("smsfile") != "":
            plugin.setText(self.file2String(lineargs.getOption("smsfile")))
        elif lineargs.getOption("smstext") != "":
            plugin.setText(lineargs.getOption("smstext"))
        else:
            KMessageBox.error(None, i18n("No text defined.."), i18n("Text undefined"))
            raise RuntimeError("No text defined!")
        plugin.setConfig(self.config)
        try:
            plugin.execute()
            KMessageBox.information(None, i18n("Your SMS was sendet successfull to "+lineargs.getOption("nr")+" with Plugin "+plugin.getObjectname()), i18n("Success"))
        except Exception, e:
            KMessageBox.error(None, i18n(e), i18n("Error"))
    def getLogin(self):
        if(os.path.isfile(os.getenv("HOME") + "/.multimobile.cfg")):
            try:
                self.config = ConfigParser.ConfigParser()
                self.config.readfp(open(os.getenv("HOME") + "/.multimobile.cfg"))
            except Exception, e:
                from config import config
                self.startAssistant = config(self.providerPluginManager, self.adressplugins, False)
                self.startAssistant.show()
                self.connect(self.startAssistant, SIGNAL("finished(int)"), self.getLogin) 

        else:
            from config import config
            self.startAssistant = config(self.providerPluginManager, self.adressplugins, True)
            self.startAssistant.show()
            self.connect(self.startAssistant, SIGNAL("finished(int)"), self.getLogin)


blubb = kontactwrapper(sys.argv)

