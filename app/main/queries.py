#from pymongo import MongoClient
import pymysql.cursors
import datetime
import json


class Mdb(object):

    def __init__(self,observer="admin"):
        self.client = pymysql.connect(host='localhost',
                                     user='root',
                                     password='password',
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

    def updateMdbBox(self, box, state, session, observer):
        """Takes the id of a box (from html), its state (checked/true or unchecked/false), and session (date)
        and updates the box to the specified state"""
        datenow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        sql = "UPDATE `%s` SET `observer`='%s',`state`='%s',`date`='%s' WHERE `box`='%s'" %(session,observer,state,datenow,box)

        with self.client.cursor() as cursor:
            cursor.execute(sql)
        
        self.client.commit()
        
        
    
    def updateMdbComment(self, box, session, observer, comment=''):
        """Takes the id of a box (from html), a comment, and session (date)
        and updates the comment text for the box"""
        commentlist = self.getComment(box, session)

        if comment != '':
            dtimenow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            commentlist[dtimenow] = [observer,comment]

        print 'Trying to update to,', commentlist
        sql = "UPDATE `%s` SET `comment`='%s' WHERE `box`='%s'" %(session,json.dumps(commentlist),box)
        with self.client.cursor() as cursor:
            cursor.execute(sql)
        self.client.commit()

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

    def deleteComment(self,box,session,observer,commentid):
        commentlist = self.getComment(box,session)
        commentlist.pop(commentid,None);
        sql = "UPDATE `%s` SET `comment`='%s' WHERE `box`='%s'" %(session,json.dumps(commentlist),box)#THIS WILL HAVE TO BE JSON

        with self.client.cursor() as cursor:
            cursor.execute(sql)
        self.client.commit()


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
            
            query_result = cursor.fetchall()
        
        return query_result
