#from pymongo import MongoClient
import pymysql.cursors
import datetime
import json


class Mdb(object):
    '''
    def __init__(self,observer="observer"):
        """initializes the database object with class variables 
        for the database and the checkbox collection"""
        self.client = MongoClient()
        self.db = self.client['checklist']
        self.col = self.db.checkbox
        self.observer = observer
    '''
    def __init__(self,observer="admin"):
        self.client = pymysql.connect(host='localhost',
                                     user='root',
                                     password='MH!kbsh85aaat',
                                     db='checklist',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        print "Closing connection"
        self.client.close()

    def queryMdb(self, session, observer):
        """takes the session/date and returns all documents for that session.
        If no documents exist for that session, ues cloneMdbTemplate to create
        documents corresponding to a new session with the current observer"""
        sql = "SELECT `*` FROM `%s`" %(session) #normal-ass mysql query, where %s will get inputted in the next line

        with self.client.cursor() as cursor:
            try:
                cursor.execute(sql)
                query_result = cursor.fetchall()
                return query_result
            except pymysql.err.ProgrammingError:
                return self.cloneMdbTemplate(observer,session)

        #docs = self.db.checkbox.find({"session": date}) #could be faster  with projection (stupid errors atm)
        #docs = self.db.checkbox.find({"session": date},{"_id":0,"box":1,"state":1,"comment":0,"observer":0,"session":0,"date":0})
        '''        
        if len(query_result) == 0:
            print "FILLING UP SESSION:",session
            return self.cloneMdbTemplate(observer, session)
        else:
            print "FOUND SESSION"
            return query_result
        ''' 

    def updateMdbBox(self, box, state, session, observer):
        """Takes the id of a box (from html), its state (checked/true or unchecked/false), and session (date)
        and updates the box to the specified state"""
        datenow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        sql = "UPDATE `%s` SET `observer`='%s',`state`='%s',`date`='%s' WHERE `box`='%s'" %(session,observer,state,datenow,box)

        with self.client.cursor() as cursor:
            cursor.execute(sql)
        
        self.client.commit()
        
        
        #result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "state": state, "observer": observer},"$currentDate":{"date": True} })
    
    def updateMdbComment(self, box, session, observer, comment=''):
        """Takes the id of a box (from html), a comment, and session (date)
        and updates the comment text for the box"""
        #KS:ok, so here we gotta do some string parsing to replace the lists in mongodb or better yet, JSON
        commentlist = self.getComment(box, session)
        print 'Current commentlist,', commentlist
        #print commentlistdb
        #commentlist = commentlistdb['comment']
        #print type(commentlist)
        print "PRINTING COMMENTS FOR BOX: ", box#," WITH COMMENTS:", commentlist
        #need to maybe store the datetime of comment too and always append
        if comment != '':
            dtimenow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            commentlist[dtimenow] = [observer,comment]

        print 'Trying to update to,', commentlist
        sql = "UPDATE `%s` SET `comment`='%s' WHERE `box`='%s'" %(session,json.dumps(commentlist),box)
        with self.client.cursor() as cursor:
            cursor.execute(sql)
        self.client.commit()

        #result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "comment": commentlist, "observer":observer},"$currentDate":{"date": True} })

    def getComment(self, box, session):
        """Takes the id of a box (from html) and session (date)
        and returns the comment field"""
        sql = "SELECT `comment` FROM `%s` WHERE `box`='%s'" %(session,box)
        with self.client.cursor() as cursor:
            cursor.execute(sql)
            
        query_result = cursor.fetchall()
        comment = query_result[0]['comment']
        query_result_deserial = json.loads(comment)
        return query_result_deserial
        #return comment

    def deleteComment(self,box,session,observer,commentid):
        commentlist = self.getComment(box,session)
        print "before deletion", commentlist
        #commentlist = commentlistdb['comment']
        commentlist.pop(commentid,None);
        print "after deletion", commentlist
        sql = "UPDATE `%s` SET `comment`='%s' WHERE `box`='%s'" %(session,json.dumps(commentlist),box)#THIS WILL HAVE TO BE JSON
        with self.client.cursor() as cursor:
            cursor.execute(sql)
        self.client.commit()
        #result = self.db.checkbox.update_one({"box": box, "session": session},{"$set": { "comment": commentlist, "observer":observer},"$currentDate":{"date": True} })



    def cloneMdbTemplate(self, observer, session):
        """takes observer name and date/session and replicates the template form
        for the given session/date returning the new form for that session"""
        sql_create = "CREATE TABLE `%s` LIKE `d19000101`" %(session)
        sql_insert = "INSERT `%s` SELECT `*` FROM `d19000101`" %(session)
        sql_update = "UPDATE `%s` SET `observer`='%s',`date`='%s'" \
            %(session,observer,datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))
        sql_select = "SELECT * FROM `%s`" %(session)

        with self.client.cursor() as cursor:
            cursor.execute(sql_create)
            cursor.execute(sql_insert)
            cursor.execute(sql_update)
            self.client.commit()
            
            cursor.execute(sql_select)
        #NEED TO UPDATE TO NEW SESSION / DATE / OBSERVER
        #cursor.execute(sql_select,(date,))
            
            query_result = cursor.fetchall()
        #temp_docs = self.db.checkbox.find({"session": "0000-00-00"})
        
        #self.updateFullTable({"observer": observer, "date": datetime.datetime.now(), "box": doc["box"], "state": False, "session": date, "comment": {}})
        
        return query_result
        #return self.db.checkbox.find({"session": date})

    '''
    def deleteMdbDoc(self, condition):
        """takes a condition and deletes the first document meeting it
        """
        result = self.db.checkbox.delete_one(condition)

    def deleteMdbDocs(self, condition):
        """takes a condition and deletes all documents meeting it
        """
        result = self.db.checkbox.delete_many(condition)
    '''
