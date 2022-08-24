from typing import List, Tuple, Set

from flask import request, render_template, redirect, url_for
from flask_jwt_extended import get_jwt
from sqlalchemy.exc import NoResultFound

from libs.jwt_functions import jwt_required_with_redirect
from models.notes import NoteModel
from models.persons import PersonModel

NOTE_ID_ERROR = "Note ID messed up."


class NoteRoutes:

    @classmethod
    def _render_write_note(
            cls,
            submit_callback,
            note=None,
            persons_visibility=None,
            csrf_token=None,
    ):
        print(csrf_token)
        if note is None:
            note = NoteModel()
        return render_template(
            'write_note.html',
            submit_callback=submit_callback,
            note=note,
            persons_visibility=persons_visibility,
            csrf_token=csrf_token,
        )

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def edit_note(cls, note_id=None):
        jwt_data = get_jwt()
        all_visibility_persons = list()
        if jwt_data.get("admin"):
            all_visibility_persons = PersonModel.get_all()

        if note_id is None:
            note = NoteModel()
        else:
            try:
                note = NoteModel.find_by_id(note_id)
            except NoResultFound:
                return {"message": NOTE_ID_ERROR}, 404

        if request.method == "POST":
            note.title = request.form["title"]
            note.content = request.form["content"]
            persons_to_on, persons_to_off = cls._visibility_changing_list(
                all_visibility_persons,
                request.form
            )
            note.add_persons_visibility(persons_to_on)
            note.remove_persons_visibility(persons_to_off)
            note.save_to_db()
            return redirect(url_for('home'))
        return cls._render_write_note(
            submit_callback=url_for('edit_note', note_id=note_id),
            note=note,
            persons_visibility=all_visibility_persons,
            csrf_token=jwt_data.get("csrf"),
        )

    @classmethod
    @jwt_required_with_redirect(admin=True)
    def delete_note(cls, note_id: int):
        jwt_data = get_jwt()
        note = NoteModel.find_by_id(note_id)
        if request.method in ["DELETE", "POST"]:
            note.delete_from_db()
            return redirect(url_for('home'))
        return render_template(
            'delete_note.html',
            submit_callback=url_for('delete_note', note_id=note_id),
            title=note.title,
            content=note.content,
            csrf_token=jwt_data.get("csrf"),
        )

    @classmethod
    def _visibility_changing_list(
            cls,
            all_persons: List["PersonModel"],
            form_dict: dict,
    ) -> Tuple[Set["PersonModel"], Set["PersonModel"]]:
        """Prepare sets of persons to add/remove visibility.

        :param all_persons: all persons who needs to be checked visibility state
        :param form_dict: dictionary containing previous state of visibility
        ('vis_previous_xxx' keys) and current state ('visibility_xxx' keys)
        of xxx in all_persons
        :return: set of persons to add visibility and set of persons to remove
        visibility
        """

        visibility_previously = {
            person.name:
                cls._bool_from_string(form_dict[f"vis_previous_{person.name}"])
            for person in all_persons
        }

        visibility_names_on = {
            key[len("visibility_"):] for key in form_dict.keys() if
            "visibility_" in key
        }

        persons_to_on = {
            PersonModel.find_by_name(name) for name in visibility_names_on
            if not visibility_previously[name]
        }
        persons_to_off = {
            PersonModel.find_by_name(name) for name in
            set(visibility_previously.keys()) - visibility_names_on
            if visibility_previously[name]
        }
        return persons_to_on, persons_to_off

    @staticmethod
    def _bool_from_string(text: str) -> bool:
        return text.lower() == "true"
