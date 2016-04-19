from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio


@socketio.on('joined', namespace='/')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('check', namespace='/')
def uncheck(message):
    """Sent by a client when the user checks a box.
    The box is checked for all people in the room."""
    room = session.get('room')
    sendID = '#'+message['msg'] 
    emit('unmessage', {'msg': sendID}, room=room)
    print "EMITTING uncheck for",sendID


@socketio.on('uncheck', namespace='/')
def check(message):
    """Sent by a client when the user checks a box.
    The box is checked for all people in the room."""
    room = session.get('room')
    sendID = '#' + message['msg']
    emit('message', {'msg': sendID}, room=room)
    print "EMITTING check for", sendID

@socketio.on('updatebar', namespace='/')
def updatebar(message):
    """Sent by a client when the user checks a box.
    The progress bar is updated for everyone."""
    room = session.get('room')
    sendBar = message['bar']
    emit('pbar', {'bar': sendBar}, room=room)
    print "EMITTING new bar value for", sendBar

@socketio.on('left', namespace='/')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

