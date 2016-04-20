from pymongo import MongoClient

class Mdb(object):

    def __init__(self,observer="karlen"):
        self.client = MongoClient()
        self.db = self.client['checklist']
        self.observer = observer

    def queryMdb(self, date):
        #to query/find data
        for doc in self.db.checkbox.find({"observer":"karlen"}):
            print doc
    
    def updateMdbBox(self, doc):
        result = self.db.checkbox.update_one({"box": "90mint1pedlights"},{"$set": { "state": False },"$currentDate":{"date": True} })

    def insertMdb(self, doc):
        result = self.db.checkbox.insert_one(doc)
        print result

    def deleteMdbDoc(self, condition):
        result = self.db.delete_one(condition)
