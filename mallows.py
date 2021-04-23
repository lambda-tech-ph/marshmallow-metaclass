from marshmallow import Schema
from marshmallow.fields import Field


class MetaMethods:
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
        """Custom __new__ method."""
        new_class = super().__new__(cls, name, bases+(MetaMethods,), attrs)

        # get all marshmallow field attributes
        FIELDS = dict()
        for attr_name in dir(new_class):
            obj = getattr(new_class, attr_name)
            if isinstance(obj, Field):
                FIELDS[attr_name] = obj

        # create schema
        SCHEMA = Schema.from_dict(FIELDS)()

        # add attributes
        new_class.SCHEMA = SCHEMA
        new_class.FIELDS = FIELDS

        return new_class
