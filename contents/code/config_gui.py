# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_gui.ui'
#
# Created: Mon Dec 20 14:02:59 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(990, 1018)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.description = QtGui.QLabel(Form)
        self.description.setWordWrap(True)
        self.description.setObjectName(_fromUtf8("description"))
        self.verticalLayout.addWidget(self.description)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.providerContainer = QtGui.QTabWidget(Form)
        self.providerContainer.setObjectName(_fromUtf8("providerContainer"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.providerContainer.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.providerContainer)
        self.saveConfigButton = QtGui.QPushButton(Form)
        self.saveConfigButton.setObjectName(_fromUtf8("saveConfigButton"))
        self.verticalLayout.addWidget(self.saveConfigButton)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.adresssources = QtGui.QTabWidget(Form)
        self.adresssources.setObjectName(_fromUtf8("adresssources"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.adresssources.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.adresssources)
        self.saveConfigAdressButton = QtGui.QPushButton(Form)
        self.saveConfigAdressButton.setObjectName(_fromUtf8("saveConfigAdressButton"))
        self.verticalLayout.addWidget(self.saveConfigAdressButton)

        self.retranslateUi(Form)
        self.providerContainer.setCurrentIndex(0)
        self.adresssources.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Config of Multimobile", None, QtGui.QApplication.UnicodeUTF8))
        self.description.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">TextLabel</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Change Provider", None, QtGui.QApplication.UnicodeUTF8))
        self.providerContainer.setTabText(self.providerContainer.indexOf(self.tab), QtGui.QApplication.translate("Form", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.saveConfigButton.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Edit adresssources", None, QtGui.QApplication.UnicodeUTF8))
        self.adresssources.setTabText(self.adresssources.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.saveConfigAdressButton.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))

