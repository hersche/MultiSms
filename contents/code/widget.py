from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import KMessageBox
from PyKDE4.kdecore import i18n, KStandardDirs
from pluginmanager import PluginManager
import providerplugins.Provider
import adressplugins.AdressPlugin
import ConfigParser, os, re

 
class Multimobilewidget(plasmascript.Applet):
    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)
 
    def init(self):
        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.Square)
        self.theme = Plasma.Svg(self)
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)
        self.getLogin()
        self.setHasConfigurationInterface(True)
        self.label = Plasma.Label(self.applet)
        self.label.setText(i18n("Welcome to the Multimobilewidget"))
        nrlabel = Plasma.Label(self.applet)
        nrlabel.setText(i18n("Phonenr(s)"))
        self.messagelabel = Plasma.Label(self.applet)
        self.messagelabel.setText(i18n("Message - 0 signs used"))
        self.nrfield = Plasma.LineEdit()
        self.messageText = Plasma.TextEdit(self.applet)
        self.messageText.nativeWidget()
        sendButton = Plasma.PushButton(self.applet)
        sendButton.setText(i18n("Send the SMS!"))
        sendButton.resize(20, 40)
        configButton = Plasma.PushButton(self.applet)
        configButton.setText("Config")
        configButton.resize(20, 40)
        self.layout.addItem(self.label)
        self.layout.addItem(nrlabel)
        self.layout.addItem(self.nrfield)
        self.layout.addItem(self.messagelabel)
        self.layout.addItem(self.messageText)
        self.layout.addItem(sendButton)
        self.layout.addItem(configButton)
        self.applet.setLayout(self.layout)
        self.connect(sendButton, SIGNAL("clicked()"), self.onSendClick)
        self.connect(configButton, SIGNAL("clicked()"), self.onConfigClick)
        self.connect(self.messageText, SIGNAL("textChanged()"), self.onTextChanged)
        fullPath = str(self.package().path())
        self.providerPluginManager = PluginManager("multimobilewidget/contents/code/providerplugins/","", providerplugins.Provider.Provider)
        self.providerpluginlist = self.providerPluginManager.getPluginClassList()
        for provider in self.providerpluginlist:
            self.ui.providerList.addItem(provider.getObjectname())
            print provider.getObjectname()
            self.ui.providerList.setCurrentRow(0)
        self.adressplugins = PluginManager("multimobilewidget/contents/code/adressplugins/","", adressplugins.AdressPlugin.AdressPlugin)
        self.adresspluginlist = self.adressplugins.getPluginClassList()
        self.adressList = list()
        
        
    def onConfigClick(self):
        from config import config
        self.startAssistant = config(self.providerPluginManager, self.adressplugins)
        self.startAssistant.show()
        self.connect(self.startAssistant, SIGNAL("finished(int)"), self.getLogin)
    def connectToAkonadi(self):
        self.akonadiEngine = Plasma.DataEngine()
        self.akonadiEngine.setName("akonadi")
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
#                    self.notification.setText(i18n("Wurde erfolgreich an <i>%1</i> geschickt!").arg(savenr ))
#                    self.notification.setTitle("Erfolg!")
#                    self.notification.sendEvent()
                    KMessageBox.information(None, i18n("SMS sendet successfully to " + savenr + ". Service: "+sms.getProvidername()), i18n("Success!"))
                except Exception, error:
                    KMessageBox.error(None, i18n(error.message), i18n("Sendproblems"))
                self.ui.phonenr.clear()
                self.ui.smstext.clear()
            else:
                KMessageBox.error(None, i18n("Please fill in a phonenr"), i18n("Please fill in a phonenr"))
        else:
            KMessageBox.error(None, i18n("Please fill in a Text"), i18n("Please fill in a Text"))
            
        
    def onTextChanged(self):
        tmp = self.messageText.nativeWidget()
        if(len(tmp.toPlainText()) < 160):
            self.messagelabel.setText(i18n("Message - ") + str(len(tmp.toPlainText())) + i18n(" signs used"))
        else:
            # count how many sms are used and update the status
            self.messagelabel.setText(i18n("Message - ") + str(len(tmp.toPlainText())) + i18n(" signs used"))
            
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

 
def CreateApplet(parent):
    return Multimobilewidget(parent)
