#!/usr/bin/env python
# coding=UTF-8
'''
Created on 05.01.2010

@author: skamster
'''

import sys, ConfigParser, os, re
from PyQt4.QtCore import SIGNAL, QStringList
from PyQt4.QtGui import QWidget, QGraphicsLinearLayout
from standalone_gui import Ui_MainWindow
from pluginmanager import PluginManager
from PyKDE4.kdeui import KMessageBox, KCompletion, KAboutApplicationDialog, KGlobalSettings, KApplication, KMainWindow
from PyKDE4.kdecore import KAboutData, i18n, ki18n, KCmdLineArgs
from PyKDE4 import akonadi
import providerplugins.Provider
import adressplugins.AdressPlugin

class standalone(KMainWindow):
    def __init__(self, parent=None):
       # QWidget.__init__(sip.simplewrapper)
        KMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.providerPluginManager = PluginManager("providerplugins","providerplugins", providerplugins.Provider.Provider)
        self.providerpluginlist = self.providerPluginManager.getPluginClassList()
        for provider in self.providerpluginlist:
            self.ui.providerList.addItem(provider.getObjectname())
            self.ui.providerList.setCurrentRow(0)
        self.adressplugins = PluginManager("adressplugins","adressplugins", adressplugins.AdressPlugin.AdressPlugin)
        self.adresspluginlist = self.adressplugins.getPluginClassList()
        self.adressList = list()
        for adressplugin in self.adresspluginlist:
            for adress in adressplugin.getAdressList():
                self.adressList.append(adress)



        self.co = akonadi.Akonadi.Collection()
        self.collectfetch = akonadi.Akonadi.CollectionFetchJob(akonadi.Akonadi.Collection().root(), akonadi.Akonadi.CollectionFetchJob.Recursive)
        self.collectionFetcherScope = akonadi.Akonadi.CollectionFetchScope()
        self.collectionFetcherScope.setContentMimeTypes(QStringList("text/directory"))
        self.collectfetch.setFetchScope(self.collectionFetcherScope)
        self.itemfetch = akonadi.Akonadi.ItemFetchJob(akonadi.Akonadi.Collection().root())

        completion = KCompletion()
        completion.setItems(self.adressList)
        completion.setCompletionMode(KGlobalSettings.CompletionPopupAuto)
        completion.setParent(self.ui.phonenr)
        self.ui.phonenr.setCompletionObject(completion)
        self.ui.contactList2.addItems(self.adressList)
        
        self.aboutData = KAboutData (
            "Multimobilewidget",
            "blubb",
            ki18n("Multimobilewidget"),
            "0.1.0",
            ki18n("Sends sms over the multimobileservice"),
            KAboutData.License_GPL,
            ki18n("(c) 2010"),
            ki18n("This is a app could send sms over the multimobileservices. It's (should be) fully integrated in the kde-world!"),
            "http://puzzle.ch",
            "hersche@puzzle.ch"
        )
        self.aboutData.addAuthor(ki18n("Vinzenz Hersche"), ki18n(""), "hersche@puzzle.ch", "http://death-head.ch")
        self.aboutData.addCredit(ki18n("#pyqt, #akonadi in freenode"), ki18n("Help on several beginnerproblems - thank you!"))
        self.aboutData.addCredit(ki18n("Tschan Daniel"), ki18n("Helps on a akonadi-related signal/slot-question"))
        self.ui.actionAbout.triggered.connect(self.onAboutClick)
        self.ui.actionSettings.triggered.connect(self.onConfigClick)
        self.ui.sendbutton.clicked.connect(self.onSendClick)
        self.ui.smstext.textChanged.connect(self.onTextChanged)
        self.itemfetch.result.connect(self.itemFetched)
        self.collectfetch.collectionsReceived.connect(self.collectionFetched)
        #self.connect(self.ui.actionAbout, SIGNAL("triggered()"), self.onAboutClick)
        #self.connect(self.ui.actionSettings, SIGNAL("triggered()"), self.onConfigClick)
        #self.connect(self.ui.sendbutton, SIGNAL("clicked()"), self.onSendClick)
        #self.connect(self.ui.smstext, SIGNAL("textChanged()"), self.onTextChanged)
        #self.connect(self.itemfetch,  SIGNAL("result(KJob*)"), self.itemFetched)
        #self.connect(self.collectfetch,  SIGNAL("collectionsReceived(const Akonadi::Collection::List&)"), self.collectionFetched)
        self.getLogin()
        self.itemfetch.fetchScope().fetchFullPayload()


    def itemFetched(self, blubb):
        for item in blubb.items():
            print str(item.mimeType())
            
    def collectionFetched(self, thelist):
        self.itemfetch.setCollection(thelist[0])
        self.itemfetch.doStart()
    def onConfigClick(self):
        from config import config
        self.startAssistant = config(self.providerPluginManager, self.adressplugins)
        self.startAssistant.show()
        self.connect(self.startAssistant, SIGNAL("finished(int)"), self.getLogin)
    
    def onAboutClick(self):
        self.kaboutUi = KAboutApplicationDialog(self.aboutData)
        self.kaboutUi.show()

    def onSendClick(self):
        for provider in self.providerpluginlist:
            if(provider.getObjectname() == self.ui.providerList.selectedItems()[0].text()):
                sms = provider
        if self.ui.smstext.toPlainText() != "":
            if self.ui.phonenr.text() != "":
                self.getLogin()
                try:
                    sms.setConfig(self.config)
                except Exception:
                    self.onConfigClick()
                    return
                sms.clearNrs()
                for nr in re.findall("(\+\d*)", self.ui.phonenr.text()):
                    sms.addNr(nr)
                sms.setText(self.ui.smstext.toPlainText())
                savenr = self.ui.phonenr.text()
                try:
                    sms.execute()
                    KMessageBox.information(None, i18n("SMS sendet successfully to " + savenr + ". Service: "+sms.getObjectname()), i18n("Success!"))
                except Exception, error:
                    KMessageBox.error(None, i18n(error.message), i18n("Sendproblems"))
                self.ui.phonenr.clear()
                self.ui.smstext.clear()
            else:
                KMessageBox.error(None, i18n("Please fill in a phonenr"), i18n("Please fill in a phonenr"))
        else:
            KMessageBox.error(None, i18n("Please fill in a Text"), i18n("Please fill in a Text"))
            
    def onTextChanged(self):
        if(len(self.ui.smstext.toPlainText()) < 160):
            self.ui.counter.setText(i18n("Message - ") + unicode(len(self.ui.smstext.toPlainText())) + i18n(" signs used"))
        else:
            # count how many sms are used and update the status
            self.ui.counter.setText(i18n("Message - ") + unicode(len(self.ui.smstext.toPlainText())) + i18n(" signs used"))

    def getLogin(self):
        if(os.path.isfile(os.getenv("HOME") + "/.multimobile.cfg")):
            try:
                self.config = ConfigParser.ConfigParser()
                self.config.readfp(open(os.getenv("HOME") + "/.multimobile.cfg"))
            except Exception, e:
                print e 
                from config import config
                self.startAssistant = config(self.providerPluginManager, self.adressplugins, False)
                self.startAssistant.show()
                self.connect(self.startAssistant, SIGNAL("finished(int)"), self.getLogin) 

        else:
            from config import config
            self.startAssistant = config(self.providerPluginManager, self.adressplugins, True)
            self.startAssistant.show()
            self.connect(self.startAssistant, SIGNAL("finished(int)"), self.getLogin)
if __name__ == '__main__':
    aboutData = KAboutData (
        "Multimobilewidget",
        "blubb",
        ki18n("Multimobilewidget"),
        "0.1.0",
        ki18n("Sends sms over the multimobileservice"),
        KAboutData.License_GPL,
        ki18n("(c) 2010"),
        ki18n("This is a app could send sms over the multimobileservices. It's (should be) fully integrated in the kde-world!"),
        "http://puzzle.ch",
        "hersche@puzzle.ch"
    )
    
    KCmdLineArgs.init(sys.argv, aboutData)
    app = KApplication()
    test = standalone()
    test.show()
    sys.exit(app.exec_())
