from marshmallow import Schema, fields


class Meta(type):
    """The meta class."""

    def __new__(cls, name, bases, attrs):
        """Custom __new__ method."""
        new_class = super().__new__(cls, name, bases, attrs)

        # get all marshmallow field attributes
        FIELDS = dict()
        for field_name in dir(new_class):
            field = getattr(new_class, field_name)
            if hasattr(field, '__module__') \
                    and field.__module__ == 'marshmallow.fields':
                FIELDS[field_name] = field

        # create schema
        SCHEMA = Schema.from_dict(FIELDS)()

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
            """Return dictionary."""
            dictionary = self.data
            for field in self.FIELDS.keys():
                if not field in self.data.keys():
                    dictionary[field] = None
            return dictionary

        # add attributes
        new_class.__init__ = __init__
        new_class.asdict = asdict
        new_class.SCHEMA = SCHEMA
        new_class.FIELDS = FIELDS

        return new_class


class KardeshevBeing(metaclass=Meta):
    level = fields.Int()


class Alien(KardeshevBeing):
    planet = fields.Str()


class Human(Alien):
    name = fields.Str()
    email = fields.Email()


class Singer(Human):
    album = fields.Str()


lady = Singer(name='Lady Gaga', email='lady@gmail.com',
              planet='Venus', album='Chromatica', level=1)
print(lady.asdict())
# {'email': 'lady@gmail.com', 'name': 'Lady Gaga', 'level': 1, 'album': 'Chromatica', 'planet': 'Venus'}
print(f'{lady.name} is from {lady.planet}')
# Lady Gaga is from Venus

nicki = Singer(name='Nicki Minaj')
print(nicki.email)
# None
print(nicki.asdict())
# {'name': 'Nicki Minaj', 'album': None, 'email': None, 'level': None, 'planet': None}

taylor = Singer(foo='Foo')
# marshmallow.exceptions.ValidationError: {'foo': ['Unknown field.']}
