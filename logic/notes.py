import re
from typing import List, Tuple, Set

from flask import redirect, url_for, Response

from models import SubjectModel
from models.notes import NoteModel
from models.persons import PersonModel
from routes.i_request import RequestPayload, ResponseData, RequestData
from routes.notes import INoteRouteLogic
from schemas.notes import (
    NoteSchema,
    note_schema,
    note_schema_without_visibility,
)
from schemas.subjects import subject_name_schema


NOTE_ID_ERROR = "Note ID messed up."


class NoteLogic(INoteRouteLogic):

    @classmethod
    def render_edit_note(
            cls,
            data: RequestData,
            note_id: int = None
    ) -> ResponseData:
        if note_id is None:
            note = NoteModel()
        else:
            note = NoteModel.find_by_id(note_id)

        all_subjects = SubjectModel.get_all()

        note_schema_ = cls._get_note_schema(data.context.get("jwt_admin"))

        return ResponseData(
            'write_note.html',
            resource={
                'note': note_schema_.dump(note),
                'all_subjects': subject_name_schema.dump(
                    all_subjects,
                    many=True,
                )
            },
            submit_callback=url_for('edit_note', note_id=note.id),
        )

    @classmethod
    def save_note(
            cls,
            data: RequestData,
            note_id: int = None
    ) -> Response:
        if note_id is None:
            note = NoteModel()
        else:
            note = NoteModel.find_by_id(note_id)

        # title and content:
        note.title = data.data["title"]
        note.content = data.data["content"]

        # persons visibility:
        cls._change_note_visibility(note, data.data)

        # subjects:
        cls._change_note_subjects(note, data.data)

        note.save_to_db()
        return redirect(url_for('home'))

    @classmethod
    def render_delete_note_confirmation(
            cls,
            data: RequestData,
            note_id: int
    ) -> ResponseData:
        note = NoteModel.find_by_id(note_id)

        note_schema_ = cls._get_note_schema(data.context.get("jwt_admin"))

        return ResponseData(
            'delete_note.html',
            resource=note_schema_.dump(note),
            submit_callback=url_for('delete_note', note_id=note_id),
        )

    @classmethod
    def delete_note(
            cls,
            data: RequestData,
            note_id: int
    ) -> Response:
        note = NoteModel.find_by_id(note_id)
        note.delete_from_db()
        return redirect(url_for('home'))

    @classmethod
    def _change_note_visibility(cls, note: NoteModel, data: RequestPayload):
        persons_to_on, persons_to_off = cls._visibility_changing_list(
            PersonModel.get_all(),
            data,
        )
        note.add_persons_visibility(persons_to_on)
        note.remove_persons_visibility(persons_to_off)

    @classmethod
    def _change_note_subjects(cls, note: NoteModel, data: RequestPayload):
        subjects_to_add, subjects_to_remove = cls._subjects_changing_list(
            note.subjects.all(),
            data,
            SubjectModel.get_all(),
        )
        note.add_subjects(subjects_to_add)
        note.remove_subjects(subjects_to_remove)

    @classmethod
    def _visibility_changing_list(
            cls,
            all_persons: List["PersonModel"],
            data: RequestPayload,
    ) -> Tuple[Set["PersonModel"], Set["PersonModel"]]:
        """Prepare sets of persons to add/remove visibility.

        :param all_persons: all persons who needs to be checked visibility state
        :param data: dictionary containing previous state of visibility
        ('vis_previous_xxx' keys) and current state ('visibility_xxx' keys)
        of xxx in all_persons
        :return: set of persons to add visibility and set of persons to remove
        visibility
        """

        visibility_previously = {
            person.name:
                cls._bool_from_string(data[f"vis_previous_{person.name}"])
            for person in all_persons
        }

        visibility_names_on = {
            key[len("visibility_"):] for key in data.keys() if
            "visibility_" in key
        }
        for key in visibility_names_on:
            if data["visibility_" + key].lower() != "true":
                raise ValueError(
                    f"Value of form 'visibility_{key}' was different that "
                    f"'True' ({data['visibility_' + key]})"
                )

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

    @classmethod
    def _subjects_changing_list(
            cls,
            current_subjects: List["SubjectModel"],
            data: RequestPayload,
            all_subjects: List["SubjectModel"],
    ):
        current_subjects_names = {
            subject.name for subject in current_subjects
        }
        valid_new_subjects = {
            data[key] for key in data.keys() if
            re.match(r"\Asubject\d+\Z", key) and
            data[key] not in ['none', 'new']
        }

        all_subjects_dictionary = {
            subject.name: subject for subject in all_subjects
        }

        subjects_to_add = {
            all_subjects_dictionary[name] for name in
            valid_new_subjects - current_subjects_names
        }
        subjects_to_remove = {
            all_subjects_dictionary[name] for name in
            current_subjects_names - valid_new_subjects
        }

        return subjects_to_add, subjects_to_remove

    @classmethod
    def _get_note_schema(cls, admin=False) -> NoteSchema:
        if admin:
            return note_schema
        return note_schema_without_visibility