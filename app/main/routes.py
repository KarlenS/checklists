from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm


@main.route('/', methods=['GET', 'POST'])
def checklists():
    """"Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = '1'
        session['date'] = str(form.date.data)
        return redirect(url_for('.startnightform'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = '1'
        #form.date.data = session.get('date', '')
    return render_template('checklists.html', form=form)


@main.route('/startnightform')
def startnightform():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = '1'
    date = session.get('date', '')
    if name == '' or room == '' or date == '':
        return redirect(url_for('.checklists'))
    return render_template('startnightform_new.html', name=name, room=room, date=date)

@main.route('/endnightform')
def endnightform():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = '1'
    date = session.get('date', '')
    if name == '' or room == '' or date == '':
        return redirect(url_for('.checklists'))
    return render_template('endnightform_new.html', name=name, room=room, date=date)
