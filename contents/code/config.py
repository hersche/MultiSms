import ConfigParser, os
from config_gui import Ui_Form
from PyQt4 import QtGui
class config(QtGui.QDialog):
    def __init__(self,providerManager,adresssManager, firstTime=False):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setMinimumWidth(389)
        self.setMinimumHeight(237)
        self.providerObject = providerManager
        self.adressObject = adresssManager
        self.ui.providerContainer.clear()
        if(os.path.isfile(os.getenv("HOME") + "/.multimobile.cfg")):
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.getenv("HOME") + "/.multimobile.cfg"))
        else:
            config = None
        for provider in self.providerObject.getPluginClassList():
            tab = QtGui.QWidget()
            tab.setObjectName(provider.getObjectname())
            layout = QtGui.QVBoxLayout()
            for singleConfig in provider.getNeededConfig():
                label = QtGui.QLabel()
                label.setObjectName(provider.getObjectname()+singleConfig+"label")
                label.setText(singleConfig)
                textField = QtGui.QLineEdit()
                textField.setObjectName(provider.getObjectname()+singleConfig+"text")
                # @TODO make that clean!!
                try:
                    if config is not None:
                        textField.setText(config.get(provider.getObjectname(), singleConfig))
                    else:
                        textField.setText("")
                except ConfigParser.NoSectionError:
                    textField.setText("")
                layout.addWidget(label)
                layout.addWidget(textField)
            tab.setLayout(layout)         
            self.ui.providerContainer.addTab(tab, provider.getObjectname())
        self.ui.adresssources.clear()  
        for adressplugin in self.adressObject.getPluginClassList():
            tab = QtGui.QWidget()
            tab.setObjectName(adressplugin.getObjectname())
            layout = QtGui.QVBoxLayout()
            for singleConfig in adressplugin.getNeededConfig():
                label = QtGui.QLabel()
                label.setObjectName(adressplugin.getObjectname()+singleConfig+"label")
                label.setText(singleConfig)
                textField = QtGui.QLineEdit()
                textField.setObjectName(adressplugin.getObjectname()+singleConfig+"text")
                try:
                    if config is not None:
                        textField.setText(config.get(adressplugin.getObjectname(), singleConfig))
                    else:
                        textField.setText("")
                except ConfigParser.NoSectionError:
                    textField.setText("")
                layout.addWidget(label)
                layout.addWidget(textField)
            tab.setLayout(layout)
            self.ui.adresssources.addTab(tab, adressplugin.getObjectname())        
        #self.ui.editState.setText("You do edit settings for: "+str(self.ui.providerlist.selectedItems()[0].text()))
        normalDescription = "This is the normal description"
        firstTimeDescription = "This is the first time you start the programm."
       # if(firstTime):
           # self.ui.description.setText(firstTimeDescription)
        #else:
         #   self.ui.description.setText(normalDescription)
        self.ui.saveConfigButton.clicked.connect(self.providerSaveButtonClicked)
        self.ui.saveConfigAdressButton.clicked.connect(self.adressSaveButtonClicked)
        self.ui.providerContainer.currentChanged.connect(self.tabChanged)
        #self.connect(self.ui.saveConfigButton, QtCore.SIGNAL("clicked()"), self.providerSaveButtonClicked)
        #self.connect(self.ui.saveConfigAdressButton, QtCore.SIGNAL("clicked()"), self.adressSaveButtonClicked)
        #self.connect(self.ui.providerContainer, QtCore.SIGNAL("currentChanged(int)"), self.tabChanged)
       # self.connect(self.ui.providerlist, QtCore.SIGNAL("itemSelectionChanged  ()"), self.onClickProviderlistUpdateFields)
       
    def adressSaveButtonClicked(self):
        containerWidget = self.ui.adresssources.currentWidget()
        provider = self.adressObject.getPluginByName(containerWidget.objectName())
        config = ConfigParser.ConfigParser()
        file = open(os.getenv("HOME") + "/.multimobile.cfg", "r")
        config.readfp(file)
        file.close()
        if not config.has_section(str(containerWidget.objectName())):
            config.add_section(str(containerWidget.objectName()))
        for currentConfig in provider.getNeededConfig():
            textContent = containerWidget.findChild(QtGui.QLineEdit, containerWidget.objectName()+currentConfig+"text").text()
            config.set(str(containerWidget.objectName()), currentConfig, unicode(textContent))
        file = open(os.getenv("HOME") + "/.multimobile.cfg", "w")
        config.write(file)
        file.flush()
        self.close()

                
    def providerSaveButtonClicked(self):
        containerWidget = self.ui.providerContainer.currentWidget()
        provider = self.providerObject.getPluginByName(containerWidget.objectName())
        config = ConfigParser.ConfigParser()
        file = open(os.getenv("HOME") + "/.multimobile.cfg", "r")
        config.readfp(file)
        file.close()
        if not config.has_section(str(containerWidget.objectName())):
            config.add_section(str(containerWidget.objectName()))
        for currentConfig in provider.getNeededConfig():
            textContent = containerWidget.findChild(QtGui.QLineEdit, containerWidget.objectName()+currentConfig+"text").text()
            config.set(str(containerWidget.objectName()), currentConfig, unicode(textContent))
        file = open(os.getenv("HOME") + "/.multimobile.cfg", "w")
        config.write(file)
        file.flush()
        self.close()
    def tabChanged(self, tabid):
        containerWidget = self.ui.providerContainer.currentWidget()
        provider = self.providerObject.getPluginByName(containerWidget.objectName())
        print  containerWidget.findChild(QtGui.QLineEdit, containerWidget.objectName()+provider.getNeededConfig()[0]+"text").text()
    def onClickProviderlistUpdateFields(self):
        try:
            currentProvider = str(self.ui.providerlist.selectedItems()[0].text())
            currentProviderObject = self.providerObject.getPluginByName(currentProvider)
            print currentProviderObject.getNeededConfig()[0] 
            self.ui.updateConfigArea(currentProviderObject.getNeededConfig())
            self.ui.editState.setText("You do edit settings for: "+currentProvider)
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.getenv("HOME") + "/.multimobile.cfg"))
        except Exception, e:
            print e

