from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from queries import Mdb
from bson.objectid import ObjectId
from .. import socketio
import datetime
from time import sleep

db = Mdb()

@socketio.on('joined', namespace='/')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    date = session.get('date')
    room = date 
    observer = session.get('name') 
    join_room(room)
    emit('status', {'msg': room}, room=room)
    print "JUST LOADED INTO", room
    current_state = db.queryMdb(date, observer)
    for doc in current_state:
        sendID =  '#'+doc['box']
        if doc['state']:
             emit('message', {'msg': sendID}, room=room)
        else:
             emit('unmessage', {'msg': sendID}, room=room)

@socketio.on('check', namespace='/')
def check(message):
    """Sent by a client when the user checks a box.
    The box is checked for all people in the room."""
    date = session.get('date')
    room = date 
    sendID = '#'+message['msg'] 
    emit('message', {'msg': sendID}, room=room)

#    db = Mdb()
    db.updateMdbBox(message['msg'],True,date)
    #db.insertMdb({"observer": session.get('name'), "date": datetime.datetime.now(), "box": message['msg'], "state": False, "session": date, "comment": ""})
    print "EMITTING check for",sendID, room


@socketio.on('uncheck', namespace='/')
def uncheck(message):
    """Sent by a client when the user checks a box.
    The box is checked for all people in the room."""
    date = session.get('date')
    room = date 
    sendID = '#' + message['msg']
    emit('unmessage', {'msg': sendID}, room=room)

#    db = Mdb()
    db.updateMdbBox(message['msg'],False,date)
    #db.insertMdb({"observer": session.get('name'), "date": datetime.datetime.now(), "box": message['msg'], "state": False,  "session": date, "comment": ""})
    print "EMITTING uncheck for", sendID, room

@socketio.on('updatebars', namespace='/')
def updatebar(message):
    """Sent by a client when the user checks a box.
    The progress bar is updated for everyone."""
    room = session.get('date')
    sendBar = message['bar']
    emit('pbars', {'bar': sendBar}, room=room)
    print "EMITTING new bar value for", sendBar, room

@socketio.on('updatebare', namespace='/')
def updatebar(message):
    """Sent by a client when the user checks a box.
    The progress bar is updated for everyone."""
    room = session.get('date')
    sendBar = message['bar']
    emit('pbare', {'bar': sendBar}, room=room)
    print "EMITTING new bar value for", sendBar, room


@socketio.on('left', namespace='/')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    print "THE DATE THAT WE'RE PASSING: ", message['msg']
    room = session.get('date') 
    leave_room(room)
    db.close_connection()
    #emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

