from marshmallow import Schema, fields


class Meta(type):
    """The meta class.
    The new class will have these attributes:
    - `__init__` method
    - `asdict` method
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
        for field_name in dir(new_class):
            field = getattr(new_class, field_name)
            for base in field.__class__.__mro__:
                if hasattr(base, '__module__') \
                        and base.__module__ == 'marshmallow.fields':
                    FIELDS[field_name] = field

        # create schema
        SCHEMA = Schema.from_dict(FIELDS)()

        # add attributes
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

    class MyString(fields.Str):
        pass

    class User(metaclass=Meta):
        name = MyString()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    cardi = User(name='Cardi B')
    print(cardi.asdict())
