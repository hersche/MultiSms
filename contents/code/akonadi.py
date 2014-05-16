from PyKDE4 import akonadi

class akonadi4sms():
    def __init__(self):
        self.akonadiObj = akonadi.Akonadi
        self.collectionModel = self.akonadiObj.CollectionModel()
        self.collectionFilter = self.akonadiObj.CollectionFilterProxyModel()
        self.collectionFilter.setSourceModel(self.collectionModel)
        self.collectionFilter.addMimeTypeFilter("text/directory")
    def getModel(self):
        return self.collectionFilter