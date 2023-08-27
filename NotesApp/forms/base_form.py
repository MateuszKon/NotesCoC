from collections import OrderedDict

from wtforms_alchemy import ModelForm


class OrderedForm(ModelForm):
    _field_order = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_order = getattr(self, '_field_order')
        visited = []
        if field_order:
            new_fields = OrderedDict()
            for field_name in field_order:
                if field_name in self._fields:
                    new_fields[field_name] = self._fields[field_name]
                    visited.append(field_name)
            for field_name in self._fields:
                if field_name in visited:
                    continue
                new_fields[field_name] = self._fields[field_name]
            self._fields = new_fields
