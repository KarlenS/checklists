from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm


@main.route('/', methods=['GET', 'POST'])
def checklists():
    """"Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.startnightform'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('checklists.html', form=form)


@main.route('/startnightform')
def startnightform():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.checklists'))
    return render_template('startnightform_new.html', name=name, room=room)

@main.route('/endnightform')
def endnightform():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.checklists'))
    return render_template('endnightform_new.html', name=name, room=room)
