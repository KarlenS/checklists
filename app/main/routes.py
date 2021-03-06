from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm


@main.route('/', methods=['GET', 'POST'])
def checklists():
    """"Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['date'] = str(form.date.data)
        session['room'] = session['date']
        if form.submit_start.data:
            return redirect(url_for('.startnightform'))
        else:
            return redirect(url_for('.endnightform'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('date','')
        #form.date.data = session.get('date', '')
    return render_template('checklists.html', form=form)


@main.route('/startnightform')
def startnightform():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    date = session.get('date', '')
    room = date
    if name == '' or room == '' or date == '':
        return redirect(url_for('.checklists'))
    return render_template('startnightform_new.html', name=name, room=room, date=date)

@main.route('/endnightform')
def endnightform():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    date = session.get('date', '')
    room = date
    if name == '' or room == '' or date == '':
        return redirect(url_for('.checklists'))
    return render_template('endnightform_new.html', name=name, room=room, date=date)
