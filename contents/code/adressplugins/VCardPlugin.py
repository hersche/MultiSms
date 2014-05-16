'''
Created on 12.03.2010

@author: skamster
'''
from AdressPlugin import AdressPlugin
from vobject.base import ParseError
import vobject
class VCardPlugin(AdressPlugin):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def getObjectname(self):
        return "VcardPlugin"
    def setPath(self, path):
        self.path = path
    def getNeededConfig(self):
        return list(["Path"])
    def getAdressList(self):
        file = open("/home/skamster/Dokumente/adressen_tmp/addressbook.vcf", "r")
        ad = vobject.readComponents(file)
        self.contactList = list()
        try:
            for x in ad:
                telContact = {}
                telContact['prename'] = self._extractAtt(x, 'x.n.value.given')
                telContact['lastname'] = self._extractAtt(x, 'x.n.value.family')
                try:
                    for tel in x.contents['tel']:
                        if tel.params['TYPE'] in [['CELL', 'VOICE'], ['VOICE', 'CELL'], ['CELL'], ['VOICE']]:
                            telContact['phone'] = tel.value
                except KeyError:
                    pass    
                if(telContact.has_key("phone")):
                    self.contactList.append(telContact['phone'] + "; ")
                    self.contactList.append("<" + telContact['prename'] + " " + telContact['lastname'] + "> " + telContact['phone'] + "; ")
                    self.contactList.append("<" + telContact['lastname'] + " " + telContact['prename'] + "> " + telContact['phone'] + "; ")
        except ParseError, message:
            print message
            pass
        return self.contactList
    def _extractAtt(self, x, st):
        """
        Supporting function for pulling information out of a attribute
        Gets around problems with non available attributes without the need for checking this beforehand for each attribute.
        @author: Michael Pilgermann alias Kichkasch
        """
        try:
            ret = None
            exec "ret = " + st
            return ret
        except AttributeError:
            return ''
