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
            for base in field.__class__.__mro__:
                if hasattr(base, '__module__') \
                        and base.__module__ == 'marshmallow.fields':
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


if __name__ == '__main__':
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

    # taylor = Singer(foo='bar')
    # marshmallow.exceptions.ValidationError: {'foo': ['Unknown field.']}

    # taylor = Singer(email='gmail.com')
    # marshmallow.exceptions.ValidationError: {'email': ['Not a valid email address.']}

    class Person(metaclass=Meta):
        name = fields.Str()
        email = fields.Email()

    class Album(metaclass=Meta):
        songs = fields.List(fields.Str())
        singer = fields.Nested(Human.SCHEMA)
        name = fields.Str()

    lady = Person(name='Lady Gaga', email='lady@gmail.com')
    album = Album(
        name='Chromatica',
        singer=lady.data,
        songs=[
            '911',
            'Rain On Me',
            'Free Woman',
            'Enigma',
            'Stupid Love'
        ]
    )
    print(album.asdict())
    # {
    #     'songs': [
    #         '911',
    #         'Rain On Me',
    #         'Free Woman',
    #         'Enigma',
    #         'Stupid Love'
    #     ],
    #     'singer': {
    #         'name': 'Lady Gaga'
    #     },
    #     'name': 'Chromatica'
    # }
