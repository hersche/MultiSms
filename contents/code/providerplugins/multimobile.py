#!/usr/bin/python
'''
Created on 07.12.2009

@author: skamster
'''
def register():
    print "do register!"
from urllib2 import HTTPRedirectHandler
import urllib2, urllib
from Provider import Provider

class multimobile(Provider):
    '''
    classdocs stabilere klasse!
    '''
    nrlist = list()

    def setConfig(self, config):
        self.username = config.get(self.getObjectname(), self.getNeededConfig()[0])
        self.password = config.get(self.getObjectname(), self.getNeededConfig()[1])
    def getObjectname(self):
        return "Multimobile.ch"
    def addNr(self,nr):
        self.nrlist.append(nr)
    def setText(self, text):
        self.text = text
    def getText(self):
        return self.text
    def clearNrs(self):
        self.nrlist = list()
    def getNeededConfig(self):
        return list(["Phonenr", "Password"])
    def execute(self):
        if(len(self.nrlist)==0):
            raise RuntimeError("No nr's are given!")
        elif(self.text==""):
            raise RuntimeError("No text is given!")
        o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        o.add_handler(HTTPRedirectHandler())
        urllib2.install_opener( o )
        try:
    # login-data!
            p = urllib.urlencode( { 'username': self.username, 'password': self.password, 'btn_login':'Login' } )
    # perform login with params
            f = o.open( 'http://www.multimobile.ch/login',  p )
            
            f.close()
            f = o.open( 'http://www.multimobile.ch/sendsms/' )
            f.close()
            for i in range(0, len(self.nrlist)):
                p = urllib.urlencode( { 'other': self.nrlist[i], 'btn_addother':'&lt;&lt;' } )
                f = o.open( 'http://www.multimobile.ch/sendsms/', p )
                if(f.read().find("the number is invalid ")!=-1):
                    raise RuntimeError("At least one nr is invalid!")
                f.close()
        
            p = urllib.urlencode( { 'message': self.text, 'btn_send':'Send' } )
            f = o.open( 'http://www.multimobile.ch/sendsms/', p )
            if(f.read().find("successfully")==-1):
                raise RuntimeError("SMS wasn't send successfully. Don't know why..Additional: "+self.username+self.password )
            f.close()
        except Exception:
            raise

