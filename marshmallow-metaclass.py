from marshmallow import Schema, fields


class Meta(type):
    """The meta class."""

    def __new__(cls, name, bases, attrs):
        """Custom __new__  method."""

        def __init__(self, **kwargs):
            """Custom __init__ method."""
            # get all marshmallow fields
            self.fields = []
            for field in dir(self):
                f = getattr(self, field)
                if hasattr(f, '__module__') \
                        and f.__module__ == 'marshmallow.fields':
                    self.fields.append(field)

            # create schema
            self.field_keys = dict()
            for field in self.fields:
                self.field_keys[field] = getattr(self, field)
            self.schema = Schema.from_dict(self.field_keys)()

            # desirialize
            self.data = self.schema.load(kwargs)

            # set attributes
            for key, val in self.data.items():
                setattr(self, key, val)
            for field in self.fields:
                if not field in self.data.keys():
                    setattr(self, field, None)

        def asdict(self):
            """Return dictionary."""
            dictionary = self.data
            for field in self.fields:
                if not field in self.data.keys():
                    dictionary[field] = None
            return dictionary

        # create new class and add custom __init__ method
        new_class = super().__new__(cls, name, bases, attrs)
        setattr(new_class, '__init__', __init__)
        setattr(new_class, 'asdict', asdict)
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
