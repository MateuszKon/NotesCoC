from flask import request, render_template, redirect, url_for

from models.notes import NoteModel


NOTE_ID_ERROR = "Note ID messed up."


class NoteRoutes:

    @classmethod
    def _render_write_note(cls, submit_callback, title=None, content=None):
        return render_template(
            'write_note.html',
            submit_callback=submit_callback,
            title=title or "",
            content=content or "",
        )

    @classmethod
    def new_note(cls):
        if request.method == "POST":
            note = NoteModel(
                title=request.form["title"],
                content=request.form["content"],
            )
            note.save_to_db()
            return redirect(url_for('home'))
        else:
            return cls._render_write_note(
                submit_callback=url_for('new_note')
            )

    @classmethod
    def edit_note(cls, note_id):
        note = NoteModel.find_by_id(note_id)
        if request.method == "POST":
            note.title = request.form["title"]
            note.content = request.form["content"]
            note.save_to_db()
            return redirect(url_for('home'))
        else:
            return cls._render_write_note(
                submit_callback=url_for('edit_note', note_id=note_id),
                title=note.title,
                content=note.content,
            )

    @classmethod
    def delete_note(cls, note_id: int):
        note = NoteModel.find_by_id(note_id)
        if request.method in ["DELETE", "POST"]:
            note.delete_from_db()
            return redirect(url_for('home'))
        else:
            return render_template(
                'delete_note.html',
                submit_callback=url_for('delete_note', note_id=note_id),
                title=note.title,
                content=note.content,
            )
