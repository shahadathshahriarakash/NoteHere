from flask import Blueprint, render_template as rt, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            newNote = Note(data=note, userId=current_user.id)
            db.session.add(newNote)
            db.session.commit()
            flash('Note added.', category='success')

    return rt('home.html', title='Home', user=current_user)


@views.route('/about')
def about():
    return rt('about.html', title='About', user=current_user)


@views.route('/deleteNote', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.userId == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
