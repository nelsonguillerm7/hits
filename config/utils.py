from django.core.exceptions import FieldDoesNotExist
from django.forms.utils import pretty_name
from django.utils.html import format_html


class Field:
    FIELD_SEPARATOR = "__"
    LABEL_SEPARATOR = ":"
    BOOLEAN_YES = "Yes"
    BOOLEAN_NO = "No"

    @classmethod
    def get_field_label(cls, model, field):
        try:
            name, verbose_name = field.split(cls.LABEL_SEPARATOR)
            return pretty_name(verbose_name)
        except ValueError:
            pass
        if "__str__" in field:
            label = str(model._meta.verbose_name)
            return pretty_name(label)
        names = field.split(cls.FIELD_SEPARATOR)
        name = names.pop(0)
        if not hasattr(model, name):
            str_model = (
                model._meta.model_name if hasattr(model, "_meta") else str(model)
            )
            raise AttributeError(f"Does not exist attribute <{name}> for {str_model}.")
        try:
            field = model._meta.get_field(name)
            if len(names):
                related_model = field.related_model
                return cls.get_field_label(
                    related_model, cls.FIELD_SEPARATOR.join(names)
                )
            label = field.verbose_name
        except FieldDoesNotExist:
            attr = getattr(object, name)
            if len(names):
                return cls.get_field_label(
                    attr(model) if callable(attr) else attr,
                    cls.FIELD_SEPARATOR.join(names),
                )
            label = name
        return pretty_name(label)

    @classmethod
    def get_field_value(cls, object, field):
        if "__str__" in field:
            return object
        if object is None:
            return object
        field = field.split(cls.LABEL_SEPARATOR)[0]
        names = field.split(cls.FIELD_SEPARATOR)
        name = names.pop(0)
        if not hasattr(object, name):
            raise AttributeError(
                f"Does not exist attribute <{name}> for {str(object)}."
            )
        if len(names):
            attr = getattr(object, name)
            return cls.get_field_value(
                attr() if callable(attr) else attr, cls.FIELD_SEPARATOR.join(names)
            )
        try:
            field = object._meta.get_field(name)
            if field.choices:
                return dict(field.choices).get(field.value_from_object(object))
            elif field.related_model:
                try:
                    return field.related_model.objects.get(
                        pk=field.value_from_object(object)
                    )
                except field.related_model.DoesNotExist:
                    return None
            else:
                return field.value_from_object(object)
        except FieldDoesNotExist:
            attr = getattr(object, name)
            attr = attr() if callable(attr) else attr
            if isinstance(attr, bool):
                attr = cls.BOOLEAN_YES if attr else cls.BOOLEAN_NO
            return format_html(str(attr))
