from marshmallow import Schema
from marshmallow.fields import Field


class Meta(type):
    """The meta class.
    The new class will have these attributes:
    - `SCHEMA`
        > This is generated even if the class isn't instantiated.
        > If you want a nested object, you will always use this
          like, `Class.SCHEMA`.
    - `FIELDS`
        > This is a dictionary of all marshmallow fields inside
          the class.
    """

    def __new__(cls, name, bases, attrs):
        # Collect fields from current class and remove them from attrs.
        attrs['declared_fields'] = {
            key: attrs.pop(key) for key, value in list(attrs.items())
            if isinstance(value, Field)
        }

        new_class = super().__new__(cls, name, bases, attrs)

        # Walk through the MRO.
        declared_fields = {}
        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        # add attributes
        new_class.SCHEMA = Schema.from_dict(declared_fields)()
        new_class.FIELDS = declared_fields

        return new_class


class DeclarativeFields(metaclass=Meta):
    """Separate class for the methods.
    `Meta` will make new classes inherit from this.
    """

    def __init__(self, **kwargs):
        """Custom __init__ method."""
        # desirialize
        self.data = self.SCHEMA.load(kwargs)
        # set attributes
        for key, val in self.data.items():
            setattr(self, key, val)
        for field in self.FIELDS.keys():
            if not field in self.data.keys():
                setattr(self, field, None)

    def asdict(self):
        """Return a dictionary version of the object."""
        dictionary = self.data
        for field in self.FIELDS.keys():
            if not field in self.data.keys():
                dictionary[field] = None
        return dictionary
