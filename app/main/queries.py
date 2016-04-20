from pymongo import MongoClient

class Mdb(object):

    def __init__(self,observer="observer"):
        self.client = MongoClient()
        self.db = self.client['checklist']
        self.col = self.db.checkbox
        self.observer = observer

    def queryMdb(self, date):
        #to query/find data
        return self.db.checkbox.find()
    
    def updateMdbBox(self, box, state):
        result = self.db.checkbox.update_one({"box": box},{"$set": { "state": state },"$currentDate":{"date": True} })

    def insertMdb(self, doc):
        result = self.db.checkbox.insert_one(doc)

    def deleteMdbDoc(self, condition):
        result = self.db.checkbox.delete_one(condition)

    def deleteMdbDocs(self, condition):
        result = self.db.checkbox.delete_many(condition)
