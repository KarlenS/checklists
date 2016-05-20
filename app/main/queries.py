from pymongo import MongoClient
import datetime

class Mdb(object):

    def __init__(self,observer="observer"):
        """initializes the database object with class variables 
        for the database and the checkbox collection"""
        self.client = MongoClient()
        self.db = self.client['checklist']
        self.col = self.db.checkbox
        self.observer = observer

    def close_connection(self):
        print "Closing connection"
        self.client.close()

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
    
    def updateMdbBox(self, box, state, session, observer):
        """Takes the id of a box (from html), its state (checked/true or unchecked/false), and session (date)
        and updates the box to the specified state"""
        result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "state": state, "observer": observer},"$currentDate":{"date": True} })
    
    def updateMdbComment(self, box, session, observer, comment=''):
        """Takes the id of a box (from html), a comment, and session (date)
        and updates the comment text for the box"""

        
        commentlistdb = self.getComment(box, session)
        #print commentlistdb
        commentlist = commentlistdb['comment']
        #print type(commentlist)
        print "PRINTING COMMENTS FOR BOX: ", box#," WITH COMMENTS:", commentlist
        #need to maybe store the datetime of comment too and always append
        if comment != '':
            dtimenow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            commentlist[dtimenow] = [observer,comment]

        result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "comment": commentlist, "observer":observer},"$currentDate":{"date": True} })

    def getComment(self, box, session):
        """Takes the id of a box (from html) and session (date)
        and returns the comment field"""
        return self.db.checkbox.find_one({"box": box, "session": session},{"comment": 1, "observer":1})

    def deleteComment(self,box,session,observer,commentid):
        commentlistdb = self.getComment(box,session)
        commentlist = commentlistdb['comment']
        commentlist.pop(commentid,None);
        result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "comment": commentlist, "observer":observer},"$currentDate":{"date": True} })



    def cloneMdbTemplate(self, observer, date):
        """takes observer name and date/session and replicates the template form
        for the given session/date returning the new form for that session"""
        temp_docs = self.db.checkbox.find({"session": "0000-00-00"})
        for doc in temp_docs:
            self.insertMdb({"observer": observer, "date": datetime.datetime.now(), "box": doc["box"], "state": False, "session": date, "comment": {}})
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
