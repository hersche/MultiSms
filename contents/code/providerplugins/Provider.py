class Provider(object):
    def __init__(self):
        pass
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
        pass
    def getNeededConfig(self):
        return list()