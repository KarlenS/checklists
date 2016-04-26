from pymongo import MongoClient
import datetime

class Mdb(object):

    def __init__(self,observer="observer"):
        """initializes the database object with class variables 
        for the database and the checkbox collection"""
        self.client = MongoClient(host="mongo", port=27017)
        self.db = self.client['checklist']
        self.col = self.db.checkbox
        self.observer = observer

    def queryMdb(self, date, observer):
        """takes the session/date and returns all documents for that session.
        If no documents exist for that session, ues cloneMdbTemplate to create
        documents corresponding to a new session with the current observer"""
        docs = self.db.checkbox.find({"session": date}) #could be faster  with projection (stupid errors atm)
        #docs = self.db.checkbox.find({"session": date},{"_id":0,"box":1,"state":1,"comment":0,"observer":0,"session":0,"date":0})
        if docs.count() == 0:
            print "FILLING UP SESSION:",date
            return self.cloneMdbTemplate(observer, date)
        else:
            print "FOUND SESSION"
            return docs
    
    def updateMdbBox(self, box, state, session):
        """Takes the id of a box (from html), its state (checked/true or unchecked/false), and session (date)
        and updates the box to the specified state"""
        result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "state": state },"$currentDate":{"date": True} })
    
    def cloneMdbTemplate(self, observer, date):
        """takes observer name and date/session and replicates the template form
        for the given session/date returning the new form for that session"""
        temp_docs = self.db.checkbox.find({"session": "0000-00-00"})
        for doc in temp_docs:
            self.insertMdb({"observer": observer, "date": datetime.datetime.now(), "box": doc["box"], "state": False, "session": date, "comment": ""})
        return self.db.checkbox.find({"session": date}) 

    def insertMdb(self, doc):
        """takes a single document and inserts it into the collection
        """
        result = self.db.checkbox.insert_one(doc)

    def deleteMdbDoc(self, condition):
        """takes a condition and deletes the first document meeting it
        """
        result = self.db.checkbox.delete_one(condition)

    def deleteMdbDocs(self, condition):
        """takes a condition and deletes all documents meeting it
        """
        result = self.db.checkbox.delete_many(condition)
