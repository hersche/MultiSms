
from urllib2 import HTTPRedirectHandler
import urllib2, urllib
from Provider import Provider

class studentsch(Provider):
    nrlist = list()
    #def __init__(self, username, password):
    #   self.username = username
    #  self.password = password

       
    def setUsername(self, username):
        self.username = username
    def setPassword(self, password):
        self.password = password
    def setConfig(self, config):
            self.username = config.get(self.getObjectname(), self.getNeededConfig()[0])
            self.password = config.get(self.getObjectname(), self.getNeededConfig()[1])
    def getNeededConfig(self):
        return list(["Username", "Password"])
    def getObjectname(self):
        return "Students.ch"
    def addNr(self,nr):
        self.nrlist.append(unicode(nr).encode("utf-8"))
    def setText(self, text):
        self.text = unicode(text).encode("utf-8")
    def getText(self):
        return self.text
    def clearNrs(self):
        self.nrlist = list()
    def execute(self):
        o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        o.add_handler(HTTPRedirectHandler())
        urllib2.install_opener( o )
        try:
            p = urllib.urlencode( { 'login': "" } )
            f = o.open( 'http://www.students.ch/#',  p )
            f.close()
    # login-data!
            p = urllib.urlencode( { 'username': self.username, 'password': self.password, 'login':'Login' } )
    # perform login with params
            f = o.open( 'http://www.students.ch/#',  p )
            
            f.close()
            for i in range(0, len(self.nrlist)):
                p = urllib.urlencode( { 'sms': "" } )
                f = o.open( 'http://www.students.ch/adminpanel/user/messages', p )
                f.close()
                p = urllib.urlencode( { 'sms': "" } )
                f = o.open( 'http://www.students.ch/adminpanel/user/messages/sms', p )
                f.close()
                p = urllib.urlencode( { 'value': self.nrlist[i]} )
                f = o.open( 'http://www.students.ch/ruleserver/mPhoneRule', p )
                f.close()
                p = urllib.urlencode( { 'recipient_mobile': self.nrlist[i], 'body': self.text, 'sms_state':"2", 'submit_button':"senden" } )
                f = o.open( 'http://www.students.ch/adminpanel/user/messages/sms', p )
                f.close()

        except Exception:
            raise

